# ADR 0015: Standardised Repository Structure

## Status
Proposed

## Context
As we move towards more autonomous agentic coding, the repository structure must be consistent and predictable. Our current structure (e.g., in `workshop_utilisation`) has inconsistencies where scripts, tests, and documentation are scattered. A standard layout allows:
1.  **AI Predictability**: Agents know exactly where to find and add code, tests, and scripts.
2.  **Shared Tooling**: Build scripts and CI pipelines can be reused across projects.
3.  **Clear Ownership**: Separation of internal source code from system-level verification and auxiliary automation.

## Decision
We will standardise the repository layout to clearly distinguish between **Source Code** (Internal), **System Verification** (External), and **Auxiliary Scripts**.

### High-Level Structure
The repository will follow this top-level layout:

```text
/
├── src/                # Source code (Internal Logic)
│   ├── backend/        # Python/FastAPI code
│   │   ├── api/        # Routers & Endpoints
│   │   ├── core/       # Business Logic / Services
│   │   ├── db/         # Models & Migrations
│   │   └── tests/      # Backend Unit & Integration Tests (Colocated)
│   └── frontend/       # TypeScript/React code
│       ├── src/        # UI Code
│       │   └── ...     # Components, Hooks, etc.
│       │       └── [name].test.tsx # Component Unit Tests (Colocated)
├── tests/              # System-Level Verification (External)
│   └── e2e/            # Playwright E2E Tests
│       ├── specs/      # Test scenarios
│       ├── mocks/      # Mock definitions
│       └── utils/      # Helpers & fixtures
├── scripts/            # Auxiliary Automation
│   ├── seed/           # Data seeding scripts
│   ├── dev/            # Local environment helpers
│   └── maintenance/    # Migrations or cleanup tasks
├── docs/               # Project-specific documentation & ADRs
├── planning/           # Epics and stories
├── dist/               # Production build output (git-ignored)
├── test-results/       # Test reports and screenshots (git-ignored)
├── build.sh            # Main CI entry point
└── Makefile            # Standard developer interface
```

### Principles
1.  **Unit Test Colocation**: Tests for specific modules or components should live as close to the source as possible (e.g., in subdirectories named `tests` or colocated `.test.tsx` files).
2.  **System Test Isolation**: Tests that verify the entire system (E2E) should live at the root level, as they are not "owned" by any single source directory.
3.  **Auxiliary vs Source**: Code that is not deployed as part of the application (seeding, dev helpers) must live in `scripts/`, never in `src/`.

## Consequences
*   **Consistency**: AI agents (and humans) have a predictable map for navigating the repo.
*   **Pipeline Reusability**: CI/CD templates can target standard directories like `test-results/` and `src/backend/tests/`.
*   **Migration**: Existing projects (`workshop_utilisation`) will require a refactor to align with this structure.
