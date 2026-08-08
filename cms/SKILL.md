---
name: cms
description: Compliance resolver for an enterprise Compliance Management System (CMS) built on the organization's policy/SOP library and a catalog of 584 filterable compliance requirements across 80 domains and 11 categories. Use when someone asks whether an activity, process, or working method is compliant, or wants to know what the organization requires. The answer is resolved from the organization's own policies and SOPs first; only when a topic is not covered by the internal library is it checked against the global standard, with the gap reported explicitly. Also use for full library-to-standard coverage scans.
license: MIT
metadata:
  author: humaninside
  tags: cms, compliance, checker, verdict, obligation, iso-37301, grc, audit, governance, legal, esg, hse
---

# Compliance Catalog — Library-First Compliance Resolver

## Overview

This skill answers compliance questions for an enterprise using two sources, in this
**strict order**:

1. **The organization's own policy/SOP library** (fetched from the public Google Drive
   folder). This is the first source of the answer.
2. **The global compliance standard** — a catalog of **584 requirements** across
   **80 domains** and **11 categories**. Used only when the library does not cover the topic.

**Resolution rule:**

- If the topic is **found** in a policy/SOP → the answer comes from that document.
- If **not found** → first state clearly that it is not found in the organization's
  policies/SOPs, then check the global standard and give the result (including the
  internal coverage gap this creates).

The requirement index is in `references/requirements-index.csv`
(name, domain, category, applicability, process owner). Full field detail lives in
`references/requirements-full.csv` (all 13 fields) and in
`references/Compliance_Requirements_Only.xlsx` (the source workbook). Always load full
field detail before judging against the global standard.

---

## Part A — Compliance Query Resolution (Primary)

Use this for any compliance question: "Is <activity/process/method> compliant?",
"What does the company require for <topic>?", "Do we cover <requirement>?"

### Step 1 — Identify the compliance topic

From the question, extract:

- **Topic** (the subject: anti-bribery, food safety, data privacy, HR records, tax
  filing, waste disposal, etc.)
- **Who** (role, function, SBU, factory, site — e.g., Finance, HR, Akij Cement)
- **What** (the process, action, or working method to be checked)

If the topic is ambiguous, ask for the specific activity or document name.

### Step 2 — Query the library remotely (no downloads, nothing persisted)

- Read `config.json` for the shared Drive `folder_id` (no API key needed; folder is public).
- Run `python3 scripts/query_library.py "<topic>"` — this:
  1. Fetches **only folder-listing pages** (metadata: names, paths) to find the relevant
     Function department / SBU area, matched by keywords and a department-alias map
     (e.g., "anti bribery" → Function/Compliance, "tax" → Function/Tax).
  2. Downloads **only the top matching documents** into memory and prints their
     extracted text (PDF via pdftotext, DOCX/XLSX parsed, Google-native files exported).
  3. **Persists nothing** — no library cache, no files written to disk (unless
     `--save-to <dir>` is used deliberately).
- If the query returns no match, widen it with more synonyms or an explicit area:
  `python3 scripts/query_library.py --tree` lists names only, or point at a specific
  folder with `--tree <area>`.

### Step 3 — Search the fetched text

Search the query output (document text) for the topic:

- Match by keywords, the function/SBU folder path, and the document name.
- Look for documents of type policy, SOP, register, or form (based on name markers:
  POL-, SOP-, WI-, REG-, FR-, "policy", "procedure", "register", "template").
- Collect every relevant document. Do not silently skip an unreadable document —
  flag it.

### Step 4 — Resolve: found in library

If one or more policies/SOPs cover the topic, the **answer comes from them**:

```
FOUND IN ORGANIZATIONAL LIBRARY

Document: <name> (<doc type>, <function/SBU path>)
Source: <saved path in library/>

What Our <Policy/SOP> Requires:
<quote/summarize the internal rule: scope, controls, evidence, approvals,
retention, escalation>

Relevant Requirements (global standard) It Aligns With:
Requirement: <name> (Domain: <domain>) — <COMPLIANT | PARTIAL | NOT EVALUATED>
<note any gap between the internal document and the global standard's minimum
requirements / required evidence / pass criteria>
```

- The primary answer is the internal document's position. Do not substitute the global
  standard for it.
- Optionally, still check alignment with the global standard and report PARTIAL gaps
  (the internal document exists but may fall short of the global minimum bar).

### Step 5 — Resolve: not found in library

If no policy/SOP covers the topic, follow this order **exactly**:

```
NOT FOUND IN ORGANIZATIONAL POLICY/SOP LIBRARY
Documents checked: <n> (list names of the closest/most similar documents, if any)

Now checking against the global standard...

Requirement: <name> (Domain: <domain>)
What the Global Standard Requires:
  Minimum Requirements: <field from the workbook>
  Required Evidence: <field from the workbook>
  Audit / Pass Criteria: <field from the workbook>
  Applicability: <field — does it apply to this role/SBU/factory?>

VERDICT: COMPLIANT | NON-COMPLIANT | NEEDS MORE INFORMATION

If NON-COMPLIANT:
  What Is Non-Compliant: <the specific behavior/gap>
  Minimum Requirement Violated: <field from the workbook>
  Evidence Missing: <what evidence is not produced/retained>
  Pass Criteria Failed: <the audit criterion not met>
  Non-Compliance Trigger Matched: <the trigger that applies>
  Remediation: <what to change, what evidence to start producing, who owns the fix
  (Indicative Process Owner), and the internal policy/SOP that must be created>

If NEEDS MORE INFORMATION:
  Missing: <what info is needed to judge>
  Ask: <specific questions to the user>

IMPORTANT: The lack of an internal policy/SOP is itself a coverage gap. If the
requirement applies and no internal document evidences it, the organization is
non-compliant with the global standard until a policy/SOP is created, regardless of
whether the underlying activity is carried out correctly in practice.
```

- First line must state the topic was **not found** in the library.
- Then evaluate only against the global standard (never guess at an internal rule).

---

## Part B — Full Library Scan (coverage report)

Use when the whole library must be checked against the global standard (e.g., "scan all
policies/SOPs").

### Step 1 — Fetch and ingest the library

- Run `python3 scripts/fetch_library.py --download-all` (optional, for a full local
  mirror) or query each area remotely with `scripts/query_library.py --tree` and
  `--save-to <dir>` to persist just what the scan needs.
- Extract text from PDFs/DOCX/XLSX so content can be searched.

### Step 2 — Load the global standard

Load all 584 requirements with full field detail from `references/requirements-full.csv`
or the workbook.

### Step 3 — Map both directions

1. **Document → requirements:** for each document, identify the requirements it is
   intended to satisfy (content keywords, domain/category tags, applicability patterns,
   stated scope).
2. **Requirement → documents:** for each applicable requirement, find which document(s)
   evidence it. Any requirement with **no** covering document is a coverage gap.

### Step 4 — Produce the report

```
LIBRARY COVERAGE REPORT — <date>

Global standard: 584 requirements / 80 domains / 11 categories
Documents scanned: <n> (policies: n, SOPs: n, registers: n, forms: n)

COVERAGE MAP (requirement -> document):
  Requirement: <name> (Domain: <domain>)
  Status: COVERED | PARTIAL | NO DOCUMENT
  Covering document: <name> (doc id)
  Gap: <what's missing vs minimum requirements / evidence / pass criteria>

PER-DOCUMENT GAP REPORT (document -> requirements):
  Document: <name> (<doc type>)
  Verdict: COMPLIANT | NON-COMPLIANT | PARTIAL | NOT ASSESSED
  Based on: <requirement names it satisfies, with the specific pass criteria met>
  Non-Compliant / Partial (for each gap):
    Requirement: <name> (Domain: <domain>)
    What Is Non-Compliant: <the specific gap in the document>
    Minimum Requirement Violated: <field from the workbook>
    Evidence Missing: <what evidence is not covered/retained>
    Pass Criteria Failed: <the audit criterion not met>
    Non-Compliance Trigger Matched: <the trigger that applies>
    Recommended Fix: <what to add/change, who owns it (Indicative Process Owner)>

SUMMARY:
  Requirements covered fully: n / 584
  Requirements with no document: n
  Documents fully compliant: n; partial: n; non-compliant: n
  Top domains at risk: <domains with most gaps>
```

- **Coverage gaps** (requirement with no document) are NON-COMPLIANT by default.
- **NOT ASSESSED** means the document text could not be extracted — flag it, do not infer.

---

## Rules of the Check

- **Internal library first, global standard second.** If a policy/SOP covers the topic,
  the answer comes from it. The global standard is consulted only when the library does
  not cover the topic — and that not-found is always stated first.
- **A missing document is a breach.** If a requirement applies and no policy/SOP
  evidences it, the organization is non-compliant with the global standard until one is
  created.
- **Judge on evidence and controls, not intention.** A good-faith effort without
  required evidence or controls is still non-compliant.
- **Scope matters.** Only judge against requirements that apply to the described role,
  SBU, factory, or activity. Requirements marked "Only the SBU or activity named" are
  not group-wide by default.
- **Minimum requirements are mandatory.** Missing any minimum requirement = non-compliant.
- **When in doubt, ask.** If the description or extracted text is insufficient to
  evaluate a requirement, mark NEEDS MORE INFORMATION / NOT ASSESSED rather than guessing.
- **Be specific.** Never answer "non-compliant" without naming the exact requirement(s)
  and the specific reason.

## Skill File Layout

```
cms/
  SKILL.md                            # this file
  config.json                         # Google Drive folder_id (public, no API key)
  scripts/query_library.py            # remote, zero-download query (default flow)
  scripts/fetch_library.py            # optional full local mirror (--download-all)
  references/requirements-index.csv   # name, domain, category, applicability, owner
  references/requirements-full.csv    # all 13 fields, 584 rows
  references/Compliance_Requirements_Only.xlsx  # source workbook (full detail)
```

## Catalog Reference

### 11 Categories and Domain Coverage

| Category | Domains |
|---|---|
| Governance, Legal & Integrity (152) | Corporate Governance, Legal, Regulatory, Compliance Management System, Enterprise Risk Management, Audit & Assurance, Ethics & Integrity, Anti-Bribery, Whistleblowing, Fraud Control, Competition & Antitrust, Procurement Integrity, Contract Management, Document & Record Management, Records Management, Internal Policy |
| Quality, Product & Customer (89) | Quality, Industry Certification, Buyer, Product, Packaging, Food Safety, Laboratory, Metrology, Customer & Market, Consumer Affairs, Marketing, Sales, Research & Innovation |
| HSE, Environment & Sustainability (77) | Occupational Health & Safety, Environmental, Chemical, Energy, Water Stewardship, Biodiversity, Carbon, Circular Economy, ESG, ESG Due Diligence, Sustainability, Sustainability Reporting |
| Supply Chain, Trade & Operations (62) | Procurement, Supply Chain, Third Party, Import Export, Trade, Export Customer, Logistics, Fleet, Operational |
| Technology, Data & Security (56) | Information Security, Cyber Security, Privacy & Data Protection, IT Governance, Cloud, Software, Digital Governance, Digital Transformation Governance, Artificial Intelligence |
| Finance, Tax & Insurance (40) | Finance, Tax, AML & Financial Crime, Insurance |
| Engineering, Assets & Manufacturing (29) | Engineering, Manufacturing, Asset Integrity, Process Safety Management, Reliability |
| People & Human Rights (28) | Human Resource, Human Rights, Diversity Equity & Inclusion, Travel & Mobility |
| Resilience, Security & Emergency (24) | Business Continuity, Crisis Management, Emergency Preparedness, Physical Security, Physical Asset Security |
| Sector-Specific & Regulated Activities (16) | Sector Specific Compliance |
| Projects, Property & Facilities (11) | Project, Real Estate & Infrastructure |

(Counts are number of requirements per category. Domain-level counts vary from 3–16.)

### Requirement Fields (Source Workbook Schema)

| Field | Meaning |
|---|---|
| Compliance Name | The requirement name |
| Domain Name | Governing domain it belongs to |
| Category | High-level grouping |
| What It Is | Definition |
| Why It Is Important | Rationale |
| Why It Is Needed | Driver (law, code, buyer, internal) |
| How It Should Work | Expected operating behaviour |
| Minimum Requirements for Compliance | Minimum controls/actions — the compliance bar |
| Required Evidence | Documentation required |
| Audit / Pass Criteria | How it is judged compliant |
| Non-Compliance Triggers | What constitutes a breach |
| Typical Applicability / SBU | Who/what it applies to |
| Indicative Process Owner | Accountable function |

## Common Applicability and Ownership Patterns

**Top applicability patterns:** Group-wide and all SBUs; all legal entities and
corporate offices; all employees/workers/contractors; all factories/sites/offices;
all taxable entities; all information assets/systems/users; SBU certification and
customer requirements; only the SBU or activity named.

**Most common process owners:** Chief Compliance Officer, Chief HR Officer, Company
Secretary/Board Office, Head of Legal, Head of Tax/CFO, Head of HSE, Head of
Environment, CFO, Chief Risk Officer, Procurement/Compliance, Management
Systems/Quality, CISO/Head of IT.

## Other Uses

The catalog also supports:

- **Obligation register mapping** — filter by category/domain/SBU and load owners,
  evidence, and pass criteria.
- **Risk-control matrices** — group by domain, define the risk, map minimum
  requirements and evidence as controls.
- **Monitoring, testing, and audits** — use audit/pass criteria as test definitions and
  non-compliance triggers to define findings.
- **Quick lookups** — "Who owns <domain>?", "What evidence does <requirement> need?",
  "Which requirements apply to all factories?"

## Reminders

- **Always resolve from the internal library first.** State "FOUND" with the document,
  or "NOT FOUND in organizational policy/SOP library" before consulting the global
  standard.
- Use `references/requirements-full.csv` for full field detail before judging against
  the global standard.
- Confirm applicability before judging; "Only the SBU or activity named" is not
  group-wide by default.
- Confirm process owners with the organization; the workbook provides indicative owners.
- Always answer with a clear result and, for non-compliance, the specific how and why.
