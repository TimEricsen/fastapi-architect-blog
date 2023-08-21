from dataclasses import dataclass

from anime_app.common.config.models.main import Config


@dataclass
class ApiConfig(Config):

    @classmethod
    def from_base(cls, base: Config):
        return cls(
            paths=base.paths,
            db=base.db
        )
