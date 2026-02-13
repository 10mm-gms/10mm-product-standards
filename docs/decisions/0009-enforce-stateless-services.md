# 9. Enforce Stateless Services

Date: 2025-12-21

## Status

Accepted

## Context

We require High Availability (HA). This means no single point of failure and the ability to handle traffic spikes by adding more servers.
If a server holds state (e.g., "User 123 is logged in on Server A" via in-memory sessions), we cannot simply route that user's next request to Server B without complex sticky sessions.

## Decision

All application services must be **Stateless**.

*   **No Local State**: No data required for a request shall persist in the application process memory or local filesystem after the request completes.
*   **External State**: All state must be stored in backing services:
    *   **Database**: PostgreSQL for persistent data.
    *   **Cache/Session**: Redis for ephemeral data (session stores, rate limits).
    *   **Object Storage**: S3/GCS for file uploads.

## Consequences

*   **Positive**: **Trivial Horizontal Scaling**. We can spin up 1 or 100 instances behind a Load Balancer and round-robin traffic.
*   **Positive**: Zero-downtime deployments (rolling updates) are easy.
*   **Negative**: Requires external infrastructure (Redis) even for simple apps.
