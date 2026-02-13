# 11. Observability Strategy

Date: 2025-12-21

## Status

Accepted

## Context

We need to monitor our applications in production.
Using client libraries to ship logs (e.g., `datadog-py`, `winston-cloudwatch`) couples the application code to a specific vendor and increases latency/complexity within the app process.

## Decision

We will follow the **12-Factor App** methodology for observability.

### 1. Logs (Streams not Files)
*   **Mechanism**: Applications must write purely to `stdout` (for info) and `stderr` (for errors).
*   **Format**: Structured JSON.
*   **Shipping**: We rely on the **Node Agent** pattern.
    *   **Explanation**: The application writes to `stdout`. The container runtime (Docker/Containerd) captures this output and writes it to a file on the *host machine*. A specialized "Node Agent" (e.g., Datadog Agent, Fluentd) running on that same host reads these files and ships them to the cloud.
    *   **Benefit**: The app container remains completely isolated and doesn't need to know how or where logs are sent.
*   **Banned**: Writing to local log files (e.g., `/var/log/app.log`) or managing log rotation within the app.
*   **Logging Rules**:
    1.  **No Print Statements**: Never use `print()` or `console.log()` in production code. Use the logger.
    2.  **Context**: Include context in log messages (e.g., `logger.info("User logged in", extra={"user_id": 123})`).
    3.  **Centralised Configuration**: Logging MUST be configured in a single entry point (e.g., `core/logging_config.py`). Domain models and business logic should never call `basicConfig`.
    4.  **Granular Level Control**: Use a `LOG_LEVEL` environment variable (`DEBUG`, `INFO`, `WARN`, `ERROR`) to control verbosity.
    5.  **Noisy Logger Management**: Applications SHOULD maintain an explicit list of noisy third-party dependency loggers (e.g., `sqlalchemy.engine`, `httpx`). These should be silenced (to `WARNING`) by default and only elevated to `DEBUG` when `LOG_LEVEL=DEBUG` is explicitly set.

### 2. Metrics (Pull not Push)
*   **Mechanism**: Applications must expose a `/metrics` HTTP endpoint.
*   **Format**: Prometheus text format.
*   **Collection**: The monitoring agent (Prometheus/Datadog Agent) scrapes this endpoint periodically.
*   **Why Pull?**: In a "Push" model, the app must know *where* to send metrics (coupling). In a "Pull" model, the app just exposes its state, and the infrastructure decides when/how to collect it. This prevents the app from being overwhelmed by reporting duties.

### 3. Tracing
*   **Standard**: OpenTelemetry (OTEL).
*   **Mechanism**: Auto-instrumentation where possible. Traces are sent to a local OTEL collector agent (sidecar), not directly to the backend over the WAN.
*   **Explanation**: "Auto-instrumentation" means the OTEL agent attaches to the running process (like a debugger) and captures HTTP/DB calls automatically, without the developer writing code to "start span" or "end span".

## Consequences

*   **Positive**: **Vendor Neutrality**. We can switch from Datadog to CloudWatch by changing the infra agent, without touching app code.
*   **Positive**: **Cloud-Native Compatibility**. Platforms like **Google Cloud Run** and **AWS Fargate** handle this natively:
    *   They automatically capture `stdout` logs (no agent needed).
    *   They have managed services for Prometheus scraping and OTel ingestion.
    *   This means "Day 1" deployment requires ZERO infrastructure setup for users on these platforms.
*   **Positive**: **Performance**. App only writes to memory buffer (stdout), not network sockets.
*   **Negative**: Developers must rely on `docker logs` or the centralized dashboard, as there are no local log files to `tail`.
