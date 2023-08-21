from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DBConfig:
    type: str | None = None
    connector: str | None = None
    host: str | None = None
    port: int | None = None
    login: str | None = None
    password: str | None = None
    name: str | None = None

    @property
    def uri(self):
        if self.type != 'postgresql':
            raise ValueError('DB type is not valid for this application!')
        url = (f'{self.type}+{self.connector}://'
               f'{self.login}:{self.password}'
               f'@{self.host}:{self.port}/{self.name}')
        return url
