# 3. Use shadcn/ui for Component Library

Date: 2025-12-21

## Status

Accepted

## Context

We have decided to use Tailwind CSS (ADR-0002).
Building accessible, high-quality components from scratch is time-consuming.
We need a solution that accelerates development while maintaining the "premium" feel and avoiding the generic look of pre-packaged libraries (like Bootstrap or Material UI).
We want to retain full control over the component code to allow for specific customizations.

## Decision

We will use **shadcn/ui** as our primary component library.

*   **Implementation**: Components are added to the codebase (no npm dependency for the library itself).
*   **Primitives**: Built on top of **Radix UI** for accessibility (headless primitives).
*   **Styling**: Styled with **Tailwind CSS**.
*   **Icons**: **Lucide React** (standard pairing with shadcn).

## Consequences

*   **Positive**: "Best of both worlds" - speed of a library, flexibility of custom code.
*   **Positive**: Excellent accessibility out of the box.
*   **Positive**: Consistent design language (Typography, Spacing, Colors).
*   **Negative**: Updates are manual. If shadcn/ui updates a component we've heavily modified, we have to resolve conflicts manually.
