# 8. Use PostgreSQL for Primary Storage & AI

Date: 2025-12-21

## Status

Accepted

## Context

We need a database that effectively handles:
1.  Relational data (users, orders, relational integrity).
2.  JSON documents (flexible schemas for rapid prototyping).
3.  **Vector Embeddings**: For future LLM/AI features (semantic search, RAG).

Managing multiple specialty databases (e.g., Postgres + Mongo + Pinecone) introduces distributed transaction headaches and high operational complexity.

## Decision

We will use **PostgreSQL** as our primary persistence layer.

*   **Relational**: Standard normalized tables for core data.
*   **Vector Search**: We will use the `pgvector` extension for storing and querying embeddings.
*   **Search**: We will use `pg_trgm` for fuzzy text search until dedicated search infrastructure (Elasticsearch) is strictly required.

## Consequences

*   **Positive**: ACID compliance for all data transactions.
*   **Positive**: "One DB to rule them all" simplifies backups, local dev, and testing.
*   **Positive**: Seamless joining of relational data with vector similarity results (e.g., "Find similar documents created by User X").
*   **Negative**: Postgres vector search may be slower than specialized vector DBs at massive scale (100M+ vectors), but sufficient for <10M scale.
