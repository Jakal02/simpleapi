"""
Define PyDantic data schemas.
"""
from pydantic import BaseModel, PositiveInt

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
