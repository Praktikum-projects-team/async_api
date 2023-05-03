import abc
from typing import Any, Optional


class AbstractFulltextSearch(abc.ABC):

    @abc.abstractmethod
    async def get_by_id(self, index_name: str, id: Any) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    async def search_many(
            self,
            index_name: str,
            query: Any,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[dict]:  # TODO: divide on search(...) and get_by_field(...)
        raise NotImplementedError
