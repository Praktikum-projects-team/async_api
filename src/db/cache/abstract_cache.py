import abc
from typing import Any, Union

from models.base import BaseApiModel


class AbstractCache(abc.ABC):

    @abc.abstractmethod
    async def set_cache(
            self,
            /,
            key_name: str,
            value: Union[BaseApiModel, list[BaseApiModel]],
            key_extra: dict[str: Any] = None,
            ttl: int = None
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_cache(
            self,
            /,
            key_name: str,
            key_extra: dict[str: Any] = None,
    ) -> Union[dict, list[dict]]:
        raise NotImplementedError
