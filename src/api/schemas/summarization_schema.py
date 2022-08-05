from typing import Optional
from pydantic import BaseModel

class Summarization(BaseModel):
    url: Optional[str]
    text: Optional[str]
    language: str