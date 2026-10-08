from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from src.database import database
from src.routes import auth, messages, orders, products, settings, social_media_links, storefronts, users


def create_app():
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        yield
        if database._engine is not None:
            await database.close()

    app = FastAPI(title="ceynic API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth.router)
    app.include_router(messages.router)
    app.include_router(orders.router)
    app.include_router(products.router)
    app.include_router(settings.router)
    app.include_router(social_media_links.router)
    app.include_router(storefronts.router)
    app.include_router(users.router)

    return app


app = create_app()
