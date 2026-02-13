# 4. Use Python (FastAPI) for Backend Services

Date: 2025-12-21

## Status

Accepted

## Context

We are building a suite of products that may require future AI/Data integration.
The primary developer has significant experience in Perl and Java, making Python a natural bridge (scripting flexibility + strong typing support).
We need a framework that adheres to our API-First standard (OpenAPI generation) and is highly performant.

## Decision

We will use **Python** with the **FastAPI** framework for backend services.

*   **Language**: Python 3.12+
*   **Framework**: FastAPI
*   **Type Safety**: We enforce strict type hints (mypy/pyright) to mimic strong typing.
*   **ORM**: SQLModel or SQLAlchemy (Async).
*   **Package Manager**: `uv` (modern, extremely fast replacement for pip/poetry).

## Consequences

*   **Positive**: Native ecosystem for AI/LLM libraries.
*   **Positive**: Automatic OpenAPI (Swagger) documentation generation.
*   **Positive**: High developer velocity.
*   **Negative**: Lower raw execution speed than Go/Rust (usually negligible for I/O bound web apps).
*   **Mitigation**: Use `uvicorn` with `gunicorn` for production concurrency.
