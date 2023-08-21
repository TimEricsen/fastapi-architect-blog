import os

from pathlib import Path
from dotenv import load_dotenv

from anime_app.common.config.models.paths import Paths


def common_get_paths(env_var: str) -> Paths:
    load_dotenv()
    if path := os.getenv(env_var):
        return Paths(Path(path))
    return Paths(Path(__file__).parent.parent.parent.parent.parent)
