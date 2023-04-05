from pydantic import BaseModel, Field


class UserResponseWithToken(BaseModel):
    msg: str = Field()
    # token: str = Field()
    user_type: str = Field()
