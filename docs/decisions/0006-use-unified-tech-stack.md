# 6. Use Unified Tech Stack

Date: 2025-12-21

## Status

Accepted

## Context

We are building a suite of products. To allow developers (and AI agents) to move seamlessly between projects, and to reduce the cognitive load of decision-making for every new service, we need a "default" technology stack.
Fragmentation in languages and frameworks leads to:
- Slower onboarding.
- Duplicated tooling (linting, CI/CD).
- Difficulty in sharing code/types between services.
- Reduced effectiveness of AI coding assistants (which benefit from consistent patterns).

## Decision

We will adopt a **Unified Tech Stack** as the default for all new applications in this product suite.
This stack consists of the specific technologies chosen in separate ADRs:

*   **Styling**: Tailwind CSS ([ADR-0002](./0002-use-tailwind-css.md))
*   **UI Components**: shadcn/ui ([ADR-0003](./0003-use-shadcn-ui.md))
*   **Backend API**: Python FastAPI ([ADR-0004](./0004-use-python-fastapi.md))
*   **Client Framework**: React Native w/ Expo ([ADR-0005](./0005-use-react-native-expo.md))

Exceptions to this default must be justified by a specific business or technical requirement and documented in a new ADR.

## Consequences

*   **Positive**: "Batteries included" start for new projects.
*   **Positive**: Shared knowledge base and patterns.
*   **Negative**: Less flexibility for developers who prefer other tools (e.g., pure React, Go).
