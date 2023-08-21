from fastapi import FastAPI

from anime_app.common.config.models.paths import Paths
from anime_app.common.config.parser.paths import common_get_paths


def create_app():
    return FastAPI()


def get_paths() -> Paths:
    return common_get_paths('API_PATH')
