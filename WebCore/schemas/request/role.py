from pydantic import BaseModel, Field


class RoleSchema(BaseModel):
    name: str = Field(default=None)
