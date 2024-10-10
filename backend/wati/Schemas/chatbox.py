
from pydantic import BaseModel, Field
from typing import Optional

class WebhookData(BaseModel):
    messaging_product: str
    phone_number_id: str
    wa_id: str
    message_id: str
    # text=payload.body,  # Use 'text' as the alias

    message_content: str = Field(alias="text")  # Alias 'text' for incoming data
    timestamp: int
    context_message_id: Optional[str] = Field(None)
    message_type: str
    message_type="text"
    direction: Optional[str] = None  # Could be "sent" or "received"

    is_first_message: bool = False  # Indicates if it's the first message in the conversation

# Define Pydantic model for the payload
class MessagePayload(BaseModel):
    phone_number_id: str
    wa_id: str
    body: str
    access_token: str
