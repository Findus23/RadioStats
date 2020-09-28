from abc import ABC, abstractmethod
from datetime import datetime
from typing import Tuple, Iterable

from models import Channel


class BaseFetcher(ABC):
    @abstractmethod
    def get(self, channel: Channel) -> Iterable[Tuple[datetime, str, str]]:
        pass
