# 2. Use Tailwind CSS for Styling

Date: 2025-12-21

## Status

Accepted

## Context

We need a consistent way to style web applications across multiple products.
The team desires high-quality, "premium" design but lacks dedicated design resources.
Previous approaches involving adopting pre-made templates (Bootstrap) often result in "messy adapted code" when customization is required.
We need a solution that allows for rapid development, consistency, and easy manipulation by AI agents.

## Decision

We will use **Tailwind CSS** as our primary styling framework.

*   **Utility-First**: We will style components using utility classes directly in the markup.
*   **Headless Components**: For complex interactive components (modals, dropdowns), we will prefer "headless" libraries (like Radix UI or Headless UI) styled with Tailwind, or copy-paste collections like **shadcn/ui**.
*   **No Global CSS**: We will avoid writing custom CSS files except for global resets or specific animations not covered by the config.

## Consequences

*   **Positive**: High consistency across projects via shared `tailwind.config.js`.
*   **Positive**: AI Agents are very proficient at generating valid Tailwind classes.
*   **Positive**: Eliminates the "messy CSS" problem of appended stylesheets and overriding rules.
*   **Negative**: HTML markup becomes verbose (many classes per element).
*   **Mitigation**: We will use component-based architectures (React/Vue/WebComponents) to encapsulate this verbosity.
