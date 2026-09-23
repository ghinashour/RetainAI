# Architecture

## Overview

RetainAI is being built as a modular monolith for the initial product phase. This means one application deployable as a combined system but structured by business domain.

## Current Phase 1 foundation

Implemented foundation:

- API versioning under /api/v1
- backend application shell
- SQLAlchemy session management
- PostgreSQL-ready configuration
- centralized logging and exception handling
- domain-oriented folder layout
- frontend app shell
- Docker development composition

## Planned architecture later

The finalized architecture remains:

Data Sources
→ Ingestion
→ Validation
→ Normalization
→ Canonical Customer/Event Model
→ Feature Engineering
→ ML/Health Engine
→ Risk Explanation
→ Recommendation
→ Human Decision
→ Intervention
→ Outcome
→ ROI Analytics

## Multi-tenancy design rule

All future organization-owned resources must be scoped to an organization and must derive tenant context from the authenticated user, never from the frontend.

## Relationship model

- User belongs to Organization
- Customer belongs to Organization
- Subscription belongs to Organization and Customer
- Data imports and validation runs belong to Organization
- Prediction and recommendation belong to Organization and Customer
- Intervention belongs to Organization and Customer
- Outcome belongs to Organization and Customer

## Status

IMPLEMENTED:

- foundation only

PLANNED:

- onboarding workflows
- authentication system
- customer import and validation
- churn modeling and health scoring
- intervention tracking
- analytics

FUTURE:

- CRM integrations
- Stripe and billing
- AI assistant
- complex monitoring
