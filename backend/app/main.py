from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.modules.catalog_items import init_module as init_catalog_items_module
from app.modules.catalog_items import router as catalog_items_router
from app.modules.clients import init_module as init_clients_module
from app.modules.clients import router as clients_router
from app.modules.users import init_module as init_users_module
from app.modules.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("app.startup")
    try:
        init_clients_module()
        init_catalog_items_module()
        init_users_module()
    except Exception:
        logger.exception("Startup initialization failed")
        raise
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.app_env)

    app = FastAPI(title="Invoicer API", lifespan=lifespan)

    origins = settings.cors_origin_list()
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        if isinstance(exc, HTTPException):
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        logging.getLogger("app.error").exception("Unhandled exception")
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    app.include_router(clients_router)
    app.include_router(catalog_items_router)
    app.include_router(users_router)

    return app


app = create_app()
