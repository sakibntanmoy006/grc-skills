#!/usr/bin/env python3
"""List, search, and selectively download the public Google Drive policy/SOP library.

Public folders only. The root folder must be shared to "Anyone with the link".

Usage:
    python3 fetch_library.py                  # build the tree index only (fast, no downloads)
    python3 fetch_library.py --search "anti bribery"   # match the query, download only matches
    python3 fetch_library.py --search "food safety" --limit 5
    python3 fetch_library.py --download-all   # full download of every document
    python3 fetch_library.py --folder-id <ID> # override root folder from config.json

Outputs:
    library/tree.json      # cached index of folders/files (built by every run)
    library/search/<...>   # downloads for a --search run
    library/<tree>         # full mirror for --download-all

Config file (config.json):
    {
        "drive": {
            "folder_id": "<PUBLIC_SHARED_ROOT_FOLDER_ID>",
            "folder_url": "https://drive.google.com/drive/folders/<ID>"
        }
    }
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

FOLDER_VIEW = "https://drive.google.com/embeddedfolderview"
UC_DOWNLOAD = "https://drive.google.com/uc?export=download"
EXPORT_SPECS = {
    "document": ("https://docs.google.com/document/d/{}/export?format=txt", ".txt"),
    "spreadsheet": ("https://docs.google.com/spreadsheets/d/{}/export?format=csv", ".csv"),
    "presentation": ("https://docs.google.com/presentation/d/{}/export?format=txt", ".txt"),
}

DOC_TYPES = {
    "policy": ("policy", "-pol", "_pol", "standard"),
    "sop": ("sop", "procedure", "work instruction", "work-instruction", "wi-", "-wi"),
    "register": ("register", "log", "tracker", "record", "matrix", "register"),
    "form": ("form", "template", "fr-", "checklist"),
}

ENTRY_RE = re.compile(
    r'flip-entry" id="entry-([^"]+)".*?<a href="([^"]+)"[^>]*>.*?flip-entry-title">([^<]*)',
    re.S,
)


def classify(name: str) -> str:
    n = name.lower()
    scores = {dt: sum(1 for m in mk if m in n) for dt, mk in DOC_TYPES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "unknown"


def safe_name(name: str) -> str:
    name = name.replace("/", "_")
    return "".join(c if c.isalnum() or c in " .-_()" else "_" for c in name)


def fetch_folder_page(folder_id: str):
    url = f"{FOLDER_VIEW}?id={folder_id}#list"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_entries(html: str):
    entries = []
    for fid, href, title in ENTRY_RE.findall(html):
        title = title.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        is_folder = "/drive/folders/" in href
        entries.append({"id": fid, "name": title.strip(), "is_folder": is_folder})
    return entries


def walk_tree(folder_id: str, path: str, visited: set, out: list):
    if folder_id in visited:
        return
    visited.add(folder_id)
    html = fetch_folder_page(folder_id)
    for e in parse_entries(html):
        entry_path = os.path.join(path, e["name"]) if path else e["name"]
        if e["is_folder"]:
            out.append({"id": e["id"], "name": e["name"], "path": entry_path, "is_folder": True})
            walk_tree(e["id"], entry_path, visited, out)
        else:
            out.append(
                {
                    "id": e["id"],
                    "name": e["name"],
                    "path": entry_path,
                    "is_folder": False,
                    "doc_type": classify(e["name"]),
                }
            )


def build_tree(folder_id: str, out_dir: str):
    out = []
    walk_tree(folder_id, "", set(), out)
    os.makedirs(out_dir, exist_ok=True)
    tree_path = os.path.join(out_dir, "tree.json")
    with open(tree_path, "w") as f:
        json.dump({"root": folder_id, "entries": out}, f, indent=2)
    folders = sum(1 for e in out if e["is_folder"])
    files = sum(1 for e in out if not e["is_folder"])
    print(f"Indexed {folders} folders, {files} documents -> {tree_path}")
    return out


def load_tree(out_dir: str):
    tree_path = os.path.join(out_dir, "tree.json")
    if not os.path.exists(tree_path):
        return None
    with open(tree_path) as f:
        return json.load(f).get("entries", [])


def tokenize(text: str):
    toks = set(re.findall(r"[a-z0-9]{2,}", text.lower()))
    return {t for t in toks if t not in {"the", "and", "for", "with", "from", "our", "all", "per"}}


def match_tree(tree: list, query: str):
    terms = tokenize(query)
    if not terms:
        return []
    scored = []
    for e in tree:
        if e["is_folder"]:
            continue
        text = f"{e['name']} {e['path']}".lower()
        score = sum(3 if t in e["name"].lower() else (2 if t in e["path"].lower() else 0) for t in terms)
        if score:
            scored.append((score, e))
    scored.sort(key=lambda x: -x[0])
    return [e for _, e in scored]


def download_file(file_id: str, name: str, out_dir: str):
    base = os.path.join(out_dir, safe_name(name))
    has_ext = bool(os.path.splitext(name)[1])
    if has_ext:
        candidates = [f"{UC_DOWNLOAD}&id={file_id}"]
        final_ext = ""
    else:
        candidates = [tpl.format(file_id) for tpl, _ in EXPORT_SPECS.values()]
        candidates.append(f"{UC_DOWNLOAD}&id={file_id}")
        final_ext = ".bin"

    for url in candidates:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                ctype = resp.headers.get("Content-Type", "")
                body = resp.read()
            if "text/html" in ctype or body[:1] == b"<":
                continue
            if not has_ext:
                for spec_name, (_, spec_ext) in EXPORT_SPECS.items():
                    if f"/{spec_name}/" in url:
                        final_ext = spec_ext
                        break
            out = base + final_ext
            with open(out, "wb") as f:
                f.write(body)
            return out, len(body)
        except (urllib.error.HTTPError, urllib.error.URLError):
            continue
    raise RuntimeError(f"Could not download {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "..", "config.json"))
    ap.add_argument("--folder-id")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "library"))
    ap.add_argument("--search", help="query to match against file/folder names")
    ap.add_argument("--limit", type=int, default=0, help="max matches to download for --search")
    ap.add_argument("--download-all", action="store_true", help="download every document")
    args = ap.parse_args()

    folder_id = args.folder_id
    if not folder_id and os.path.exists(args.config):
        with open(args.config) as f:
            folder_id = (json.load(f).get("drive") or {}).get("folder_id") or None
    if not folder_id:
        print("ERROR: folder_id required. Set it in config.json or pass --folder-id.", file=sys.stderr)
        sys.exit(2)

    if args.download_all:
        manifest = []
        visited = set()

        def crawl(fid, path):
            if fid in visited:
                return
            visited.add(fid)
            os.makedirs(path, exist_ok=True)
            print(f"[folder] {path}")
            for e in parse_entries(fetch_folder_page(fid)):
                if e["is_folder"]:
                    crawl(e["id"], os.path.join(path, safe_name(e["name"])))
                else:
                    try:
                        out, size = download_file(e["id"], e["name"], path)
                    except Exception as exc:
                        print(f"  [FAIL] {e['name']}: {exc}")
                        continue
                    manifest.append(
                        {
                            "name": e["name"],
                            "drive_id": e["id"],
                            "saved_as": os.path.relpath(out, start=args.out),
                            "doc_type": classify(e["name"]),
                            "size": size,
                        }
                    )
                    print(f"  [file] {e['name']}")

        crawl(folder_id, args.out)
        with open(os.path.join(args.out, "manifest.json"), "w") as mf:
            json.dump(manifest, mf, indent=2)
        n_types = {}
        for m in manifest:
            n_types[m["doc_type"]] = n_types.get(m["doc_type"], 0) + 1
        print(f"\nDone. {len(manifest)} documents fetched: {n_types}")
        return

    tree = load_tree(args.out)
    if tree is None or not args.search:
        tree = build_tree(folder_id, args.out)

    if args.search:
        matches = match_tree(tree, args.search)
        if not matches:
            print(f"No documents matched '{args.search}' in the library tree.")
            return
        if args.limit:
            matches = matches[: args.limit]
        search_dir = os.path.join(args.out, "search")
        os.makedirs(search_dir, exist_ok=True)
        print(f"Downloading {len(matches)} matched documents to {search_dir}")
        for e in matches:
            try:
                out, size = download_file(e["id"], e["name"], search_dir)
                print(f"  {e['name']}  (score, path: {e['path']}) -> {os.path.basename(out)} ({size} b)")
            except Exception as exc:
                print(f"  [FAIL] {e['name']}: {exc}")
        print("\nMatches are in library/search/. Extract their text and read them before answering.")


if __name__ == "__main__":
    main()
