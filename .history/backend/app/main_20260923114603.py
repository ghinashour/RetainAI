from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import RetainAIError
from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware

settings = get_settings()
logger = setup_logging()

app = FastAPI(
    title="RetainAI API",
    description="RetainAI SaaS foundation for retention intelligence and customer health workflows.",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RetainAIError)
async def retainai_exception_handler(request: Request, exc: RetainAIError):
    logger.warning("application_error", extra={"path": request.url.path, "code": exc.code, "message": exc.message})
    status_code = 501 if exc.code == "NOT_IMPLEMENTED" else 400
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": {},
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("validation_error", extra={"path": request.url.path, "details": exc.errors()})
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "RetainAI API is running"}


app.include_router(api_v1_router)
