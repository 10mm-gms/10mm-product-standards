# 14. Logging Implementation & Strategies

Date: 2026-01-03

## Status

Accepted

## Context

We need to define specific implementation strategies for logging across different components of our products (Backend, Frontend, Mobile). 

A critical distinction exists between these components:
1.  **Backend Services**: Logs are persistent, stored in central infrastructure, and searchable.
2.  **Client-Side Code**: Logs are ephemeral (session-based), visible only in the user's browser, and not captured by our infrastructure.

Consistent usage of levels and tools is required to ensure observability without compromising security or cluttering infrastructure.

## Decision

### 1. Languages & Libraries

*   **Python (Backend)**:
    *   **Library**: Standard `logging` module combined with `python-json-logger`.
    *   **Strategy**: Initialise a root logger with a JSON formatter in a central `logging_config.py`.
*   **TypeScript/JavaScript (Frontend/Mobile)**:
    *   **Library**: A custom `logger` abstraction (e.g., `src/lib/logger.ts`).
    *   **Strategy**: The abstraction should respect the environment (e.g., only log to console in development).

### 2. Environment Detection

To ensure correct behavior across environments, we standardise how applications identify their current mode:

*   **Python (Backend)**:
    *   **Mechanism**: Use an `ENVIRONMENT` environment variable.
    *   **Values**: `development`, `staging`, `production`.
    *   **Fallback**: Default to `production` if unset for security.
*   **TypeScript (Vite Frontend)**:
    *   **Mechanism**: Use `import.meta.env.PROD` and `import.meta.env.DEV`.
    *   **Mode**: `import.meta.env.MODE` can be used for specific environment names.
*   **Node.js/Next.js (Alternative)**:
    *   **Mechanism**: Use `process.env.NODE_ENV`.

### 3. Component Strategies

*   **Backend (FastAPI/Services)**:
    *   Writes directly to `stdout`/`stderr` in JSON format.
    *   These logs are captured by the container runtime and available in infrastructure logs.
    *   The minimum fields required are `asctime`, `levelname`, `name`, and `message`.
*   **Client-Side (React/Web)**:
    *   **Policy**: Client-side scripts **MUST NOT** write to the browser console in production.
    *   **Reasoning**: Browser console logs are not captured in container logs and are visible to end-users, which can be a security risk.
    *   **Exception**: Critical initialisation or fatal errors may be logged, but the custom logger abstraction should suppress `debug` and `info` levels in production.
    *   **Error Monitoring**: Significant client-side errors should be sent to an error tracking service (e.g., Sentry) via an API, not purely logged to the console.

### 3. Data Scrubbing & Privacy

When using third-party error tracking services (e.g., Sentry), we MUST prevent the transmission of PII (Personally Identifiable Information) or credentials.

*   **Server-Side Scrubbing**: Use the service's built-in data scrubbing rules to strip common sensitive fields (e.g., `password`, `token`, `secret`, `authorization`, `cookie`).
*   **Client-Side Redaction**: Implement a `beforeSend` hook (or equivalent) in the logging SDK to:
    1.  Sanitise URLs (strip sensitive query parameters).
    2.  Redact PII from error messages or breadcrumbs.
    3.  Exclude specific sensitive UI components from "Replay" features if used.
*   **Minimal Exposure**: Only send the minimum context required to fix the bug. Avoid sending the entire application state if it contains sensitive data.

### 4. Logging Levels

We standardise on the following levels:

| Level | Usage | Production Policy |
| :--- | :--- | :--- |
| `DEBUG` | Fine-grained informational events that are most useful to debug an application. | Suppressed by default. |
| `INFO` | High-level non-critical events (e.g., Service Start, Successful Login). | Enabled. |
| `WARNING` | Potentially harmful situations or recovered errors. | Enabled. |
| `ERROR` | Error events that might still allow the application to continue running. | Enabled. |
| `CRITICAL` | Severe error events that will presumably lead the application to abort. | Enabled. |

### 4. Dynamic Log-Level Control

To aid in production troubleshooting, **Server-Side Services** (Backend) **MUST** implement a mechanism to allow runtime modification of the log level without restarting the service.

*   **Mechanism**: An administrative API endpoint (e.g., `/api/admin/logging`).
*   **Method**: `POST` to update, `GET` to check current level.
*   **Security**: This endpoint **MUST** be protected by administrative authentication.
*   **Scope**: This affects the **Service's** root logging level and internal filters.
*   **Client-Side Note**: Dynamic control **DOES NOT** apply to client-side (Frontend) code by default. Client-side logging is static and determined at build-time (see Section 2). Products requiring dynamic client logs must implement a separate runtime check (e.g., via LocalStorage or Feature Flags).

## Consequences

*   **Positive**: Clear distinction between backend (server-side) and frontend (client-side) logging.
*   **Positive**: Ability to troubleshoot production issues in real-time without redeploying code via dynamic levels.
*   **Negative**: Slight overhead in maintaining the logger abstraction on the frontend.
