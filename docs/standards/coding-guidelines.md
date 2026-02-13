# Coding Guidelines

## General Principles
1.  **Readability over Cleverness**: Code is read more often than it is written.
2.  **Consistency**: Follow the established idioms of the codebase.
3.  **Standardized Structure**: Follow the [Repository Structure](repository-structure.md) for all projects.
4.  **Comments**: Comment "why", not "what". The code explains "what".
5.  **Data-Driven Defaults**: Avoid "Magic String" defaults for dynamic entities (slugs, IDs). Fetch available values from the API and default to the first valid item if no specific state is provided.
6.  **Language**: All technical and internal text (code, logs, docs, db schemas) MUST use **UK English** (en-GB). UI elements may be localised based on product requirements. See [ADR 0013](../decisions/0013-standardise-uk-english.md).
7.  **Character Set Robustness**: Systems MUST handle non-ASCII, Unicode, and special characters (e.g., apostrophes, accents) gracefully. Always use UTF-8 as the standard encoding for databases, APIs, and file storage. Test data should explicitly include edge-case characters to verify rendering and storage.

## Language Specific Standards

### JavaScript / TypeScript (Frontend & Mobile)
*   **Style Guide**: Airbnb or Google Style Guide (enforced via ESLint).
*   **Formatting**: [Prettier](https://prettier.io/).
*   **Naming**:
    *   Variables/Functions: `camelCase`
    *   Classes/Components: `PascalCase`
    *   Constants: `UPPER_SNAKE_CASE`

### Python (Backend)
*   **Framework**: **FastAPI** is the default for APIs.
*   **Style Guide**: Follow PEP 8.
*   **Type Hints**: **Mandatory**. Do not write functions without type hints.
*   **Tooling**: Use `uv` for package management. Use `ruff` for linting/formatting (it replaces Black/Isort/Flake8).
*   **Testing**: `pytest`.

### HTML / CSS (Web)
*   **Framework**: **Tailwind CSS**. Do not use Bootstrap or vanilla CSS files unless necessary.
*   **Component Library**: **shadcn/ui**.
    *   Do not build complex interactive components (modals, dropdowns) from scratch; use the shadcn (Radix) primitives.
    *   Customize the components in `components/ui/` rather than overriding styles locally where used.
*   **Structure**: Component-based. Don't repeat lists of classes; wrap them in a component (e.g., `<Button>`).
*   **Semantic HTML**: Tailwind doesn't replace semantics. Use `<button>`, `<nav>`, `<h1>` appropriately.
*   **Ordering**: Use a consistent class ordering (e.g., `prettier-plugin-tailwindcss`) to reduce merge conflicts.

### Mobile (React Native)
*   **Framework**: **Expo**.
*   **Styling**: **NativeWind**. Use Tailwind classes (`className="flex-1 bg-white"`) exactly as you do on the Web.
*   **Navigation**: **Expo Router**. Use file-based routing (`app/index.tsx`).
    *   Avoid hardcoding platform checks (`Platform.OS === 'ios'`).
    *   Use `.native.tsx` or `.web.tsx` extensions if a component must diverge significantly.

### Database Evolution (Migrations)
*   **Tool**: **Alembic** (Python).
*   **Workflow**:
    *   Migrations are code. They must be reviewed.
    *   **Forward Only**: Never modify an existing migration file after it has been merged. Create a new one.
    *   **Non-Destructive**: Avoid `DROP COLUMN` in the same deployment as code usage changes. Usage: "Expand and Contract" pattern.

### UX & Accessibility (A11y)
*   **Standard**: **WCAG 2.1 AA**.
*   **Requirements**:
    *   All interactive elements must have `aria-label` or accessible text.
    *   Color contrast must pass the 4.5:1 ratio.
    *   Keyboard navigation must work (focus states).
    *   **Tools**: Use `axe-core` in E2E tests to auto-detect violations.

## Tooling
All projects must include configuration files (`.prettierrc`, `.eslintrc`, `pyproject.toml`) to enforce these rules automatically in the IDE and CI pipelines.

## Error Handling

### Python (FastAPI)
*   **Exceptions**: Use Python exceptions for control flow.
*   **Catching**: Catch exceptions at the API layer (`exception_handlers.py`) and convert them to standard HTTP responses.
    *   **Chaining**: Always use `raise ... from err` when re-raising or transforming exceptions to preserve the stack trace.
    ```python
    try:
        data = await service.get_data()
    except ValueError as err:
        raise HTTPException(status_code=400, detail="Invalid data") from err
    ```
    *   Do not crash the server on expected errors (e.g., UserNotFound).
    *   Do crash (or log error) on unexpected system states (e.g., DB connection lost) so the supervisor can restart the process.

### TypeScript / React
*   **Reactivity**: When relying on `localStorage` for cross-tab or persistent state (e.g., `accessToken`), use a `storage` event listener to ensure components remain reactive.
*   **Initialization**: Initialize error states directly from URL parameters (if applicable) using lazy initializers to avoid redundant renders or race conditions in `useEffect`.
*   **Validation**: Use `Zod` to validate inputs at the boundary.
*   **Try/Catch**: Use `try/catch` blocks around async calls.

## Logging

Logging is a critical component of our observability strategy. We use **Structured Logging** (JSON) for all server-side components.

Detailed rules and implementation strategies are defined in the following Architecture Decision Records:
*   [ADR 0011: Observability Strategy](../decisions/0011-observability-strategy.md) - Core logging rules (JSON format, 12-factor logs, no print statements).
*   [ADR 0014: Logging Implementation & Strategies](../decisions/0014-logging-implementation-strategies.md) - Language-specific tools, component policies (e.g. client-side console), logging levels, and dynamic control.

## Software Design Philosophy

We adopt specific principles to ensure code quality and maintainability (our "12-Factor for Code").

### 1. SOLID Principles
We prioritize these two above all:
*   **Single Responsibility Principle (SRP)**: A class/function should have one job.
    *   *Bad*: A generic `UserManager` that handles DB queries, email sending, and password hashing.
    *   *Good*: `UserRepository` (DB), `EmailService` (Email), `PasswordHasher` (Crypto).
*   **Dependency Inversion (DIP)**: Depend on abstractions, not details.
    *   Inject dependencies (like `db_session` or `email_client`) rather than importing specific implementations globally.

### 2. Clean Architecture (Lite)
We enforce a strict dependency flow:
*   **Controllers (API)**: Can import Services. Cannot import DB Models directly.
*   **Services (Business Logic)**: Can import Repositories. Cannot import HTTP/API code.
*   **Repositories (Data Access)**: Can import DB Models.
*   **Entities/Models**: Pure data. Depend on nothing.

### 3. Concurrency & Synchronicity

To maintain interface responsiveness and system scalability:
- **Async/Await First**: Use asynchronous I/O (`async`/`await`) for all networked and filesystem operations in the backend (FastAPI).
- **Avoid Blocking the Event Loop**: Never perform long-running CPU-bound tasks or synchronous I/O directly within an `async` function.
- **Bridge Synchronous Calls**: When using libraries that only provide a synchronous interface (e.g., legacy SDKs), wrap the calls in `asyncio.to_thread` (Python 3.9+) to offload them to a background thread and avoid blocking the main event loop.

### 4. Database Transaction Integrity

To prevent database contention (e.g., SQLite `database is locked` errors):
- **Minimal Transaction Duration**: Keep database transactions as short as possible. Commit or rollback immediately after the necessary operations are complete.
- **No External API Calls in Transactions**: Never perform slow or external I/O (like calling the Xero API) while holding a database transaction open. This prevents locking the database for the duration of the network request.
- **Granular Sessions**: Use separate, short-lived database sessions for distinct units of work rather than one long-lived session for a complex multi-step process.

### 5. Responsiveness & Reliability
- **Throttling & Concurrency**: Background tasks (e.g., sync loops) MUST be throttled and protected against concurrent execution of the same task to prevent resource exhaustion or data corruption.
- **Race Condition Prevention**: Frontends should prefer idempotent operations and handle slow/stale response data correctly (e.g., using `AbortController` in JS to cancel outdated requests).
- **Graceful Polling**: When polling for status, use a backing-off or fixed interval that balances user experience with server load. Ensure the UI can handle the transition from "initializing" to "polling" without state flickering.
