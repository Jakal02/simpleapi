"""
Define PyDantic data schemas.
"""
from datetime import datetime
from pydantic import BaseModel, PositiveInt
from pydantic import PlainSerializer
from pydantic.type_adapter import TypeAdapter
from typing_extensions import Annotated


MyDateTime = Annotated[datetime, PlainSerializer(lambda x: x.isoformat(), return_type=str)]

class CreatePost(BaseModel):
    """
    Information needed to create a post.
    """
    title: str
    body: str


class RetrievePost(CreatePost):
    """
    Information returned when a post is retrieved.
    """
    id: PositiveInt
    date_modified: MyDateTime
    is_deleted: bool

    model_config = {
        "from_attributes": True,
    }

post_serializer = TypeAdapter(type=RetrievePost)
