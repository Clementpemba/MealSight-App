from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from contextlib import asynccontextmanager

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

@asynccontextmanager

async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    # Create tables (use Alembic migrations in production)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


def _error_code_from_status(status_code: int) -> str:
    mapping = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR",
    }
    return mapping.get(status_code, "ERROR")


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    status_code = exc.status_code
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
            "error_code": _error_code_from_status(status_code),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_, __):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR",
        },
    )

# CORS middleware
# CORS configuration: allow all origins when wildcard is used (mobile clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
async def root():
    """Welcome root endpoint."""
    return {"message": f"Welcome to {settings.PROJECT_NAME}", "version": settings.VERSION}

# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000