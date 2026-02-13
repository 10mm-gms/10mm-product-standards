# 16. Adopt Semantic Versioning

Date: 2026-01-23

## Status

Accepted

## Context

As the ecosystem of products grows, we need a clear and predictable way to version our software components, libraries, and APIs. Without a formal versioning strategy, it's difficult for consumers (both internal and external) to understand the impact of updates, leading to potential breaking changes, dependency hell, and deployment uncertainty.

We need a standard that:
1.  Communicates the nature of changes (breaking vs. non-breaking).
2.  Works well with modern package managers (npm, pip, cargo, etc.).
3.  Is widely understood by the developer community.

## Decision

We will adopt **Semantic Versioning (SemVer) 2.0.0** across all products and repositories.

*   **Format**: Version numbers will follow the `MAJOR.MINOR.PATCH` format (e.g., `1.2.3`).
*   **Rules**:
    *   **MAJOR** version: Incremented when you make incompatible API changes.
    *   **MINOR** version: Incremented when you add functionality in a backward compatible manner.
    *   **PATCH** version: Incremented when you make backward compatible bug fixes.
*   **Initial Development**: Starting at `0.1.0` for new projects. Version `1.0.0` defines the first stable public API.
*   **Automation**: We will encourage the use of tooling (like `standard-version`, `semantic-release`, or custom scripts) to automate version bumps based on Conventional Commits.
*   **Git Integration**: All releases must be tagged in Git using the `vX.Y.Z` format (e.g., `v1.0.0`).

## Consequences

*   **Positive**: Predictable dependency management for both internal and external consumers.
*   **Positive**: Improved automation potential for CI/CD pipelines (automatic changelog generation, release notes).
*   **Positive**: Clearer communication of breaking changes through version increments.
*   **Negative**: Requires developer discipline to categorize changes correctly.
*   **Negative**: Initial overhead in setting up versioning tooling and workflows.
*   **Negative**: Risk of "version inflation" if minor fixes are miscategorized as major changes.
