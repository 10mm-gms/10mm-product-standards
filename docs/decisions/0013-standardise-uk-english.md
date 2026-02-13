# 13. Standardise UK English

Date: 2026-01-02

## Status

Accepted

## Context

Consistency in language across all technical artifacts (code, logs, documentation) is essential for maintainability and clear communication within the team and when interacting with LLM-based agents. Inconsistent spelling (e.g., "color" vs. "colour", "standardize" vs. "standardise") can lead to confusion and duplication in codebase searches and log analysis.

## Decision

We will standardise on **UK English** (en-GB) for all internal and non-UI text elements across all products.

*   **Scope**: This includes but is not limited to:
    *   Source code (variable names, function names, class names, comments).
    *   Configuration files and property keys.
    *   Log messages and error strings.
    *   Internal and technical documentation (READMEs, ADRs, user stories).
    *   Database schemas (table and column names).
*   **User Interface (UI)**:
    *   Individual products have the autonomy to decide if the UI should be localised or internationalised for different regions.
    *   However, the default UI language should also be UK English unless specified otherwise by the product owner.

## Consequences

*   **Positive**: Improved consistency across the entire technical ecosystem.
*   **Positive**: Reduced cognitive load for developers and AI agents by having a single source of truth for spelling.
*   **Positive**: Simplified grep/search operations across logs and source code.
*   **Negative**: Developers accustomed to US English (the common default in many libraries) will need to be diligent about spelling.
*   **Negative**: Some third-party libraries use US English, creating an unavoidable mix in certain contexts (e.g., `backgroundColor` in CSS), but our own abstractions should remain UK English.
