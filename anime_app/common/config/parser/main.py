from anime_app.common.config.models.paths import Paths
from anime_app.common.config.models.main import Config
from anime_app.infrastructure.db.config.parser.db import load_db_config


def load_config(config_dict: dict, paths: Paths) -> Config:
    return Config(
        paths=paths,
        db=load_db_config(config_dict['db'])
    )
