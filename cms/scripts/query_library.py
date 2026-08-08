#!/usr/bin/env python3
"""Query the public Google Drive policy/SOP library without saving anything locally.

Everything is fetched on demand and held only in memory:
  - folder listing pages (metadata: names, paths, doc types)
  - the text of only the top matching documents (never persisted)

Usage:
    python3 query_library.py "anti bribery"
    python3 query_library.py "food safety" --limit 5
    python3 query_library.py "AML" --folder-id <ROOT_ID>    # override config.json
    python3 query_library.py --tree compliance              # list names only in a subfolder
    python3 query_library.py --save-to /tmp/out <topic>     # optionally write fetched text

Nothing is written to the skill/library directory unless --save-to is given.
"""

import argparse
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile

FOLDER_VIEW = "https://drive.google.com/embeddedfolderview"
UC_DOWNLOAD = "https://drive.google.com/uc?export=download"
EXPORT_SPECS = {
    "document": ("https://docs.google.com/document/d/{}/export?format=txt", ".txt"),
    "spreadsheet": ("https://docs.google.com/spreadsheets/d/{}/export?format=csv", ".csv"),
    "presentation": ("https://docs.google.com/presentation/d/{}/export?format=txt", ".txt"),
}

ENTRY_RE = re.compile(
    r'flip-entry" id="entry-([^"]+)".*?<a href="([^"]+)"[^>]*>.*?flip-entry-title">([^<]*)',
    re.S,
)
STOPWORDS = {"the", "and", "for", "with", "from", "our", "all", "per", "any"}


def fetch(folder_id: str):
    req = urllib.request.Request(
        f"{FOLDER_VIEW}?id={folder_id}#list", headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def entries(folder_id: str):
    html = fetch(folder_id)
    out = []
    for fid, href, title in ENTRY_RE.findall(html):
        title = title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        out.append({"id": fid, "name": title.strip(), "is_folder": "/drive/folders/" in href})
    return out


def tokenize(text: str):
    toks = set(re.findall(r"[a-z0-9]{2,}", text.lower()))
    return {t for t in toks if t not in STOPWORDS}


ALIASES = {
    "compliance": {"compliance", "bribery", "anti", "corrupt", "aml", "money", "whistle", "ethics", "integrity", "legal"},
    "tax": {"tax", "vat", "duty", "customs", "transfer pricing"},
    "finance": {"finance", "accounting", "payable", "receivable", "treasury"},
    "treasury": {"treasury", "cash", "fx", "bank"},
    "internal audit": {"audit", "internal audit", "auditor"},
    "hr": {"hr", "human resource", "employee", "workforce", "recruit", "training", "attendance", "leave"},
    "hseq": {"hseq", "hse", "safety", "health", "environment", "hazard", "chemical", "emergency", "waste", "incident"},
    "esg": {"esg", "sustainability", "carbon", "climate", "biodiversity", "water"},
    "it": {"it", "information", "cyber", "cybersecurity", "data", "privacy", "security", "software", "cloud", "network", "server"},
    "scm": {"scm", "procurement", "supply", "vendor", "purchase", "logistics", "import", "export"},
    "logistics & distribution": {"logistics", "distribution", "transport", "fleet", "shipping"},
    "warehouse": {"warehouse", "storage", "inventory", "stock"},
    "quality": {"quality", "product", "laboratory", "metrology", "food safety", "packaging"},
    "project management": {"project", "capex"},
    "brand and marketing": {"brand", "marketing", "advertis", "advertising", "promotion"},
    "revenue": {"revenue", "sales"},
    "operation": {"operation", "production", "manufacturing"},
    "research and insight": {"research", "insight", "rnd", "innovation"},
    "company secretaritae": {"company secretar", "board", "governance", "agm", "egm"},
    "opex": {"opex"},
}


def alias_folders(terms: set):
    """Return Function department names that plausibly cover the query terms."""
    hits = set()
    for folder, keywords in ALIASES.items():
        if terms & keywords:
            hits.add(folder)
    return hits


def score(terms: set, name: str, path: str):
    n, p = name.lower(), path.lower()
    s = 0
    for t in terms:
        if t in n:
            s += 3
        elif t in p:
            s += 2
    return s


def raw_download(file_id: str):
    req = urllib.request.Request(f"{UC_DOWNLOAD}&id={file_id}", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        ctype = resp.headers.get("Content-Type", "")
        body = resp.read()
    if "text/html" in ctype or body[:1] == b"<":
        raise RuntimeError("not a file payload")
    return body


def native_download(file_id: str):
    specs = [tpl for tpl, _ in EXPORT_SPECS.values()]
    for tpl in specs:
        try:
            req = urllib.request.Request(tpl.format(file_id), headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read()
            if body[:1] != b"<":
                return body
        except (urllib.error.HTTPError, urllib.error.URLError):
            continue
    return raw_download(file_id)


def extract_text(name: str, body: bytes):
    n = name.lower()
    if n.endswith(".pdf"):
        tmp = "/tmp/_cms_query.pdf"
        with open(tmp, "wb") as f:
            f.write(body)
        out = os.popen(f"pdftotext {tmp} - 2>/dev/null").read()
        try:
            os.remove(tmp)
        except OSError:
            pass
        return out
    if n.endswith(".docx"):
        try:
            with zipfile.ZipFile(io.BytesIO(body)) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
            return re.sub(r"<[^>]+>", " ", xml).replace("\x00", "").strip()
        except Exception:
            return "[unable to extract docx text]"
    if n.endswith(".xlsx"):
        try:
            import openpyxl

            wb = openpyxl.load_workbook(io.BytesIO(body), read_only=True)
            lines = []
            for ws in wb.worksheets:
                lines.append(f"== {ws.title} ==")
                for row in ws.iter_rows(values_only=True):
                    cells = [str(c) for c in row if c is not None]
                    if cells:
                        lines.append(" | ".join(cells))
            return "\n".join(lines)
        except Exception:
            return "[unable to extract xlsx text]"
    try:
        return body.decode("utf-8", "replace")
    except Exception:
        return "[binary; unable to decode text]"


def resolve_root(folder_id):
    if folder_id:
        return folder_id
    cfg = os.path.join(os.path.dirname(__file__), "..", "config.json")
    if os.path.exists(cfg):
        with open(cfg) as f:
            fid = (json.load(f).get("drive") or {}).get("folder_id")
            if fid:
                return fid
    print("ERROR: folder_id required (config.json or --folder-id).", file=sys.stderr)
    sys.exit(2)


def list_tree(root, depth=0):
    for e in entries(root):
        print("  " * depth + ("[F] " if e["is_folder"] else "     ") + e["name"])
        if e["is_folder"]:
            list_tree(e["id"], depth + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic", nargs="?")
    ap.add_argument("--folder-id")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--tree", action="store_true", help="print the folder/file tree (metadata only)")
    ap.add_argument("--save-to", help="optionally write fetched document text here")
    args = ap.parse_args()

    root = resolve_root(args.folder_id)
    if args.tree:
        list_tree(root)
        return
    if not args.topic:
        ap.print_help()
        sys.exit(1)

    terms = tokenize(args.topic)
    if not terms:
        print("Could not parse topic into keywords.")
        sys.exit(1)
    print(f"Query: '{args.topic}' | keywords: {', '.join(sorted(terms))}\n")

    # metadata pass: pick relevant roots, then departments/companies inside them
    file_matches = []  # (score, id, name, area)
    root_entries = entries(root)
    desired = alias_folders(terms)
    budget = 30  # max folder-listing pages fetched (metadata only)

    def scan_folder(fid, name, path, depth):
        nonlocal budget
        if budget <= 0:
            return
        budget -= 1
        try:
            children = entries(fid)
        except Exception as exc:
            print(f"  (could not read {name}: {exc})")
            return
        for c in children:
            if c["is_folder"]:
                cm = score(terms, c["name"], name)
                if depth == 0 and "function" in name.lower():
                    cm = cm or any(d in c["name"].lower() for d in desired)
                if cm:
                    scan_folder(c["id"], c["name"], f"{path}/{c['name']}", depth + 1)
            else:
                fs = score(terms, c["name"], path) or score(terms, c["name"], name)
                if fs:
                    file_matches.append((fs, c["id"], c["name"], path))

    scanned_roots = []
    for re_ in root_entries:
        if not re_["is_folder"]:
            continue
        root_name = re_["name"]
        root_l = root_name.lower()
        if "function" in root_l and desired:
            print(f"[area] {root_name} (departments: {', '.join(sorted(desired))})")
            scan_folder(re_["id"], root_name, root_name, 0)
            scanned_roots.append(root_name)
        elif score(terms, root_name, root_name) > 0 or (
            "sbu" in root_l and any(score(terms, c["name"], root_name) > 0 for c in entries(re_["id"]) if c["is_folder"])
        ):
            print(f"[area] {root_name}")
            scan_folder(re_["id"], root_name, root_name, 0)
            scanned_roots.append(root_name)

    if not scanned_roots:
        print("No area matched. Listing top-level areas:\n")
        list_tree(root)
        return
    print(f"\nMatched {len(file_matches)} documents.")

    if not file_matches:
        print("No documents found by name/path for this topic. The topic is not covered "
              "by the organization library -> resolve against the global standard.")
        return

    file_matches.sort(key=lambda c: -c[0])
    picks = file_matches[: args.limit]
    print(f"Fetching text for top {len(picks)} matches (no local persistence)...\n")

    for s, fid, name, area in picks:
        print("=" * 70)
        print(f"DOCUMENT: {name}  (area: {area}, score: {s})")
        try:
            body = raw_download(fid) if os.path.splitext(name)[1] else native_download(fid)
            text = extract_text(name, body)
        except Exception as exc:
            print(f"  [fetch failed] {exc}\n")
            continue
        if args.save_to:
            safe = re.sub(r"[^\w.\-]", "_", name) + ".txt"
            os.makedirs(args.save_to, exist_ok=True)
            with open(os.path.join(args.save_to, safe), "w") as f:
                f.write(text)
            print(f"  [saved to {os.path.join(args.save_to, safe)}]")
        print(text[:6000])
        if len(text) > 6000:
            print(f"\n  ... (truncated, {len(text)} chars total)")
        print()


if __name__ == "__main__":
    main()
