# 10. Comprehensive Testing Strategy

Date: 2025-12-21

## Status

Accepted

## Context

We need a consistent testing strategy to ensure reliability across our unified tech stack (FastAPI, React Native/Expo, shadcn/ui).
Without a standard, some teams might rely often on manual QA or slow E2E tests, while others might over-mock unit tests.

## Decision

### Methodology: TDD is Encouraged, Not Required

We view **Test-Driven Development (TDD)** as a valuable tool for designing interfaces and handling complex logic, but we do not overly enforce it for boilerplate code.

*   **Complex Logic**: **Strongly Recommended**. (e.g., pricing algorithms, complex state transitions). Write the test first to clarify the requirements.
*   **Boilerplate / CRUD**: **Optional**. (e.g., simple database models, pass-through API endpoints). It is acceptable to write tests after the implementation, provided they are written in the same PR.

We value **confidence** and **coverage** over the chronological order of test writing.

We will follow the **Testing Pyramid**:

### 1. Unit Tests (70%)
*   **Scope**: Individual functions, classes, and components. Fast and isolated.
*   **Backend**: `pytest`.
*   **Frontend**: `vitest` + `react-testing-library`.

### 2. Integration Tests (20%)
*   **Scope**: Interactions between immediate dependencies (API interactions with DB, Component interactions with Hooks).
*   **Backend**: `pytest` + `testcontainers` (spin up real Postgres/Redis in Docker).
    *   *Note*: Avoid mocking databases if possible; use ephemeral containers.
*   **Frontend**: Render components that include React Query / API calls (mocking the network layer via MSW or similar).

### 3. End-to-End (E2E) Tests (10%)
*   **Scope**: Critical user flows running against a full environment to verify "system connectivity."
*   **Tool**: **Playwright**.
*   **Philosophy**: Test distinct critical paths. 

#### System Connectivity & The "Mock-Lie" Prevention
To prevent "Mock-Lies" (tests passing while the system is broken), we enforce a "Connectivity Rule": Every functional requirement must be verified by at least one **System Mode** test (zero-mock) before being considered "Done." 

#### Dual-Mode Playwright Specs
Playwright tests should be written once and executed in two modes via `PLAYWRIGHT_MODE`:
*   **MOCKED**: Browser intercepts API calls with local JSON. (Fast, no backend needed, verifies UX/UI state).
*   **SYSTEM**: Requests pass through to the real backend and database (running in Docker or local dev). (Verifies schema parity and endpoint existence).

### 3.1 Traceability Matrix Enforcement
To prevent the omission of system-level verification, all project **Traceability Matrices** MUST comply with the following:
1.  **Mandatory E2E Coverage**: Every functional requirement (prefixed with `REQ-`) MUST have an "E2E" entry in the `Test Tier` column.
2.  **No Isolation for Mutators**: Requirements involving data mutation (Create, Update, Delete) CANNOT be verified by Unit or Integration tests in isolation; a System-Mode E2E test is mandatory to prove the end-to-end circuit is unbroken.
3.  **UI Verification**: E2E tests must verify the visual presence and functionality of UI triggers (buttons, forms, links) as perceived by the user.
4.  **Audit Failure**: Any Test Plan (`testing.md`) that lists a functional requirement with only "Unit" or "Integration" is a violation of this standard and must be rejected.

## CI/CD Enforcement
*   All tests must pass in CI before merging.
*   Coverage metrics are collected but loose (no hard 100% requirement), aiming for meaningful coverage.

## Consequences

*   **Positive**: High confidence in releases.
*   **Positive**: "Shift Left" - bugs caught early in unit tests.
*   **Negative**: Integration tests with `testcontainers` can be slower than mocks.
*   **Negative**: Maintaining E2E tests requires dedicated effort to avoid flakiness.
