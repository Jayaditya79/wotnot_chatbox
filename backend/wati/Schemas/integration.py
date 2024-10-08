from pydantic import BaseModel,Json
from datetime import datetime
from typing import List



class Parameter(BaseModel):
    key: str

class wooIntegration(BaseModel):
    template_id:str
    parameters:List[Parameter]
    type:str
