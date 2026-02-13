# 1. Record Architecture Decisions

Date: 2025-12-21

## Status

Accepted

## Context

We need a way to record architectural decisions, the context of those decisions, and the consequences of those decisions. This needs to be consistent across all products to ensuring that historical context is preserved and new team members (and AI agents) can understand the "why" behind the system design.

## Decision

We will use **Architecture Decision Records (ADRs)**, as described by Michael Nygard.

*   We will store these decisions in the repository under `docs/decisions`.
*   We will use a lightweight Markdown format.
*   The naming convention will be `NNNN-title-in-kebab-case.md` (e.g., `0001-record-architecture-decisions.md`).
*   ADRs are immutable once accepted (except for Status updates).

## Consequences

*   **Positive**: Clear history of decisions.
*   **Positive**: AI agents can easily ingest this folder to understand constraints.
*   **Negative**: Slight overhead in writing them down, but pays off in clarity.
