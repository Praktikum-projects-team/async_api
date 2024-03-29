import abc
from typing import Optional

from api.v1.utils import Page
from db.fulltext.abstract_indices.base_index import AbstractFulltextIndex
from models.base_model import BaseServiceModelChild


class BaseService(abc.ABC):
    def __init__(self, index: AbstractFulltextIndex):
        self.index = index

    async def get_by_id(self, obj_id: str) -> Optional[BaseServiceModelChild]:
        obj = await self.index.get_by_id(obj_id)
        return obj

    async def get_all(self, page: Page) -> Optional[list[BaseServiceModelChild]]:
        obj = await self.index.get_all(page_from=page.page_from, page_size=page.page_size)
        return obj

    async def search(self, query: str, page: Page, sort: str = None) -> Optional[list[BaseServiceModelChild]]:
        obj = await self.index.search(
            raw_query=query,
            sort=sort,
            page_size=page.page_size,
            page_from=page.page_from
        )
        return obj
