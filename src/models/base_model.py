from typing import TypeVar
from pydantic import BaseModel

BaseServiceModelChild = TypeVar("BaseServiceModelChild", bound="BaseModel")  # for type hints
