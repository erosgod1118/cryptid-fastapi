from pydantic import BaseModel, validator, EmailStr, Field

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, description="The password cannot be empty")

class UserSignupRequest(BaseModel):
    full_name: str = Field(..., min_length=1, description="The full name cannot be empty")
    email: EmailStr 
    password: str = Field(..., min_length=1, description="The password cannot be empty")
    confirm_password: str = Field(..., min_length=1, description="The confirm password cannot be empty")

    @validator("confirm_password")
    def verify_password_match(cls, v, values):
        password = values.get("password")

        if v != password:
            return ValueError("The two passwords do not match")

        return v 