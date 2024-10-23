from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqladmin import Admin

from .core.config import settings
from .db.session import get_async_engine
from .db.session import create_async_session_maker
from .admin.model_views import get_model_views
from .admin.auth import authentication_backend
from .exception_handlers import exception_handlers

# Routers
from .auth.router import router as auth_router
from .tournaments.router import router as tournaments_router
from .events.router import router as events_router
from .socials.router import router as socials_router


# App configuration
app = FastAPI(
    title=settings.app_name,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount media and static directories
app.mount(
    settings.media_url,
    StaticFiles(directory=settings.media_root),
    name=settings.media_mount_name,
)
app.mount(
    settings.static_url,
    StaticFiles(directory=settings.static_root),
)

# Include routers
ROUTERS: list[APIRouter] = [
    auth_router,
    tournaments_router,
    events_router,
    socials_router,
]
for router in ROUTERS:
    app.include_router(router, prefix=f"/api/v{settings.app_version}")

# Include custom exception handlers
for exc_cls, handler in exception_handlers():
    app.add_exception_handler(exc_cls, handler)

# Admin panel
admin = Admin(
    app,
    engine=get_async_engine(),
    session_maker=create_async_session_maker(),
    authentication_backend=authentication_backend,
)
for model_view in get_model_views():
    admin.add_view(model_view)
