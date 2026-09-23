# Database design

## Current state

Phase 1 intentionally does not implement the full product database yet. The foundation establishes the SQLAlchemy and PostgreSQL-ready environment and the domain-oriented folder structure for future models.

## Current foundation

- SQLAlchemy engine and session factory configured
- Base model class available
- domain structure prepared for future modules:
  - auth
  - organization
  - customer
  - data
  - risk
  - intervention
  - audit
  - model

## Future multi-tenant model requirements

Each future table for organization-owned data must include:

- id
- organization_id
- created_at
- updated_at

## Security rule

Cross-tenant access must be blocked by service-layer authorization checks. The frontend must never be trusted to provide organization identity.

## Migration approach

Alembic is configured as the migration tool for the backend project.

## Planned database domains

- auth
- organization
- customer
- data ingestion
- risk and prediction
- intervention
- audit
- model registry

## Not yet implemented

- full schema migration set
- actual domain tables
- tenant-aware user table
- organization table
- customer table
- import + validation tables
