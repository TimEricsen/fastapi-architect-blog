from anime_app.common.config.parser.main import load_config as load_common_config
from anime_app.common.config.parser.config_file_reader import read_config
from anime_app.common.config.models.paths import Paths
from anime_app.api.config.models.main import ApiConfig


def load_config(paths: Paths) -> ApiConfig:
    config_dict = read_config(paths)
    return ApiConfig.from_base(
        base=load_common_config(config_dict, paths)
    )
