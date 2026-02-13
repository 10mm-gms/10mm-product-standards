# Product Requirements Standards

## Overview
This document defines how we strictly define product requirements before implementation. Just as we use the 12-Factor App for engineering, we use the **10-Factor Requirement** for product definition to ensure clarity, value, and feasibility.

## The 10-Factor Requirement

1.  **Problem-First**: Always start with the user problem or business need, never the solution. "Why are we doing this?" must be answered first.
2.  **Targeted Persona**: Explicitly identify *who* benefits. Generic "users" are not allowed; use specific personas or roles.
3.  **Value Hypothesis**: State the expected outcome. "If we build X, then Y will happen for persona Z."
4.  **Success Metrics**: Define how success is measured (KPIs). If you can't measure it, you can't manage it.
5.  **Anti-Scope**: Explicitly define what is *not* being built. Scope creep is the enemy; boundaries must be set.
6.  **Visualized**: A picture is worth a thousand lines of text. Wireframes, sketches, or user flows are mandatory for UI features.
7.  **Technical Feasibility**: Engineering *must* review and identify architectural impact (migrations, new services, etc.) before approval.
8.  **Dependencies**: Identification of other teams, APIs, or blockers that must be resolved.
9.  **Acceptance Criteria**: Verifiable, binary (pass/fail) conditions that define "Done". For behavioral changes, these **must** be defined using Gherkin syntax (Given/When/Then).
10. **Living Status**: The requirement document is the source of truth. It must be updated if things change during implementation.

## Implementation
Every significant feature, epic, or product initiative must have a corresponding "Product Requirement Document" (PRD) or "Shape" (Basecamp style) that adheres to these 10 factors. **Individual user stories are typically grouped within the PRD of the feature they belong to**, rather than each having their own document. See `blueprints/prd.md` for the standard template.

> [!IMPORTANT]
> **Scenarios Before Code**: Behavioral specifications (Gherkin) **must** be written and approved in the PRD *before* any backend/frontend code or E2E tests are implemented. This ensures the specification is the objective source of truth and drives development.

## Review Process
1.  **Draft**: PM/Author creates the draft covering factors 1-6.
2.  **Feasibility**: Engineering reviews for factors 7-8.
3.  **Refinement**: Acceptance criteria (9) are agreed upon.
4.  **Approval**: Stakeholders sign off.
