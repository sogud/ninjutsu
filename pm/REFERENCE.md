# PM Skill Reference

Detailed PMP-style templates for software engineering projects. Copy only the sections needed for the user's request.

## 0. Software PM judgment model

A software PM is not only a scheduler. The core job is to keep software delivery controlled under uncertainty.

Always start by answering:

```markdown
## Project judgment
- Status: Green / Amber / Red
- Confidence: High / Medium / Low
- Evidence:
- Root blocker:
- Decision needed:
- Next 24–48h action:
```

Use the PMP scenario loop:
1. Understand facts before acting.
2. Check plan, baseline, policy, contract, or working agreement.
3. Analyze impact on scope, schedule, cost, quality, risk, stakeholders, and business value.
4. Engage the right people: team first when possible, sponsor/change authority when required.
5. Use formal change control or escalation when commitments change or authority is exceeded.
6. Document decision, owner, due date, and follow-up.

Software PM control loop:
- Outcome: business value and measurable success.
- Scope: PRD, non-goals, acceptance criteria.
- Delivery: milestones, sprint/release plan, owners.
- Engineering: architecture, API, data, infra, security, QA, observability.
- Governance: RAID, change control, launch readiness, stakeholder communication.

## 1. Project intake template

```markdown
# Project Intake

## Objective
- Desired outcome:
- Business value:
- Success metrics:

## Context
- Sponsor:
- Decision owner:
- Users / impacted groups:
- Delivery team:
- Current phase:

## Constraints
- Deadline / launch window:
- Budget:
- Resources:
- Compliance / legal / security:
- Technical constraints:

## Software context
- Product / PRD link:
- Affected systems / repos:
- Frontend / backend / client / data / infra scope:
- API contracts:
- Data migration:
- Release path:
- Monitoring / rollback needs:

## Known facts
- Fact 1:

## Assumptions
- Assumption 1:

## Open questions
- Question 1:
```

## 2. Project charter template

```markdown
# Project Charter

## Executive summary
One paragraph: why this project exists, what it will deliver, and how success is measured.

## Goals and success metrics
| Goal | Metric | Target | Measurement owner |
|------|--------|--------|-------------------|
| TBD | TBD | TBD | TBD |

## Scope
### In scope
- TBD

### Out of scope
- TBD

## Stakeholders
| Role | Name | Responsibility | Engagement need |
|------|------|----------------|-----------------|
| Sponsor | TBD | Approves funding and priority | Weekly summary |
| Accountable owner | TBD | Final delivery accountability | Decision reviews |

## Milestones
| Milestone | Target date | Owner | Exit criteria |
|-----------|-------------|-------|---------------|
| Kickoff | TBD | TBD | Charter approved |

## Constraints and assumptions
- Constraint: TBD
- Assumption: TBD

## Initial risks
| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| TBD | M | H | TBD | TBD |

## Approval
- Sponsor approval:
- Date:
```

## 2.5 PRD-to-engineering plan

```markdown
# PRD-to-Engineering Plan

## Business outcome
- Outcome:
- Success metric:
- User impact:

## Scope translation
| PRD requirement | Engineering deliverable | Owner | Acceptance criteria | Notes |
|-----------------|-------------------------|-------|---------------------|-------|
| TBD | TBD | TBD | TBD | TBD |

## Technical workstreams
| Workstream | Scope | DRI | Dependencies | Exit criteria |
|------------|-------|-----|--------------|---------------|
| Product / requirements | TBD | TBD | TBD | PRD signed off |
| Design / UX | TBD | TBD | TBD | UX accepted |
| Frontend / client | TBD | TBD | TBD | Feature complete |
| Backend / API | TBD | TBD | TBD | API contract stable |
| Data / migration | TBD | TBD | TBD | Migration rehearsed |
| QA / automation | TBD | TBD | TBD | Regression passed |
| Security / compliance | TBD | TBD | TBD | Review passed |
| Release / ops | TBD | TBD | TBD | Rollback ready |

## Milestones
| Milestone | Date | Owner | Exit criteria | Confidence |
|-----------|------|-------|---------------|------------|
| PRD freeze | TBD | TBD | Scope/non-goals accepted | M |
| Tech design review | TBD | TBD | Architecture/API/data risks closed | M |
| Feature complete | TBD | TBD | Code merged behind flag | M |
| Test complete | TBD | TBD | Critical defects = 0 | M |
| Launch | TBD | TBD | Monitoring and rollback ready | M |

## Open decisions
| Decision | Owner | Due | Impact if delayed |
|----------|-------|-----|-------------------|
| TBD | TBD | TBD | TBD |
```

## 3. WBS / backlog planning

Use WBS for predictive delivery; use backlog for agile delivery; use both for hybrid delivery.

```markdown
| ID | Deliverable / Epic | Work package / Story | Owner | Dependency | Acceptance criteria | Due |
|----|--------------------|----------------------|-------|------------|---------------------|-----|
| 1.0 | TBD | TBD | TBD | TBD | TBD | TBD |
```

Check each item:
- Has one accountable owner.
- Produces a verifiable output.
- Has acceptance criteria.
- Has dependencies visible.
- Is small enough to track within one reporting cycle.

## 4. RACI template

```markdown
| Deliverable / Decision | Responsible | Accountable | Consulted | Informed |
|------------------------|-------------|-------------|-----------|----------|
| TBD | TBD | TBD | TBD | TBD |
```

Rules:
- Exactly one `Accountable` per row.
- `Responsible` can be multiple people, but avoid crowds.
- If everyone is consulted, no one is truly consulted. Name the critical voices.
- Convert repeated RACI conflicts into decision-rights escalation.

## 5. RAID log template

```markdown
| Type | Item | Impact | Probability | Severity | Owner | Due | Response | Status |
|------|------|--------|-------------|----------|-------|-----|----------|--------|
| Risk | TBD | H | M | H | TBD | TBD | Mitigate | Open |
| Assumption | TBD | M | M | M | TBD | TBD | Validate | Open |
| Issue | TBD | H | N/A | H | TBD | TBD | Resolve | Open |
| Dependency | TBD | H | M | H | TBD | TBD | Track | Open |
```

Severity guide:
- `High`: threatens committed date, budget, customer promise, compliance, or executive trust.
- `Medium`: affects team efficiency, quality, or one milestone but has workaround.
- `Low`: monitor only; no immediate management action.

Risk responses:
- Avoid: change plan to remove risk.
- Mitigate: reduce probability or impact.
- Transfer: move ownership or financial exposure.
- Accept: acknowledge and monitor.
- Escalate: outside project team's authority.

### Software RAID examples

| Type | Example | Typical response |
|------|---------|------------------|
| Risk | API provider may miss contract freeze | Escalate owner/date, define mock/fallback, protect integration window |
| Risk | Data migration may exceed downtime window | Rehearse migration, split batches, prepare rollback |
| Risk | Performance target unknown | Define SLO, run load test before launch gate |
| Assumption | Existing auth service supports new role model | Validate with owner before design freeze |
| Issue | CI pipeline failing intermittently | Assign DRI, block release if reproducibility risk remains |
| Dependency | Security review required before external launch | Book reviewer, set due date, track as launch gate |

## 6. Status report templates

### Executive status

```markdown
# Project Status — <Project Name>

Overall: Green / Amber / Red
Date: YYYY-MM-DD
Owner: TBD

## Executive summary
One paragraph with status, confidence, and the most important ask.

## Progress
| Area | Plan | Actual | Status | Note |
|------|------|--------|--------|------|
| Scope | TBD | TBD | G/A/R | TBD |
| Schedule | TBD | TBD | G/A/R | TBD |
| Cost / resources | TBD | TBD | G/A/R | TBD |
| Quality | TBD | TBD | G/A/R | TBD |
| Risk | TBD | TBD | G/A/R | TBD |

## Key accomplishments
- TBD

## Next milestones
| Milestone | Date | Owner | Confidence |
|-----------|------|-------|------------|
| TBD | TBD | TBD | H/M/L |

## Decisions / escalations needed
| Need | Owner | Due | Impact if delayed |
|------|-------|-----|-------------------|
| TBD | TBD | TBD | TBD |

## Top risks / issues
| Item | Impact | Owner | Response | Due |
|------|--------|-------|----------|-----|
| TBD | TBD | TBD | TBD | TBD |
```

### Team standup / delivery update

```markdown
## Since last update
- Done:
- Learned:

## Now
- In progress:
- Blocked:

## Next
- Next 24–48h:
- Help needed:
```

## 7. Change control template

```markdown
# Change Request

## Requested change
- Change:
- Requestor:
- Date:

## Rationale
- Why now:
- Business value:

## Impact analysis
| Dimension | Impact | Evidence |
|-----------|--------|----------|
| Scope | TBD | TBD |
| Schedule | TBD | TBD |
| Cost / resources | TBD | TBD |
| Quality | TBD | TBD |
| Risk | TBD | TBD |
| Stakeholders | TBD | TBD |

## Options
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| Accept | TBD | TBD | TBD |
| Reject | TBD | TBD | TBD |
| Defer | TBD | TBD | TBD |

## Decision
- Decision:
- Decision owner:
- Date:
- Follow-up actions:
```

## 8. Troubled project recovery playbook

Use when the project is late, blocked, politically sensitive, over budget, or losing stakeholder trust.

### First 30 minutes
1. State current status: objective, committed date, actual progress, known blockers.
2. Separate symptoms from causes.
3. Identify critical path and irreversible dates.
4. Freeze uncontrolled scope changes until decision owner reviews impact.
5. Create a single RAID log if none exists.

### First 24 hours
1. Validate top 3 risks/issues with owners.
2. Rebuild a milestone plan from now to next externally visible commitment.
3. Identify options:
   - Reduce scope.
   - Add resources.
   - Move date.
   - Lower quality bar knowingly.
   - Split release.
4. Prepare sponsor decision memo with impact and recommendation.

### First 48 hours
1. Hold recovery meeting with sponsor and accountable owners.
2. Decide trade-off explicitly.
3. Re-baseline schedule/scope.
4. Communicate new plan, owners, and escalation cadence.
5. Track daily until the project returns to Green/Amber.

## 9. Meeting templates

### Steering committee agenda

```markdown
# Steering Committee

## Purpose
Decision / alignment / escalation.

## Agenda
1. Current status and confidence.
2. Progress against last commitments.
3. Top risks and issues.
4. Decisions needed.
5. Next milestone and asks.

## Pre-read
- Status report:
- RAID log:
- Change requests:
```

### Minutes

```markdown
# Meeting Minutes

Date:
Attendees:

## Decisions
| Decision | Owner | Date | Rationale |
|----------|-------|------|-----------|
| TBD | TBD | TBD | TBD |

## Actions
| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| TBD | TBD | TBD | Open |

## Risks / issues raised
| Item | Owner | Next step |
|------|-------|-----------|
| TBD | TBD | TBD |
```

## 10. Quality gate checklist

Before declaring a milestone complete:
- Deliverable matches agreed scope.
- Acceptance criteria are verified.
- Defects, exceptions, and waivers are documented.
- Required stakeholders accepted or signed off.
- Operational handover is ready.
- Support, monitoring, and rollback paths are known.
- Open risks/issues have owners and dates.

### Software release readiness checklist

```markdown
# Release Readiness

## Scope and product
- PRD scope locked or approved changes documented.
- Non-goals are explicit.
- Acceptance criteria verified.
- User-facing communication prepared.

## Engineering
- Tech design reviewed.
- API contracts stable.
- Database/data migration rehearsed where applicable.
- Code merged and reviewed.
- Feature flag / gray release / rollback path ready.

## Quality
- Test plan complete.
- Regression passed.
- Critical defects = 0 or explicitly waived by decision owner.
- Performance/security/privacy gates passed.

## Operations
- Monitoring and alerts configured.
- On-call / support owner assigned.
- Runbook ready.
- Incident escalation path known.

## Launch decision
- Go / No-Go:
- Decision owner:
- Launch time:
- Rollback owner:
```

## 11. Communication principles

- Sponsor communication: concise, decision-oriented, risk-aware.
- Delivery-team communication: concrete tasks, blockers, dependencies, dates.
- Customer/user communication: value, impact, timing, behavior changes.
- Bad news: early, factual, options-based, with a recommended path.
- Good news: connect progress to business outcome, not activity volume.
