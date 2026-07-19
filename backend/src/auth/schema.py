from uuid import UUID  # Import the capital UUID type
from pydantic import BaseModel, EmailStr

# Details API needs to create a user
class UserInfo(BaseModel):
    email: EmailStr
    username: str
    password: str

# What we can safely send to the frontend
class UserResponse(BaseModel):
    id: UUID          # Fixed: Use UUID class type instead of the lower module name
    username : str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

# The Token schema returned on successful login DEFINED BY OAUTH2
class TokenSchema(BaseModel):
    access_token: str
    token_type: str