from fastapi import APIRouter

from app.api.v1.actions.routes import router as actions_router
from app.api.v1.analytics.routes import router as analytics_router
from app.api.v1.assistant.routes import router as assistant_router
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.customers.routes import router as customers_router
from app.api.v1.dashboard.routes import router as dashboard_router
from app.api.v1.health import router as health_router
from app.api.v1.interventions.routes import router as interventions_router
from app.api.v1.outcomes.routes import router as outcomes_router
from app.api.v1.recommendations.routes import router as recommendations_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health_router, tags=["health"])
api_v1_router.include_router(auth_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(customers_router)
api_v1_router.include_router(actions_router)
api_v1_router.include_router(interventions_router)
api_v1_router.include_router(outcomes_router)
api_v1_router.include_router(recommendations_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(assistant_router)
