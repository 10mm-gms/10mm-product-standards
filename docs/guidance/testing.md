# Testing Guide

This document provides practical instructions for writing and running tests in our product suite.

## The Testing Pyramid

We prioritize tests that are fast and reliable.
1.  **Unit**: Most of your tests.
2.  **Integration**: Test database/API boundaries.
3.  **E2E**: Verify critical user flows.

## Data Integrity & Character Handling

All applications in the product suite MUST support **UTF-8** character encoding throughout the entire stack (Database, API, Frontend).

### Expectations:
1.  **Non-ASCII Support**: Systems must gracefully handle characters like `é`, `ü`, `ø`, etc., in names, descriptions, and metadata.
2.  **Special Characters**: Systems must correctly escape and render special ASCII characters such as single quotes (`'`), double quotes (`"`), and ampersands (`&`) to prevent crashes or SQL injection vulnerabilities.
3.  **Search & Filters**: Frontend search and filtering should be case-insensitive and, where appropriate, diacritic-insensitive.

## Behavior Driven Development (BDD)

We use **Gherkin syntax** (Given/When/Then) in our [Product Requirement Documents](blueprints/prd.md) to define behavioral specifications.

> [!IMPORTANT]
> **Source of Truth**: Gherkin scenarios MUST be written and approved in the PRD *before* any implementation or automated test code is created. These scenarios drive both the engineering effort and the verification plan.
### Generating Tests from Gherkin
While we don't currently use an automated compiler (like `playwright-bdd`), you can use the following methods to generate tests:

1.  **Manual Translation (Standard)**: Map Gherkin scenarios to Playwright `test` and `test.step` blocks for transparency.
2.  **Agentic Generation**: You can ask an AI agent (like Antigravity) to:
    > "Generate a Playwright test file based on the Gherkin scenarios in [PRD link]."
3.  **Scaffold Snippet**: Use `test.step()` to mirror Gherkin steps exactly.

```typescript
test('Engineer views their daily progress', async ({ page }) => {
  await test.step('Given I am logged in as "engineer@domain.com"', async () => {
    // ... automation code
  });
  // ... When / Then steps
});
```

## TDD Workflow (Recommended)

When working on complex logic, use the "Red-Green-Refactor" loop:

1.  **Red**: Write a small test for the next piece of functionality. Run it and watch it fail.
2.  **Green**: Write simpler code to make the test pass.
3.  **Refactor**: Clean up the code while keeping the test passing.

## Backend (Python/FastAPI)

### Setup
We use `pytest`. Ensure you have `pytest` and `httpx` installed via `uv`.

### Writing a Unit Test
Tests live in `tests/`.

```python
# tests/test_core.py
from app.core import calculate_total

def test_calculate_total_simple():
    assert calculate_total([10, 20]) == 30
```

### Writing a DB Integration Test
Use `TestContainers` or a fixture that rolls back transactions.

```python
# tests/test_db.py
import pytest
from app.models import User

@pytest.mark.asyncio
async def test_create_user(db_session):
    user = User(name="Alice")
    db_session.add(user)
    await db_session.commit()
    
    saved = await db_session.get(User, user.id)
    assert saved.name == "Alice"
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific file
pytest tests/test_core.py
```

## Frontend (Web & Mobile)

We follow a React-centric testing approach using local runners.

### Automated Unit Tests
Tests are consolidated in `src/[frontend|mobile]/tests/`.

*   **Web (Vite)**: Uses `vitest` for fast execution.
*   **Mobile (Expo)**: Uses `jest` with the `jest-expo` preset.

### Writing a Unit Test
```tsx
// src/mobile/tests/App.test.tsx
import { render, screen } from '@testing-library/react-native';
import { App } from '../app';

test('renders correctly', () => {
  render(<App />);
  expect(screen.getByText('Workshop Utilisation')).toBeTruthy();
});
```

### Running Tests Locally
```bash
# Web only
cd src/frontend && npm run test

# Mobile only
cd src/mobile && npm run test
```

## E2E (Playwright)

We use Playwright for web E2E.

### The Mocking Philosophy
We typically **mock external identity providers** (like Google, Xero, or Auth0) in local and CI E2E tests for the following reasons:
1.  **Determinism**: External services can be slow or intermittently unavailable, leading to flaky tests.
2.  **Security**: Real logins often require MFA or real credentials which are difficult and insecure to automate.
3.  **Isolation**: We want to test our application's response to a valid/invalid token, not Google's infrastructure.
4.  **Speed**: Mocked redirects happen in milliseconds, whereas real OAuth flows take seconds.

> [!TIP]
> Use real accounts only for **Critical Path Verification** (E2E) in staging/production environments. For local feature development, simulating the redirect with a token is the standard pattern.

### Running Tests
> [!IMPORTANT]
> Playwright tests require the development servers to be running. While the latest configuration attempts to start them automatically, it is recommended to have `make dev` running in a separate terminal.

> [!NOTE]
> Tests must be executed from the directory containing `playwright.config.ts` (typically `src/frontend`) or via the root-level `make test-e2e` shortcut.

```bash
# Option 1: Using Make from the root (Recommended)
make test-e2e

# Option 2: Running directly from the frontend directory
cd src/frontend
npx playwright test

# Option 3: Run in headed mode (shows the browser)
npx playwright test --headed

# Option 4: Run in UI mode (interactive explorer)
make test-e2e-ui
# or directly
npx playwright test --ui

# Open the HTML report to see failures, screenshots, and traces
npx playwright show-report
```

### Debugging Headless Failures
When tests fail in headless mode (e.g., in CI), you can use the following tools for visual feedback:

1.  **HTML Report**: Automatically generated on failure. Run `npx playwright show-report` to view it.
2.  **Screenshots & Video**: Can be configured in `playwright.config.ts` to capture only on failure.
3.  **Trace Viewer**: The most powerful tool. It records every action, console log, and network request. If a trace is recorded, you can open it with:
    ```bash
 npx playwright show-trace path/to/trace.zip
    ```

## Mobile E2E (Maestro)
We use **Maestro** for mobile E2E testing as it provides a clean, declarative syntax for cross-platform mobile automation.

### Writing a Flow
Maestro flows are written in YAML (`.yaml`) files.
```yaml
appId: com.10mm.workshop
---
- launchApp
- assertVisible: "Workshop Utilisation"
- tapOn: "Today"
- assertVisible: "Data Complete"
```

### Running Tests
Maestro requires an active emulator or physical device.
```bash
# Run a specific flow
maestro test .maestro/today_navigation.yaml

# Run all flows in a directory
maestro test .maestro/
```

### Debugging Failures
*   **Maestro Studio**: An interactive UI for building flows.
    ```bash
    maestro studio
    ```
*   **Screenshots/Hierarchy**: Maestro captures the UI hierarchy on failure, which is accessible via the CLI output.

## Observational Testing
If tests are passing too quickly or concurrently to observe, use these methods to slow them down for manual verification.

### 1. Playwright UI Mode (Best for Development)
UI mode allows you to step through tests, see snapshots at every point, and watch the behavior interactively.
```bash
npx playwright test --ui
```

### 2. Slow-Mo & Sequential Execution
Run in headed mode, limited to a single worker, with an artificial delay between actions.
```bash
npx playwright test --headed --workers=1 --project=chromium
```
To add a specific delay (e.g., 500ms between actions), you can use the `--slow-mo` flag if supported by your runner or modify `playwright.config.ts` temporarily.

## Automation Interface

We use a root-level `Makefile` and `build.sh` script to provide a consistent interface for developers and CI.

### Makefile Targets
The `Makefile` provides granular control over different layers of the application:

| Target | Description |
| :--- | :--- |
| `make test` | Runs ALL unit and integration tests (Web + Mobile). |
| `make test-web` | Runs only Backend and Frontend unit/integration tests. |
| `make test-mobile` | Runs only Mobile unit tests (Jest). |
| `make test-e2e` | Runs Playwright E2E tests (Web). |
| `make lint` | Runs ruff (Backend) and eslint (Frontend & Mobile). |
| `make fmt` | Formats all source code across all components. |
| `make build` | Builds ALL artifacts (Container + Mobile Export). |
| `make build-container`| Builds the web frontend and Docker image. |
| `make build-mobile` | Builds the Android export for the mobile app. |

### Scoped Pipelines
The `./build.sh` script supports scoping to speed up development iterations:

```bash
# Run the full project pipeline (Default)
./build.sh all

# Run only the web/container pipeline (Lint, Test, E2E, Build)
./build.sh container

# Run only the mobile pipeline (Lint, Test, Build)
./build.sh mobile
```
