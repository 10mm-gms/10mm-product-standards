# Git Workflow

## Branching Strategy
We use **Main-based Development**.
1.  **Main Branch**: `main`. Always deployable.
2.  **Feature Branches**: Short-lived branches created from `main`.

### Naming Convention
format: `type/description-slug`
*   `feat/user-login`
*   `fix/billing-calculation`
*   `chore/update-deps`

## Commit Messages
We follow **Conventional Commits**.
Format: `type(scope): description`

*   `feat: add login page`
*   `fix(api): handle null user`
*   `docs: update architecture diagram`

## Pull Requests
*   **Small**: Aim for PRs < 400 lines of code.
*   **Squash & Merge**: All PRs are squashed into a single commit on `main` to keep history linear and clean.
