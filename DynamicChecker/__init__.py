from pydantic import BaseModel, Json
from typing import Optional
from .DescChecker import Desc
from .CardChecker import Card
from .DisplayChecker import Display
from .ExtendJsonChecker import ExtendJson


class Dynamic(BaseModel):
    card: Json[Card]
    desc: Desc
    display: Optional[Display]
    # extend_json: Json[ExtendJson]


