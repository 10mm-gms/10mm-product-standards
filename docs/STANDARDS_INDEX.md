# Product Standards Index

This index classifies all Architecture Decision Records (ADRs) and Product Standards by domain to allow agents to accurately filter relevant rules for a given task.

## Domains

### UI / Frontend
*Focus: Visual design, user interaction, branding, web and mobile styling.*
*   **ADRs**:
    *   [ADR-0002: Use Tailwind CSS](decisions/0002-use-tailwind-css.md)
    *   [ADR-0003: Use shadcn/ui](decisions/0003-use-shadcn-ui.md)
    *   [ADR-0005: Adopt 10mm GMS Design System](decisions/0005-adopt-10mm-design-system.md) (Colors, Fonts)
    *   [ADR-0005-Mobile: Use React Native Expo](decisions/0005-use-react-native-expo.md)
*   **Standards**:
    *   [Style Standard](standards/style.md) (Standardized components and visual language)
    *   [Coding Guidelines](standards/coding-guidelines.md) (Frontend sections)

### Backend / API
*Focus: Business logic, API contracts, data validation, service architecture.*
*   **ADRs**:
    *   [ADR-0004: Use Python FastAPI](decisions/0004-use-python-fastapi.md)
    *   [ADR-0007: Modular Monolith Architecture](decisions/0007-modular-monolith-architecture.md)
    *   [ADR-0009: Enforce Stateless Services](decisions/0009-enforce-stateless-services.md)
*   **Standards**:
    *   [API Standards](standards/api-standards.md) (RFC 7807, Versioning)
    *   [Coding Guidelines](standards/coding-guidelines.md) (Python/FastAPI specific rules)

### Data / Persistence
*Focus: Database schema, storage, migrations.*
*   **ADRs**:
    *   [ADR-0008: Use PostgreSQL for Primary DB](decisions/0008-use-postgresql-for-primary-db.md)
*   **Standards**:
    *   [Architecture Standard](standards/architecture.md) (Database patterns)

### QA / Reliability
*Focus: Testing strategy, observability, logging.*
*   **ADRs**:
    *   [ADR-0010: Comprehensive Testing Strategy](decisions/0010-comprehensive-testing-strategy.md)
    *   [ADR-0011: Observability Strategy](decisions/0011-observability-strategy.md)
    *   [ADR-0014: Logging Implementation & Strategies](decisions/0014-logging-implementation-strategies.md)
    *   [ADR-0015: Repository Structure & Testing Hierarchy](decisions/0015-repository-structure-and-organization.md)
*   **Standards**:
    *   [Testing & Traceability](standards/testing-traceability.md)
    *   [Security Testing](standards/security-testing.md)

### DevOps / Infrastructure
*Focus: CI/CD, deployment, environment management.*
*   **ADRs**:
    *   [ADR-0012: App Execution Standards](decisions/0012-app-execution-standards.md)
    *   [ADR-0016: Adopt Semantic Versioning](decisions/0016-adopt-semantic-versioning.md)
    *   [ADR-0017: Standard Environment Variable Naming](decisions/0017-standard-environment-variable-naming.md)
*   **Standards**:
    *   [CI/CD Standard](standards/cicd.md)
    *   [Infrastructure Standard](standards/infrastructure.md)
    *   [Monitoring Standard](standards/monitoring.md)

### Process / Governance
*Focus: Legal, language, workflows, project management.*
*   **ADRs**:
    *   [ADR-0001: Record Architecture Decisions](decisions/0001-record-architecture-decisions.md)
    *   [ADR-0006: Use Unified Tech Stack](decisions/0006-use-unified-tech-stack.md)
    *   [ADR-0013: Standardise UK English](decisions/0013-standardise-uk-english.md)
    *   [ADR-0018: Shared Libraries Management](decisions/0018-shared-libraries-management.md)
*   **Standards**:
    *   [Agile Workflow](standards/agile-workflow.md)
    *   [Git Workflow](standards/git-workflow.md)
    *   [Requirements Standard](standards/requirements.md)
