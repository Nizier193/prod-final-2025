from fastapi import APIRouter

from .clients.router        import router as client_router
from .advertisers.router    import router as advertisers_router
from .campaigns.router      import router as campaigns_router
from .ads.router            import router as ads_router
from .advertisers.router    import mlscore_router
from .time.router           import router as time_router
from .statistics.router     import router as statisctics_router
from .images.router         import router as images_router
from .moderation.router     import router as moderation_router

# Список роутеров с префиксами
routers = [
    (client_router,      "/clients"),
    (advertisers_router, "/advertisers"),
    (mlscore_router,     ""),
    (campaigns_router,   "/advertisers"),
    (ads_router,         "/ads"),
    (time_router,        "/time"),
    (statisctics_router, "/stats"),
    (images_router,      "/images"),
    (moderation_router,  "/moderation"),
]

endpoints = APIRouter()

# Автоматическое добавление роутеров
for router, prefix in routers:
    endpoints.include_router(router, prefix=prefix)

__all__ = ["endpoints"]