from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import Broadcast  
from typing import Any, Dict
import httpx

def get_template_by_id(db: Session, template_id: str):
    return db.query(Broadcast.Template).filter(Broadcast.Template.id == template_id).first()

async def send_template_to_whatsapp(template: dict , access_token: str, business_account_id: str) -> Dict[str, Any]:
    url = f"https://graph.facebook.com/v14.0/{business_account_id}/message_templates"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "allow_category_change": True,
        "category": template.get('category'),
        "components": [comp for comp in template.get('components', [])],
        "language": template.get('language'),
        "name": template.get('name'),
        "sub_category": template.get('sub_category')
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()