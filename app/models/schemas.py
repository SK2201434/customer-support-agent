from pydantic import BaseModel


class CustomerSupportRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: str


class CustomerSupportResponse(BaseModel):
    message: str
    conversation_id: str