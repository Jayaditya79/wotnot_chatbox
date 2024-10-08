from pydantic import BaseModel,HttpUrl,Field
from typing import List, Optional
from datetime import datetime
from fastapi import  File, UploadFile

class Contact(BaseModel):
    name: str = Field(..., example="John Doe")
    phone: str = Field(..., example="+1234567890")

class input(BaseModel):
    name:str
    recipients: List[Contact]
    template:str
    status:str
    scheduled_time:str
    type:str
    image_id:Optional[str] = None 
    body_parameters: str = None




class input_broadcast(BaseModel):
    recipients: List[Contact]
    template:str
    status:str
    name:str
    type:str
    image_id:Optional[str] = None 
    body_parameters: str = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "New Year Campaign",
                "template": "new_year_template",
                "type": "Broadcast",
                "recipients": [
                    {"name": "John Doe", "phone": "+1234567890"},
                    {"name": "Jane Smith", "phone": "+0987654321"}
                ],
                "image_id": "123456789",
                "body_parameters": ["param1", "param2"]
            }
        }
    

class BroadcastListCreate(BaseModel): 
    name:str
    template:str
    type:str
    contacts:list[str]
    success:int
    failed:int
    status:str
    scheduled_time: Optional[datetime] = None  # Optional, as it could be null
    task_id: Optional[str] = None 

class BroadcastListUpdate(BaseModel): 
    task_id: Optional[str] = None 

# class BroadcastAnalysis(BaseModel):
#     id:int 
#     broadcast_id:int
#     message_id:str
#     phone_no:str
#     read:bool
#     delivered:bool
#     sent:bool

    


class Button(BaseModel):
    type: str = Field(..., description="The type of the button, e.g., 'URL' or 'QUICK_REPLY'")
    text: str = Field(..., description="The text of the button")
    url: Optional[HttpUrl] = None
class Component(BaseModel):
    type: str
    format: Optional[str] = None  # Allowed only for certain component types
    text: Optional[str] = None
    buttons: Optional[List[Button]] = None  # Optional list of Button objects
    @classmethod
    def validate_component(cls, component: dict):
        # Ensure 'BODY' type component does not have 'format' field
        if component['type'] == 'BODY':
            component.pop('format', None)  # Remove the format field if it exists
        # Ensure 'BODY' type component has 'text' field
        if component['type'] == 'BODY' and not component.get('text'):
            raise ValueError("Component of type BODY must have 'text' field")
        # Validate buttons if present
        if component.get('buttons'):
            for button in component['buttons']:
                Button(**button)  # Validate using the Button model
class TemplateCreate(BaseModel):
    name: str
    category: str
    components: List[Component]
    language: str
    sub_category: Optional[str] = None
    @classmethod
    def validate_template(cls, template: dict):
        for component in template.get('components', []):
            Component.validate_component(component)
class TemplateResponse(BaseModel):
    id: str
    status: str
    category: str

class uploadMedia(BaseModel):
    File:UploadFile