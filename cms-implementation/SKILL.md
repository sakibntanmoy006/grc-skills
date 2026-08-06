---
name: cms-implementation
description: Audit, design, implement, and improve an enterprise Compliance Management System (CMS) using ISO 37301 and supporting governance, integrity, risk, legal, regulatory, ESG, buyer-code, and industry requirements. Use whenever the user invokes $cms, asks whether an activity, process, document, control, SBU, site, system, or proposed action is compliant, asks Codex to perform work that should first be checked against the CMS, requests a compliance audit or gap assessment, needs corrective actions for failed compliance, or needs CMS architecture, obligations, risks, controls, evidence, CAPA, monitoring, dashboards, or certification readiness.
---

# CMS — Compliance Management System

## Overview

This skill codifies the design and delivery of a certifiable enterprise Compliance
Management System (CMS). It follows ISO 37301:2021 (with Amendment 1:2024) as the
primary framework, ISO 37302:2025 for effectiveness evaluation, and ISO 37303:2025 for
compliance-role competency, supported by the ISO 37000/37001/37002/37003 family, ISO
31000, COSO ERM, the IIA Three Lines Model, G20/OECD Corporate Governance Principles,
and the U.S. DOJ compliance-program benchmark.

The operational target is a single connected compliance data chain, automated through
an I-BOS-style system, delivered via a PDCA-based 15-day Minimum Viable launch with a
structured 90-day completion phase.

## Audit-First Operating Rule

Treat every invocation as an audit gate before giving a compliance conclusion or
implementing a CMS-sensitive request.

1. Define what is being assessed: entity, SBU, site, process, product, document,
   transaction, system, proposed action, jurisdiction, and period.
2. Select the applicable requirements from laws, regulations, licences, permits,
   contracts, buyer codes, standards, internal policies, and the compliance universe.
3. Ask for or inspect objective evidence. Never treat a policy, assertion, or template
   alone as proof that a control operates effectively.
4. Test both control design and operating effectiveness.
5. Classify every applicable requirement and calculate the overall conclusion using the
   decision rules below.
6. If a requirement fails, identify containment, root cause, corrective action,
   preventive action, owner, target date, closure evidence, escalation, and retest.
7. Proceed with the requested work only in a way that preserves the CMS. Do not implement
   a design that bypasses a mandatory control or leaves a critical compliance failure
   unaddressed.

Read [references/audit-methodology.md](references/audit-methodology.md) for the full
testing, evidence, decision, and remediation method whenever performing an audit,
compliance check, or gap assessment.

Inspect [assets/Enterprise_Compliance_Universe.xlsx](assets/Enterprise_Compliance_Universe.xlsx)
with spreadsheet tools when the assessment spans multiple domains, Bangladesh legal or
regulatory sources, global standards, buyer requirements, or an SBU-wide compliance
universe. Use it as a source catalogue; Legal must still validate applicability and the
current version of external requirements.

## Mandatory Decision States

Use only these overall states:

- **COMPLIANT** — all applicable requirements tested are satisfied; controls are suitably
  designed and operating effectively; required evidence is current and sufficient; no
  unresolved critical/high failure prevents compliance.
- **PARTIALLY COMPLIANT** — requirements are partly satisfied, but non-critical gaps or
  incomplete operating effectiveness require remediation.
- **NON-COMPLIANT** — a mandatory requirement failed, a critical/high control is absent
  or ineffective, a licence/permit/filing is expired or overdue, or evidence proves a
  breach.
- **NOT DEMONSTRATED — EVIDENCE REQUIRED** — scope, criteria, or objective evidence is
  insufficient. Never use COMPLIANT when evidence is missing.
- **NOT APPLICABLE** — a documented and approved applicability assessment demonstrates
  that the requirement does not apply.

Overall conclusion rules:

- Any critical or high non-compliance makes the overall conclusion NON-COMPLIANT.
- Any untested mandatory requirement or missing material evidence prevents COMPLIANT.
- PARTIALLY COMPLIANT is permitted only when remaining gaps are not critical/high and do
  not constitute a legal, regulatory, licence, permit, contractual, or buyer-code breach.
- COMPLIANT is permitted only after every in-scope applicable criterion passes.
- NOT APPLICABLE requires a documented rationale and Legal approval for legal or
  regulatory interpretations.

## Required Audit Response

Lead with exactly one outcome line:

`COMPLIANT — <scope and basis>`

`PARTIALLY COMPLIANT — <scope and main gaps>`

`NON-COMPLIANT — <scope and decisive failures>`

`NOT DEMONSTRATED — EVIDENCE REQUIRED — <missing scope/evidence>`

Then provide:

1. Scope and criteria used.
2. Evidence reviewed and evidence missing.
3. Requirement-level findings: requirement/source, applicability, expected control,
   evidence, design result, operating result, status, risk, and rationale.
4. Overall conclusion and decisive reasons.
5. For every failed or partial item, a prioritized remediation/CAPA plan with owner,
   due date, closure evidence, and retest method.
6. If compliant, state which evidence and tests support the conclusion and the next
   monitoring or review date.

Do not claim certification, legal assurance, or universal compliance from a limited
review. State the actual scope and level of assurance.

## When to Apply

- Planning or implementing a Compliance Management System or GRC Management System.
- Building or updating a compliance universe, obligation register, or risk-control matrix.
- Designing or configuring automated compliance workflows (obligations, calendar,
  evidence, escalation, third-party due diligence, investigations, CAPA).
- Running or reviewing a 15-day CMS launch roadmap.
- Defining compliance KPIs/KRIs and dashboards.
- Preparing for ISO 37301 gap assessment or certification readiness.

## Core Principles

1. **Audit before action** — identify criteria, evidence, control design, and operating
   effectiveness before concluding or implementing CMS-sensitive work.
2. **Frameworks first** — anchor to ISO 37301 as the certifiable baseline and the
   supporting integrity standards for specific domains.
3. **One connected data chain** — every element links from source to outcome:
   Compliance Universe → Obligation → Risk → Control → Owner → Due Date → Evidence →
   Testing → Finding/Case → CAPA → Management Review.
4. **Automation is non-negotiable** — key controls are enforced by the system, not by
   manual discipline.
5. **DoJ benchmark** — the system must be well designed, adequately empowered and
   resourced, and demonstrably effective in practice, using risk assessment, data
   analytics, confidential reporting, investigation, periodic testing, root-cause
   analysis, and remediation.
6. **Minimum Viable then complete** — 15 days launches the automation; 90 days completes
   the population and prepares for certification.

## Reference Frameworks

| Domain | Standard / Framework |
|---|---|
| CMS (certifiable) | ISO 37301:2021 + Amendment 1:2024 |
| Effectiveness evaluation | ISO 37302:2025 |
| Compliance-role competency | ISO 37303:2025 |
| Anti-bribery | ISO 37001:2025 |
| Whistleblowing | ISO 37002:2021 |
| Fraud control | ISO 37003:2025 |
| Governance / risk / assurance | ISO 37000, ISO 31000, COSO ERM & Compliance Risk Mgmt, IIA Three Lines Model, G20/OECD Principles of Corporate Governance 2023 |
| Program benchmark | U.S. DOJ Compliance Program (well designed, empowered/resourced, demonstrably effective) |

Always confirm which standards are in scope for the organization before assuming
requirements.

## Enterprise CMS Architecture (I-BOS Modules)

| Module | Main purpose |
|---|---|
| Compliance Universe | Define all legal, regulatory, contractual, licence, ESG, buyer-code and internal requirements |
| Obligation Register | Record applicability, owner, frequency, due date, evidence and source |
| Compliance Risk Register | Assess likelihood, impact, inherent risk and residual risk |
| Control Library | Define preventive, detective and corrective controls |
| Compliance Calendar | Generate recurring tasks, reminders and overdue escalation |
| Evidence and DMS Link | Prevent task closure without valid supporting evidence |
| Third-Party Due Diligence | Screen suppliers, agents, contractors, dealers and consultants |
| Ethics and Declaration | Manage conflicts of interest, gifts, hospitality and compliance declarations |
| Speak-Up and Investigation | Protect confidentiality and manage investigation lifecycle |
| Monitoring and Testing | Test whether controls are designed and operating effectively |
| CAPA | Manage root cause, corrective action, preventive action and verification |
| Dashboard | Provide Group, SBU, factory and process-level compliance reporting |

## PDCA-Based 15-Day Roadmap

### PLAN — Days 1–6

| Day | Key activity | Main output |
|---|---|---|
| 1 | Confirm enterprise scope, SBUs, factories, sites, priority domains and sponsorship | Approved CMS project charter |
| 2 | Establish governance, committee, Three Lines responsibilities, RACI and escalation authority | CMS governance structure |
| 3 | Develop enterprise compliance universe | Group-wide compliance domain map |
| 4 | Design obligation taxonomy and load priority obligations, permits and filings | Priority obligation register |
| 5 | Approve 5×5 compliance-risk assessment methodology | Compliance risk register |
| 6 | Develop common control library and map obligations, risks, controls and evidence | Risk-control matrix |

### DO — Days 7–12

| Day | Key activity | Main output |
|---|---|---|
| 7 | Configure I-BOS master data, roles, access, unique IDs and segregation of duties | CMS data model and access matrix |
| 8 | Configure new/changed obligation validation and approval workflow | Obligation lifecycle workflow |
| 9 | Configure calendar, recurring tasks, evidence, reminders and escalation | Automated compliance calendar |
| 10 | Configure third-party DD, COI, gifts, hospitality and declaration workflows | Integrity workflow package |
| 11 | Configure confidential case, investigation, root-cause and CAPA workflows | Case and CAPA module |
| 12 | Establish compliance training matrix, champions and policy acknowledgements | Competence and communication plan |

### CHECK — Days 13–14

| Day | Key activity | Main output |
|---|---|---|
| 13 | Develop KPI/KRI dashboard, monitoring plan and management-review reporting | CMS dashboard and testing plan |
| 14 | Conduct end-to-end UAT using obligation, overdue task, vendor and investigation scenarios | Signed UAT and readiness checklist |

### ACT — Day 15

| Day | Key activity | Main output |
|---|---|---|
| 15 | Leadership management review, go-live decision, ownership transfer and 30/60/90-day planning | Controlled go-live approval |

## Mandatory Automation Controls (Non-Negotiable)

- Every obligation, risk, control, case and CAPA must have a unique ID.
- Legal interpretations and applicability decisions require Legal approval.
- High-risk activities must have separate maker, reviewer and approver roles.
- Tasks cannot be closed without mandatory evidence.
- Critical obligations should have 90/60/30/15/7/1-day reminders where relevant.
- Overdue critical matters must escalate from owner → functional head → SBU head →
  Group leadership.
- High-risk vendors should not be activated before due-diligence approval.
- Investigation records must use restricted, need-to-know access.
- CAPA closure must require independent effectiveness verification.
- All changes, approvals, evidence and status updates must remain in the audit trail.

## Initial Performance Indicators (Dashboard)

At minimum, report:

1. Total, overdue and upcoming obligations.
2. Critical and high residual compliance risks.
3. Controls that are ineffective, weak or untested.
4. Licence and permit expiry exposure.
5. Open and overdue investigations.
6. CAPA ageing and effectiveness.
7. High-risk third-party due-diligence status.
8. Regulatory changes awaiting implementation.
9. Compliance training completion and assessment results.
10. Compliance monitoring and audit pass rate.
11. SBU and factory-level compliance scores.
12. I-BOS workflow implementation progress.

## Implementation Position

The 15-day programme is a **Minimum Viable Enterprise CMS automation launch** — not
completion of the entire legal register or ISO 37301 certification.

Use the following **90 days** to:

- Populate all applicable entities, factories, licences and legal obligations.
- Validate obligation ownership with Legal and SBU management.
- Complete critical/high-risk control testing.
- Integrate relevant ERP, HRIS, procurement, finance, HSE, DMS and LMS data.
- Conduct internal audit and formal management review.
- Prepare for ISO 37301 gap assessment or certification readiness.

## Workflow

### Plan a CMS

1. Confirm scope (SBUs, factories, sites, priority domains) and sponsorship.
2. Establish governance: committee, Three Lines responsibilities, RACI, escalation.
3. Develop the compliance universe and obligation taxonomy.
4. Load priority obligations; approve risk-assessment methodology (e.g., 5×5).
5. Build the control library and risk-control matrix.
6. Produce a roadmap with milestones, owners, and approval gates.

### Automate (configure the system)

1. Configure master data, roles, access, unique IDs, and segregation of duties.
2. Build obligation validation/approval lifecycle workflow.
3. Configure calendar, recurring tasks, evidence requirements, reminders, escalation.
4. Configure integrity workflows (third-party DD, COI, gifts, hospitality, declarations).
5. Configure confidential case, investigation, root-cause, and CAPA workflows.
6. Enable audit trail on all changes, approvals, evidence, and status updates.

### Monitor and test

1. Define KPIs/KRIs and the monitoring/testing plan.
2. Test whether controls are designed and operating effectively.
3. Review dashboards for overdue obligations, residual risks, ineffective controls,
   licence expiries, investigations, CAPA ageing, and training completion.
4. Escalate overdue critical matters up the defined chain.

### Review and improve

1. Run end-to-end UAT and obtain signed readiness checklist.
2. Conduct leadership management review and controlled go-live decision.
3. Plan 30/60/90-day completion activities.
4. Prepare gap assessment / certification readiness against ISO 37301.

## Deliverables

Typical outputs produced under this skill:

- CMS project charter and governance structure (RACI, escalation authority)
- Compliance universe and obligation register
- Compliance risk register (5×5 likelihood/impact, inherent/residual risk)
- Risk-control matrix (obligations, risks, controls, evidence)
- I-BOS workflow blueprint and access matrix
- Compliance calendar and escalation rules
- KPI/KRI dashboard and monitoring/testing plan
- Signed UAT and go-live approval records
- 30/60/90-day completion and certification-readiness plan

## Reminders

- Confirm scope and applicable standards before assuming requirements.
- Keep the connected data chain intact; each element must trace to source and outcome.
- Treat the listed automation controls as non-negotiable, system-enforced rules.
- Keep one source of truth and a complete, auditable audit trail.
- The 15-day launch is a Minimum Viable automation launch, not full certification.
