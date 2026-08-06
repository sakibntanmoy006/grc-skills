---
name: cms
description: Compliance checker for an enterprise Compliance Management System (CMS) built on a catalog of 584 filterable compliance requirements across 80 domains and 11 categories. Use when someone describes their work, process, or working method and wants to know whether it is compliant or non-compliant, and if non-compliant, exactly which requirements are breached, what minimum requirements are violated, what evidence is missing, and which non-compliance triggers apply.
license: MIT
metadata:
  author: humaninside
  tags: cms, compliance, checker, verdict, obligation, iso-37301, grc, audit, governance, legal, esg, hse
---

# Compliance Catalog — Enterprise Compliance Checker

## Overview

This skill evaluates whether a described activity, process, or working method is
**compliant** or **non-compliant** against an enterprise compliance catalog of
**584 requirements** across **80 domains** and **11 categories**.

Given any description of how someone does their work, this skill:

1. Identifies which compliance requirements could apply.
2. Compares the described working method against the minimum requirements, required
   evidence, and audit/pass criteria for those requirements.
3. Produces a clear verdict: **COMPLIANT**, **NON-COMPLIANT**, or **NEEDS MORE
   INFORMATION**.
4. If non-compliant, explains **how and why** it is non-compliant, citing the exact
   requirements breached.

The requirement index is in `references/requirements-index.csv`
(name, domain, category, applicability, process owner). The full field detail
(minimum requirements, evidence, pass criteria, non-compliance triggers) lives in the
source workbook `Compliance_Requirements_Only.xlsx`; load it when full detail is needed
for a verdict.

## The Compliance Check Workflow (Primary)

Whenever someone describes their work or working method and asks whether it is
compliant, follow this order:

### Step 1 — Understand the described activity

Extract from the description:

- **Who** (role, function, SBU, factory, site)
- **What** (the process, action, or working method)
- **How** (steps, handling of documents/evidence, approvals, retention, controls)

Ask clarifying questions only if you cannot determine scope from the description.

### Step 2 — Identify candidate requirements

- Filter the requirements index by keywords in the described activity, the role/SBU,
  and the applicability patterns (e.g., "all factories", "Group-wide", "procurement",
  "all information assets", "only the SBU named").
- Narrow to the most relevant requirements; do not judge against the whole catalog.
- Use the source workbook for full detail on each candidate.

### Step 3 — Evaluate each candidate requirement

For each candidate, compare the described method against:

- **Minimum Requirements for Compliance** — are all required controls/actions present?
- **Required Evidence** — is the required documentation produced and retained?
- **Audit / Pass Criteria** — would the described method pass the audit test?
- **Non-Compliance Triggers** — does the described method match any trigger?

Also apply the CMS automation rules where relevant: unique IDs, mandatory evidence
before closure, approval roles, segregation of duties, escalation, and audit trail.

### Step 4 — Produce the verdict

Use exactly this format:

```
VERDICT: COMPLIANT | NON-COMPLIANT | NEEDS MORE INFORMATION

If COMPLIANT:
  Based on: <requirement name(s)> — the method meets the minimum requirements,
  produces required evidence, and passes audit criteria.

If NON-COMPLIANT (for each breached requirement):
  Requirement: <name> (Domain: <domain>)
  What Is Non-Compliant: <the specific behavior/gap>
  Minimum Requirement Violated: <field from workbook>
  Evidence Missing: <what evidence is not produced/retained>
  Pass Criteria Failed: <the audit criterion not met>
  Non-Compliance Trigger Matched: <the trigger that applies>

If NEEDS MORE INFORMATION:
  Missing: <what info is needed to judge>
  Ask: <specific questions to the user>
```

### Step 5 — Advise remediation (when non-compliant)

For each breach, recommend corrective action: what to change in the working method,
what evidence to start producing, who should own the fix (refer to the Indicative
Process Owner), and how to re-verify compliance.

## Rules of the Check

- **Judge on evidence and controls, not intention.** A good-faith effort without
  required evidence or controls is still non-compliant.
- **Scope matters.** Only judge against requirements that apply to the described role,
  SBU, factory, or activity. Requirements marked "Only the SBU or activity named" are
  not group-wide by default.
- **Minimum requirements are mandatory.** Missing any minimum requirement = non-compliant.
- **When in doubt, ask.** If the description is insufficient to evaluate a requirement,
  mark NEEDS MORE INFORMATION rather than guessing.
- **Be specific.** Never answer "non-compliant" without naming the exact requirement(s)
  and the specific reason.

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

- The index CSV contains only name, domain, category, applicability, and owner — pull
  full detail from the source workbook before issuing a verdict.
- Confirm applicability before judging; "Only the SBU or activity named" is not
  group-wide by default.
- Confirm process owners with the organization; the workbook provides indicative owners.
- Always answer with a clear verdict and, for non-compliance, the specific how and why.
