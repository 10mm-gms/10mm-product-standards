# 7. Use Modular Monolith Architecture

Date: 2025-12-21

## Status

Accepted

## Context

We are building a new product suite. We have conflicting requirements:
1.  **MVP Speed**: We need to ship and iterate fast to prove the concept.
2.  **Scalability**: If successful, the system may need to handle high load and be split into teams.

Typical approaches have downsides:
*   **Microservices first**: Accidental complexity, distributed systems fallacies (network latency, consistency), high infra overhead for an unproven product.
*   **Classic Monolith**: "Big ball of mud," tight coupling making future splitting impossible.

## Decision

We will build a **Modular Monolith**.

*   **Single Deployment Unit**: All "services" (Auth, Core, Payments) run within a single FastAPI process (or cluster of identical processes).
*   **Strict Module Boundaries**: Code is organized into modules (e.g., `src/auth`, `src/billing`) that enforce interface boundaries.
    *   Cross-module communication occurs via simple function calls (in-process).
    *   No direct database access across modules (e.g., Billing cannot query Auth tables directly; it must ask the Auth module).
*   **Future-Ready**: Since modules are decoupled, properly bounded contexts are established. Moving `src/billing` to a separate microservice later is a mechanical refactor (replace function call with gRPC/HTTP client), not a rewrite.

## Consequences

*   **Positive**: Zero network latency between components.
*   **Positive**: Simple "one container" deployment.
*   **Positive**: Codebase is structured for scale from Day 1 without the infra tax.
*   **Negative**: Must discipline developers to avoid coupling modules (using linting tools like `import-linter` is recommended).
