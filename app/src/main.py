    import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers.base import api_router
from cscs_tools.version.services.version_service import VersionService


description = """
# ML REST API 🚀
"""


def start_app():
    version_service = VersionService()

    application = FastAPI(
        description=description,
        version=version_service.get_version().str_repr(),
    )
    application.include_router(api_router)
    return application


app = start_app()

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(os.path.join(static_path, "index.html"))
