from pydantic import BaseModel


class AccountResponseSchema(BaseModel):
    id: int
    name: str
    region: str
    has_account_setup: bool

    class Config:
        from_attributes = True


class AccountCreateRequestSchema(BaseModel):
    name: str
    access_key: str
    secret_key: str
    region: str
    session_key: str
