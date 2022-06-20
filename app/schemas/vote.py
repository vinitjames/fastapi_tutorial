from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
    
    
