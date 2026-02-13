# API & Code Generation Standards

## Philosophy
We prefer **contract-first** development. Defining contracts explicitly allowing us to generate documentation, clients, and server stubs, ensuring consistency.

## REST APIs
*   **Standard**: [OpenAPI 3.1](https://www.openapis.org/)
*   **File Location**: `api/openapi.yaml` in the respective service repo.
*   **Tools**:
    *   *Linting*: `spectral`
    *   *Docs*: `Swagger UI` (available at `/api/docs`) or `Redoc` (available at `/api/redoc`)
    *   *OpenAPI Spec*: `/api/openapi.json`
    *   *Code Gen*: `openapi-generator` or `orval` (for Frontend)

## API Namespace & SPA Routing
To prevent routing collisions between backend endpoints and Single Page Application (SPA) client-side routers, all backend API routes **must** be namespaced under a clear prefix.

*   **Standard Prefix**: `/api` (or `/api/v1`).
*   **Routing Fallback**: The backend root (`/`) and any non-prefixed paths should serve the SPA `index.html`, allowing the frontend router to handle deep-linked URLs (e.g., `/dashboard/items`) without premature interference from backend authentication middleware.

## Standard Error Responses
To ensure the Frontend can consistently handle errors, all APIs must follow **RFC 7807 (Problem Details for HTTP APIs)**.

**JSON Structure:**
```json
{
  "type": "https://example.com/probs/out-of-credit",
  "title": "You do not have enough credit.",
  "detail": "Your current balance is 30, but that costs 50.",
  "instance": "/account/12345/msgs/abc",
  "status": 403
}
```
*   **Benefits**: Frontend can have a single `ErrorHandler` component that parses `title` and `detail` for *any* 4xx/5xx error globally.

## Secure Redirect Error Reporting
For processes using HTTP redirects (like OAuth/OIDC callbacks), **never** pass user-facing error strings in query parameters. This prevents XSS and reflection vulnerabilities.

*   **Mandatory**: Use standardized error codes (e.g., `?error=domain_restricted`).
*   **Implementation**: The Frontend must map these codes to predefined, safe local messages.

## Event-Driven Architecture
*   **Standard**: [AsyncAPI](https://www.asyncapi.com/)
*   **Usage**: For defining message payloads and topics (Kafka/RabbitMQ).

## Code Generation
When possible, generate boilerplate from these standards to avoid manual drift.
*   **Do not edit generated files manually.**
*   Regenerate as part of the build process or commit with a clear provenance.
