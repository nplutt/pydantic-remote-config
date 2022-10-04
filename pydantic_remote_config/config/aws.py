from typing import Optional

from pydantic import BaseModel


class AWSConfig(BaseModel):
    region: Optional[str] = None
