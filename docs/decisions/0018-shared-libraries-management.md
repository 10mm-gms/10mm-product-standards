# 18. Shared Libraries Management

Date: 2026-02-07

## Status

Accepted

## Context

As the product suite grows, we are encountering code that is common across multiple services and frontends (e.g., authentication logic, standard logging, UI component foundations). Duplicating this code leads to maintenance overhead, inconsistency, and slower development. We need a way to maintain shared code that ensures high reuse while keeping changes synchronised across all products.

## Decision

We will centralise all shared code into a dedicated libraries collection.

1.  **Repository Location**: All shared libraries will be stored in the `product_standards` repository under the `libraries/` directory.
    -   Example: `product_standards/libraries/backend-core`, `product_standards/libraries/ui-core`.
2.  **Product Integration**: To ensure changes automatically flow out to all products during development and build time, we will **symlink** the `libraries/` directory from the `product_standards` repository into the root of each product repository.
    -   In each product repo (e.g. `parts_service`), there will be a `libraries/` symlink pointing to `../product_standards/libraries/`.
3.  **Versioning**: 
    -   Local development will use the symlinked "live" version to ensure immediate feedback.
    -   For production builds and releases, libraries will follow **Semantic Versioning (SemVer)** as per ADR 0016.
    -   The `pyproject.toml` (for Python) or `package.json` (for JS/TS) in each service will reference these libraries using consistent relative paths during local development.
4.  **Automatic Synchronisation**: By using symlinks, any update to a shared library in the `product_standards` repo is immediately reflected in the development environment of all products tracking that standard.

## Consequences

*   **Positive**: Reduced code duplication and logic drift.
*   **Positive**: Improved consistency across the product suite.
*   **Positive**: Faster development of new products by building on established foundations.
*   **Negative**: A breaking change in a shared library can impact multiple products simultaneously; strict adherence to automated testing in libraries is required.
*   **Mitigation**: Shared libraries must maintain high test coverage (unit + integration) within their own directory before being pushed.
