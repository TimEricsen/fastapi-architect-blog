from fastapi import FastAPI

from anime_app.api.dependencies.auth import get_current_user, get_current_user_or_pass, AuthProvider
from anime_app.api.dependencies.db import DBProvider, dao_provider


def setup_dependencies(app: FastAPI, auth: AuthProvider, db: DBProvider):
    app.dependency_overrides[get_current_user] = auth.get_current_user
    app.dependency_overrides[get_current_user_or_pass] = auth.get_current_user_or_pass
    app.dependency_overrides[dao_provider] = db.dao
