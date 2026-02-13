# Security Standards

This document defines the **Product Security Baseline** that all applications must meet before going to production.

## 1. Transport Security

### SSL/TLS Termination
As per [ADR-0012](../decisions/0012-app-execution-standards.md), SSL/TLS termination MUST be handled at the **Infrastructure Layer** (e.g., Ingress Controller, Load Balancer, or Cloud Gateway).

1.  **Plain HTTP Internal**: Applications generally receive plain HTTP traffic from the load balancer.
2.  **Trusted Proxies**: Backend frameworks MUST be configured to trust the infrastructure's proxy headers (e.g., `X-Forwarded-Proto`, `X-Forwarded-For`).
    *   *FastAPI Example*: Use `ProxyHeadersMiddleware`.
3.  **HSTS**: The infrastructure layer SHOULD be configured to inject `Strict-Transport-Security` headers for all production domains.
4.  **Encryption in Transit**: TLS 1.2+ everywhere. FORCE_SSL must be enabled at the entry point.

## 2. Authentication & Authorization

### Google OAuth 2.0
We use Google OAuth 2.0 as our primary authentication provider for internal and client applications.

1.  **Mandatory Domain Restriction**: All internal applications MUST enforce a hosted domain (`hd`) check.
    *   Access must be restricted to the `@10mm.com` domain (or a project-specific whitelist).
    *   This check MUST be performed on the backend, not solely on the frontend.
2.  **Scopes**: Only request the minimum required scopes (e.g., `openid`, `email`, `profile`).
3.  **Protocol**: **OAuth 2.0 / OIDC** is the standard. Avoid custom auth schemes.

### RBAC
Implement **Role-Based Access Control** at the API Gateway or Middleware level.
- API endpoints must explicitly declare required roles (e.g., `@requires_role("admin")`).

## 3. Session Management

We use JSON Web Tokens (JWT) for stateless session management.

### Token Expiry Policy
To balance security and developer productivity, the following expiry policy is mandated:
- **Access Tokens**: Short-lived, valid for **60 minutes**. (Web clients: Use **HttpOnly Cookies** where possible).
- **Refresh Tokens**: Long-lived, valid for **7 days**.

### Silent Refresh Mechanism
Applications MUST implement a silent refresh flow to prevent user disruption:
1.  **Interceptor**: The frontend API client (e.g., Axios) should include a response interceptor.
2.  **401 Handling**: Upon receiving a `401 Unauthorized` error, the client should attempt to call the `/refresh` endpoint using the stored refresh token.
3.  **Automatic Retry**: If the refresh is successful, the client should update the local access token and automatically retry the original failed request.
4.  **Graceful Failure**: If the refresh token is also expired or invalid, the user should be redirected to the login page.

## 4. Input Validation (Zero Trust)
*   **Sanitization**: Never trust user input. Use libraries (Pydantic, Zod) to strict-type and validate all incoming data.
*   **SQL Injection**: **Never** write raw SQL strings with concatenation. Always use the ORM or parameterized queries.
*   **XSS**: Use modern frontend frameworks (React) which escape by default. Audit `dangerouslySetInnerHTML` usage.

## 5. Data Protection
*   **Encryption at Rest**: PII (Personally Identifiable Information) must be encrypted in the DB.
*   **Secrets**:
    *   Never commit secrets to Git.
    *   Use `.env` files for local dev (gitignored). This is the mandatory way to provide credentials to **AI Agents** (like Antigravity) without risking a commit.
    *   Use Secret Managers (AWS Secrets Manager, Doppler, K8s Secrets) in production.

## 6. Logout
1.  **Explicit Termination**: Applications MUST provide a clear "Logout" or "Sign out" button.
2.  **Local Cleanup**: Clicking logout MUST clear all session data (`access_token`, `refresh_token`).
3.  **Redirection**: After logout, the user MUST be redirected to the login page.

## 7. HTTP Security Headers
All web responses must set standard security headers:
*   `Content-Security-Policy` (CSP): Restrict script sources.
*   `X-Content-Type-Options: nosniff`
*   `X-Frame-Options: DENY`
*   `Strict-Transport-Security` (HSTS)

## 8. Dependency Management
*   **SCA (Software Composition Analysis)**: 
    *   Run `npm audit` and `pip-audit` in CI/CD pipelines to detect vulnerable libraries.
    *   **Baseline Management**: Vulnerabilities with no available fix should be explicitly ignored with an audit trail, but all other findings must block the build.
*   **Container Scanning**: 
    *   Use tools like **Trivy** to scan Docker images for OS-level vulnerabilities.
    *   Scans should be integrated into the container build process (e.g., in the `Makefile` or CI config).
*   **Updates**: Keep dependencies patched. Schedule regular dependency updates to minimize technical debt and security drift.

## 10. Logging & PII Protection
*   **Structured Logging**: Prefer structured JSON logging over plaintext for better observability and indexability.
*   **Redaction**: **NEVER** log sensitive credentials (passwords, JWTs, OAuth tokens) in Plaintext. 
    *   *Implementation Standard*: Use a redaction utility or explicit "safe-mapping" when logging request/response headers or payloads.
    *   *Example*: Replace `Authorization: Bearer <secret>` with `Authorization: Bearer [REDACTED]` in debug logs.
*   **PII Filtering**: Minimize the logging of Personally Identifiable Information (PII) like full names or email addresses unless relevant to a specific audit trail. Use internal identifiers (UUIDs) where possible.
