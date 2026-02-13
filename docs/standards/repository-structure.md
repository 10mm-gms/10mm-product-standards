# Repository Structure Standard (v0.2)
<!-- Standard Version: 0.2 -->

This document defines the standard directory layout for all products in the suite. Consistency in structure allows for shared tooling, easier onboarding, and predictable AI-agent interaction.

## 1. High-Level Layout

Every repository follows this top-level structure:

```text
repo-root/
├── src/               # Source code (Internal Logic)
│   ├── backend/       # Python/FastAPI code
│   │   └── tests/     # Backend unit & integration tests
│   ├── frontend/      # Web/React UI code
│   │   └── tests/     # Frontend unit tests
│   └── mobile/        # Mobile/React Native UI code
│       └── tests/     # Mobile unit tests
├── tests/             # System-Level Verification
│   └── e2e/           # Playwright E2E tests (specs, mocks, utils)
├── scripts/           # Maintenance, seeding, and auxiliary scripts
├── docs/              # Project-specific documentation & ADRs
├── planning/          # Epics and stories
│   ├── BOARD.md       # Kanban board for project tracking
│   └── epics/         # Folder per epic (PRD + Stories)
├── dist/              # Built production artifacts
├── test-results/      # Test reports and screenshots
├── build.sh           # Main CI entry point
└── Makefile           # Standard automation interface
```

## 2. UI Structure (`src/frontend/` and `src/mobile/`)

We follow a React-compatible structure for both Web and Mobile:

*   `public/` (Web) or `assets/` (Mobile): Static assets.
*   `src/` (Web) or `app/` (Mobile): Application entry points.
*   `components/`: Reusable UI components.
*   `hooks/`: Shared React hooks.
*   `lib/` or `services/`: API clients and library initializations.
*   `tests/`: Consolidated unit tests (following the backend pattern).
*   `types/`: TypeScript definitions.

## 3. Backend Structure (`src/backend/`)

We follow a "Clean Architecture Lite" structure:

*   `api/`: FastAPI routes and dependency injection.
*   `core/`: Pure business logic (Services/Entities).
    *   `config/`: Environment configuration.
*   `db/`: Database models and migration scripts (Alembic).
*   `schemas/`: Pydantic models for request/response validation.

## 4. Planning Structure (`planning/`)

We use a file-based tracking system for progress and requirements:

*   `BOARD.md`: The central source of truth for the project state. Tracks Epics (highest level) and their child Stories.
*   `epics/`: Contains a directory for every significant feature or initiative:
    *   `EPIC_XXX_.../`:
        *   `prd.md`: The 10-Factor Requirement document (PRD).
        *   `stories.md`: The technical breakdown and checklist for individual implementation steps.

## 5. Built vs Source

*   **Source**: Everything inside `src/`, `docs/`, `planning/`, etc.
*   **Built**: Generated directories MUST be git-ignored.
    *   `/dist/`: Production builds.
    *   `/build/`, `/.tmp/`: Temporary build artifacts.
    *   `/test-results/`: CI reports, Playwright traces, and screenshots.
    *   `/node_modules/`, `/.venv/`: Dependency directories.

## 6. Testing Hierarchy
        
To prevent "Mock-Lies" (tests passing while the system is broken), we enforce a three-tier testing hierarchy:

*   **Integration Tests (Logic & Storage)**:
    *   **Backend**: Located in `src/backend/tests/`.
    *   **Frontend/Mobile**: Located in `src/[frontend|mobile]/tests/`.
*   **E2E Specs (System Verification)**: 
    *   Located in root `tests/e2e/`.
    *   Must be runnable in **MockED Mode** (fast UI checks) and **System Mode** (connected to real backend and database).

## 7. Build & Auxiliary Artifacts

*   `build.sh`: The primary entry point for CI. It orchestrates building, linting, unit tests, and system E2E tests.
*   `Makefile`: Provides a standard interface for developers (e.g., `make dev`, `make test`, `make seed`).
*   `scripts/`: Contains transient scripts (seeding, data migrations, local dev helpers). No application logic should reside here.
