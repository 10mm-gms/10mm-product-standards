# Infrastructure Overview

This document outlines the runtime environment expectations for our product suite.

## Philosophy
We treat infrastructure as **Ephemeral** and **Declarative**.

## Principles

### 1. Containerization
All applications are packaged as **OCI Containers** (Docker images).
*   **Base Images**: distroless or alpine (minimal surface area).
*   **Artifacts**: The build output is a Docker image, not a jar/executable.

### 2. Configuration
*   **Environment Variables**: All config (DB URLs, API Keys) is injected via ENV vars.
*   **Mandatory Validation**: Applications MUST validate critical environment variables on startup. The application should "fail fast" and refuse to start if mandatory configuration is missing or malformed.
*   **Secrets**: Secrets are mounted or injected at runtime; never baked into the image.

### 3. Orchestration
We assume a container orchestrator (Kubernetes / ECS / Cloud Run).
*   **Health Checks**: Apps must expose `/healthz` and `/readyz`.
*   **Graceful Shutdown**: Apps must handle `SIGTERM` to finish in-flight requests before exiting.

### 4. Observability Patterns
We use two distinct patterns to keep our apps "dumb" regarding infrastructure:

*   **Node Agents (For Logs & Metrics)**:
    *   A single agent runs on each server (Node). It collects logs from *all* containers running on that node by reading the underlying Docker log files.
    *   *Why*: Efficient. One agent process per 50 apps.
*   **Sidecars (For Tracing/Proxying)**:
    *   A specialized container running inside the *same pod* as your app. It shares the network interface (localhost).
    *   *Why*: Used for things that need tight coupling, like collecting traces (OTEL Collector) or handling mTLS encryption (Service Mesh).
