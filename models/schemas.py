from pydantic import BaseModel, Field, WithJsonSchema
from typing import Optional, Annotated
from fastapi import UploadFile


# left alone as a template
# class pdf2image_range_schema(BaseModel):
#     start: int = Field(gt=0)
#     end: Optional[int] = None

CustomUploadFile = Annotated[
    UploadFile, 
    WithJsonSchema({"type": "string", "format": "binary"})
]