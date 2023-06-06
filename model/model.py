from pydantic import BaseModel
from typing import Optional


class RequestParams(BaseModel):
    filter: str = ""
    location: str = ""
    fulltime: Optional[str] = None
