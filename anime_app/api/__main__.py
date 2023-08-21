import uvicorn

from fastapi import FastAPI

from anime_app.api.routes import setup_routers
from anime_app.api.dependencies import setup_dependencies
from anime_app.api.config.parser.main import load_config
from anime_app.infrastructure.db.factory import create_pool
from anime_app.api.main_factory import create_app, get_paths
from anime_app.api.dependencies.db import DBProvider
from anime_app.api.dependencies.auth import AuthProvider
from anime_app.core.utils.exception_handlers import setup_exception_handlers


def main() -> FastAPI:
    paths = get_paths()
    auth = AuthProvider()

    config = load_config(paths)
    app = create_app()
    pool = create_pool(config.db)
    db = DBProvider(pool=pool)

    setup_routers(app)
    setup_dependencies(app, auth, db)
    setup_exception_handlers(app)

    return app


def run():
    uvicorn.run('anime_app.api:main', reload=True, host='0.0.0.0', port=80)


if __name__ == '__main__':
    run()
