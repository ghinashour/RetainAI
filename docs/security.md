# Security

## Current Phase 1 security posture

The foundation deliberately includes configuration and architecture needed for secure production design, but does not yet implement the full authentication and authorization system.

## Included in Phase 1

- centralized settings management via environment variables
- JWT secret configuration
- password hashing abstraction using passlib
- JWT token creation/validation abstraction
- tenant-aware service interfaces placeholder
- no hardcoded secrets
- structured exception handling
- secure response patterns that avoid exposing stack traces or internals

## Required future security controls

- registration and login flow
- refresh token rotation strategy
- role-based authorization
- organization-level scoping for every resource
- audit logs for security and business-critical actions
- input validation on all requests
- file validation and size limits for CSV uploads
- rate limiting
- secure CORS configuration
- structured logging without credential leakage

## Multi-tenant rule

The frontend must never determine organization identity. The backend must derive tenant context from the authenticated user.

## Not implemented yet

- full auth service
- user/role tables
- access-control enforcement
- audit logging tables and APIs
