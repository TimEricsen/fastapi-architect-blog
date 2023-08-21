from .paths import Paths

from dataclasses import dataclass

from anime_app.infrastructure.db.config.models.db import DBConfig


@dataclass
class Config:
    paths: Paths
    db: DBConfig

    @property
    def config_path(self):
        return self.paths.config_path
