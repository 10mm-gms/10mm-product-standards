# 5. Adopt 10mm GMS Design System over Material Design

Date: 2026-01-25

## Status

Accepted

## Context

Previous standards mandated "Material Design 3" (ADR-legacy) while simultaneously choosing **shadcn/ui** + **Tailwind CSS** (ADR-0003) for implementation. This created a conflict where developers had to override shadcn's native aesthetic better suited for Tailwind to mimic Material Design's specific traits (ripples, high rounded corners), leading to inconsistency and wasted effort.

We need a consistent look across products that is easy to implement with our chosen stack.

## Decision

We will drop the requirement to mimic **Material Design 3**.

Instead, we will adopt the **10mm GMS Design System**, which is defined technically as:
1.  **Component Library**: The native visual style of **shadcn/ui** (clean, modern, modest border radii).
2.  **Design Tokens**: A shared Tailwind configuration defining our specific brand colors (10mm GMS Red), typography (Fira Sans/Poppins), and spacing.
3.  **Maintenance**: Files in `blueprints/frontend/` are the authoritative source for these tokens and must not be modified in a way that affects the appearance of fonts or colors without an explicit request by the user.

## Consequences

*   **Positive**: Zero "fight" between the design standard and the code library.
*   **Positive**: Higher consistency as the "standard" is now a copy-pasteable configuration file.
*   **Positive**: Faster development speed (no custom CSS needed to force Material looks).
*   **Negative**: We lose the "familiarity" of Google's specific Material Design patterns, though shadcn is standard enough that users will adapt instantly.
