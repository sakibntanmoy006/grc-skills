---
name: compliance-catalog
description: Enterprise Compliance Management System (CMS) catalog of 584 filterable compliance requirements across 80 domains and 11 categories for a multi-SBU industrial enterprise (AKIJ Resource). Use when building or populating an obligation register, checking which compliance requirements apply to a function or SBU, mapping requirements to domains, identifying process owners or required evidence, creating risk-control matrices, or conducting compliance monitoring, testing, and audits.
license: MIT
metadata:
  author: humaninside
  tags: cms, compliance, obligation-register, risk-control, iso-37301, grc, audit, governance, legal, esg, hse
---

# Compliance Catalog — Enterprise Compliance Requirements

## Overview

This skill provides the structured catalog of an enterprise Compliance Management
System (CMS): **584 filterable compliance requirements** organized across **80 domains**
and **11 categories**, each with minimum compliance requirements, required evidence,
audit/pass criteria, non-compliance triggers, typical applicability/SBU, and an
indicative process owner.

The full index is in `references/requirements-index.csv`
(name, domain, category, applicability, process owner). Use it to look up, filter, and
map requirements into obligation registers, risk-control matrices, and audit plans.

## When to Apply

- Building or populating a CMS obligation register or compliance universe.
- Identifying which compliance requirements apply to a given SBU, factory, or function.
- Looking up required evidence, audit/pass criteria, or non-compliance triggers.
- Assigning process owners and accountability for specific requirements.
- Building a risk-control matrix or compliance risk assessment.
- Planning monitoring, testing, and internal audit coverage.
- Mapping requirements to standards (e.g., ISO 37301, ISO 27001, ISO 42001, ISO 14001,
  ISO 45001) and buyer/customer codes.

## Catalog Structure

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
| Minimum Requirements for Compliance | Minimum controls/actions |
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

## Workflow

### Map requirements to an obligation register

1. Filter `requirements-index.csv` by category, domain, or applicability/SBU.
2. For each requirement, record: name, domain, owner, applicability.
3. Pull minimum requirements, evidence, and pass criteria from the source workbook.
4. Assign owners (default to the Indicative Process Owner unless overridden).
5. Load into the CMS obligation register with due dates and frequencies.

### Determine applicability for an SBU or function

1. Identify the SBU/function/factory/site in scope.
2. Search the index by applicability keywords (e.g., "all factories", "Group-wide",
   "procurement", "all information assets").
3. Cross-reference with the source workbook's "Typical Applicability / SBU" field.
4. Add requirements named to that SBU specifically ("Only the SBU or activity named").
5. Produce the applicable requirement list for that scope.

### Build a risk-control matrix

1. Group requirements by domain.
2. For each requirement, define the risk (what could go wrong).
3. Map the minimum requirements/controls from the workbook.
4. Link the required evidence as the control evidence.
5. Use audit/pass criteria as the testing and monitoring standard.

### Plan monitoring, testing, and audits

1. Prioritize by criticality of domain (Governance/Legal, HSE, Technology/Data first).
2. For each requirement, use "Audit / Pass Criteria" as the test definition.
3. Use "Non-Compliance Triggers" to define findings and escalations.
4. Use "Required Evidence" as the sampling basis.
5. Assign the Indicative Process Owner as the primary auditee/control owner.

### Quick lookups

- **"What evidence does <requirement> need?"** → filter the index to the requirement and
  reference the source workbook's Required Evidence field.
- **"Who owns <domain>?"** → group index by domain and inspect process owners.
- **"Which requirements apply to all factories?"** → filter applicability containing
  "factories" or "sites".
- **"Is <activity> a compliance risk?"** → search the index for the activity keyword.

## Deliverables

- Applicable-requirement registers per SBU/function/site
- Obligation register entries with owner, evidence, and pass criteria
- Risk-control matrices mapped from requirements and controls
- Audit/monitoring plans using pass criteria and non-compliance triggers
- Domain and category coverage analyses

## Reminders

- Always pull the full field detail (evidence, criteria, triggers) from the source
  workbook — the index CSV contains only name, domain, category, applicability, and
  owner.
- Verify applicability before including a requirement; "Only the SBU or activity named"
  means the requirement is not group-wide by default.
- Confirm process owners with the organization; the workbook provides indicative owners.
- Keep one source of truth (the workbook/register) and trace every obligation to its
  requirement and evidence.
