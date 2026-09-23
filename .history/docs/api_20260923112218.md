# API design

## Current API

Implemented:

- GET /api/v1/health
- GET /api/v1/health/db

## Versioning

All routes are namespaced under /api/v1 to keep the API evolvable without breaking the frontend.

## Security rules

- Sensitive errors are not exposed
- Validation errors are normalized into structured JSON
- Database credentials and secrets are never returned in HTTP responses

## Future endpoints planned

- /api/v1/auth/register
- /api/v1/auth/login
- /api/v1/auth/refresh
- /api/v1/organizations
- /api/v1/customers
- /api/v1/data-sources
- /api/v1/imports
- /api/v1/predictions
- /api/v1/risk
- /api/v1/recommendations
- /api/v1/interventions
- /api/v1/outcomes
- /api/v1/analytics
- /api/v1/audit

## Response contract

The API returns structured error payloads in this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {}
  }
}
```

## Not implemented yet

- JWT login flow
- authorization middleware
- tenancy-aware access validation
- customer-centric endpoints
- prediction routes
- product workflows
