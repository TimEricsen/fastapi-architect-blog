from dataclasses import dataclass
from pathlib import Path


@dataclass
class Paths:
    app_dir: Path

    @property
    def config_path(self) -> Path:
        return self.app_dir / 'config_dist'
