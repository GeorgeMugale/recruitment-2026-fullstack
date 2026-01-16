from pydantic import BaseModel
from typing import List


class ConstituencyResponse(BaseModel):
    province: str
    constituencies: List[str]
    
# Define the Pydantic models to match Swagger documentation exactly to show specific structures in OpenAPI documentation
class ProvinceConstituencyResponse(BaseModel):
    constituency: str
    province: str

class ValidationErrorItem(BaseModel):
    loc: List[str]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: List[ValidationErrorItem]