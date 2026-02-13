# 17. Standard Environment Variable Naming

Date: 2026-01-26

## Status

Accepted

## Context

As the number of products and services increases, having inconsistent environment variable names across repositories leads to configuration errors, slower onboarding, and complicated deployment scripts. We need a unified naming convention for common infrastructure and application settings.

## Decision

We will standardize on the following environment variable names for all 10mm GMS products:

### Core Infrastructure
*   **`DATABASE_URL`**: The primary data store connection string. For asynchronous Python services, use the appropriate dialect (e.g., `postgresql+asyncpg://...`).
*   **`SECRET_KEY`**: Used for cryptographic signing of session cookies, JWTs, and other security sensitive tokens.
*   **`LOG_LEVEL`**: Used to control logging output (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).

### Authentication & Authorization
*   **`GOOGLE_CLIENT_ID`**: The OAuth 2.0 Client ID for Google integration.
*   **`GOOGLE_CLIENT_SECRET`**: The OAuth 2.0 Client Secret for Google integration.
*   **`GOOGLE_REDIRECT_URI`**: The callback endpoint for OAuth flows.
*   **`ALLOWED_DOMAIN`**: Restriction for corporate domain logins (e.g., `10mm.net`).

### Service Linkage
*   **`FRONTEND_URL`**: The public-facing base URL of the frontend application.
*   **`VITE_API_URL`**: Used by frontend build/runtime to locate the backend API.
*   **`EXTERNAL_SERVICE_URL`** / **`EXTERNAL_SERVICE_KEY`**: Follow the pattern `{SERVICE_NAME}_URL` and `{SERVICE_NAME}_KEY` for third-party integrations (e.g., `ODOO_API_URL`, `STRIPE_KEY`).

### Application State
*   **`ENABLE_FEATURE_NAME`**: Feature flags should follow the `ENABLE_` prefix (e.g., `ENABLE_TEST_BACKDOOR`, `ENABLE_BETA_UI`).

## Consequences

*   **Positive**: Improved portability—`run_docker.sh` and CI/CD templates can be reused across projects.
*   **Positive**: Reduced "magic knowledge" required to configure a new environment.
*   **Neutral**: Existing projects should be migrated to these standards during their next major update or when implementing new features.
*   **Negative**: Slight overhead in renaming variables in legacy systems.
