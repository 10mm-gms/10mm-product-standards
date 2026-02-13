# Requirement-Test Traceability Standard

To ensure every requirement is tested and every test represents a valid requirement ("No Orphan Code"), we use a **Traceability Standard** driven by IDs and Gherkin behavior specs.

## 1. Requirement IDs
Every functional requirement in a PRD must have a stable, unique ID.
*   **Format**: `REQ-[COMPONENT]-[NUMBER]`
*   **Example**: `REQ-AUTH-001` (User Login), `REQ-CART-005` (Add item)

## 2. Behavioral Specs (Gherkin)
For complex user flows (E2E candidates), requirements must be defined using **Gherkin syntax** (Given/When/Then). This serves as the "Source of Truth" for generative testing.

**In the PRD:**
```gherkin
Feature: User Login
  @REQ-AUTH-001
  Scenario: Successful login with valid credentials
    Given the user is on the login page
    When they enter valid username "alice" and password "secure123"
    Then they are redirected to the dashboard
```

## 3. Linking in Code
Tests must reference the ID they verify. This allows us to grep for coverage.

### Backend (Pytest)
Use a custom marker or docstring reference.
```python
import pytest

@pytest.mark.req("REQ-AUTH-001")
def test_login_success():
    """Verifies REQ-AUTH-001: Successful login"""
    ...
```

### Frontend/E2E (Playwright)
Use the annotation API.
```typescript
test('user can log in', async ({ page }) => {
  test.info().annotations.push({ type: 'req', description: 'REQ-AUTH-001' });
  // ... test code
});
```

## 4. Generating Tests from Requirements
Because we use Gherkin in the PRD, we can define the standard for **Automated Test Generation**:

1.  **Input**: PRD with valid Gherkin scenarios.
2.  **Process**: AI Agent or Code Gen tool reads the Gherkin.
3.  **Output**: Playwright test skeleton with `test.step` mapping one-to-one with Gherkin lines. See `blueprints/prd.md` for the standard template structure.

**Example Generated Code:**
```typescript
test('Successful login with valid credentials', async ({ page }) => {
  test.info().annotations.push({ type: 'req', description: 'REQ-AUTH-001' });

  await test.step('Given the user is on the login page', async () => {
    await page.goto('/login');
  });
  
  await test.step('When they enter valid username...', async () => {
    // ...
  });
});
```

## 5. Automated Environment Management
For E2E tests, the environment should ideally be started automatically. We use Playwright's `webServer` feature in `playwright.config.ts`.

**Standard Config:**
```typescript
export default defineConfig({
  // ...
  webServer: {
    command: 'make dev', // Starts backend & frontend
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```
This ensures a "single command" testing experience (`make test-e2e`) even on fresh clones.

**Environment Isolation**:
To prevent "readonly database" errors or port contention, the testing command MUST explicitly terminate orphaned server processes (e.g., using `pkill`) before starting a new run. This guarantees a clean state regardless of previous run outcomes.
## 6. Tiered E2E Testing (Mocked vs System)

To ensure both development speed and integration reliability, E2E tests must support two modes defined via the `PLAYWRIGHT_MODE` environment variable:

1.  **Mocked Mode (`MOCKED`)**:
    *   **Goal**: Instant feedback on UI logic.
    *   **Implementation**: Intercept all API calls using `page.route` and return JSON mocks.
    *   **Visibility**: No backend server is required (though it may be running).
2.  **System Mode (`SYSTEM`)**:
    *   **Goal**: Zero "Mock-Lies" and verification of system connectivity.
    *   **Implementation**: No intercepts. Requests go to a real backend and database (e.g., SQLite via `webServer`).

**Standard Command Interface**:
*   `make test-e2e`: Runs in **Mocked** mode (default).
*   `make test-e2e-system`: Runs in **System** mode.

## 7. Zero-Warning Policy

To prevent technical debt and catch subtle bugs early, all automated tests (Integration and E2E) must treat warnings as errors.

*   **Python (Pytest)**: Must configure `filterwarnings = ["error"]` in `pyproject.toml`.
*   **Frontend**: Must fail CI if `npm run lint` or `npx playwright test` produces unresolved warnings.
