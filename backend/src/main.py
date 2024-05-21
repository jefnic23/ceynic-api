from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.src.routes import products


def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(products.router)

    # app.mount("/", StaticFiles(directory="build/", html=True), name="static")

    # @app.get("/")
    # def index():
    #     return app.send_static_file("index.html")  # type: ignore

    return app


app = create_app()
