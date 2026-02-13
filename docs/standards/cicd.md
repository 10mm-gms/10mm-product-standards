# CI/CD Standard (v0.2)
<!-- Standard Version: 0.2 -->

This document defines our **Local-First CI/CD** philosophy. We prioritize automation that runs on a developer's machine exactly as it runs in a remote environment.

## 1. Philosophy: Local-First
We avoid platform-specific lock-in (e.g., GitHub Actions, GitLab CI logic).
*   **Agnosticism**: The "Brain" of the pipeline must be a set of portable scripts/commands in the repository.
*   **Parity**: Running the pipeline locally must be identical to running it in a CI tool.
*   **Entry Point**: Every project must have a `Makefile` or `Taskfile` as the standardized interface for automation.

## 2. Pipeline Stages

The pipeline is realized via standardized commands in the `Makefile` and orchestrated by `build.sh`.

### `make lint` (Static Analysis)
*   Enforces style and type safety (e.g., `ruff check`, `npm run lint`).
*   Must pass before any further testing.

### `make test` (Integration Testing)
*   Runs fast, isolated tests (e.g., `pytest src/backend/tests/`).
*   Focuses on business logic correctness and database interactions (using ephemeral SQLite or containers).

### `make code-scan` (Security)
*   Runs dependency audits and static security analysis (e.g., `npm audit`, `pip-audit`, `bandit`, `semgrep`).

### `make test-e2e` (Mocked E2E)
*   Runs Playwright tests with fully mocked API responses.
*   Focuses on UI/UX correctness and fast feedback loops.

### `make test-e2e-system` (System E2E)
*   Runs the same Playwright tests but against a real backend and database.
*   Ensures "No Mock-Lies" and validates system connectivity.

### `make build` (Packaging)
*   Compiles frontend assets and packages the app into OCI (Docker) images.

### `make container-scan` (Vulnerability Scanning)
*   Scans the final production image for OS-level vulnerabilities (e.g., `trivy`).

## 2.6 Test Environment Isolation
To prevent database locking and resource contention in local and remote environments:
*   **Cleanup**: Testing targets (especially E2E) MUST explicitly kill orphaned server processes from previous runs before starting.
*   **Idempotency**: Every test run must be able to recover from a previous partial failure or interrupted process.
*   **Implementation**: Use `pkill` or equivalent in the `Makefile` to ensure a clean state.

## 3. Build Identification (The "Build ID")
In a local-first environment, we use the **Git Commit Count** to provide a sequential integer build number. This ensures traceability without requiring a persistent file state like a `BUILD` file.

### Standard Format
`v[VERSION].b[SERIAL]-[GIT_SHA]`

*   **Example**: `v0.1.b42-a1b2c3d`
*   **Traceability**: This provides a classic "Build 1, Build 2, Build 3" experience while still being linked to the specific code SHA.
*   **Immutability**: Once a Build ID is assigned to an image, that number is "burned" and must not be reused for different code.

## 4. Remote Integration
A remote CI tool (if used later) should be a "dumb" runner that simply executes the repo's `build.sh`.
```bash
./build.sh
```

## 5. Blueprint
See `blueprints/Makefile` and `blueprints/build.sh` for the standard implementations.
