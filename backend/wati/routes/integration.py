from fastapi import APIRouter,Depends,HTTPException, File, UploadFile,Request
from ..models import Broadcast,Contacts,Integration
from ..Schemas import broadcast,user
from ..database import database
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
import json
from fastapi.responses import JSONResponse
import csv
import io
from ..oauth2 import get_current_user
from dramatiq import get_broker
from dramatiq import Message
from ..crud.template import send_template_to_whatsapp
from ..services import tasks




router=APIRouter(tags=["Integration"])



@router.get("/integration/list")
def integrationlist(db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    integrationList=db.query(Integration.Integration).filter(Integration.Integration.user_id==get_current_user.id).order_by(Integration.Integration.user_id.desc()).all()

    if not integrationList:
        raise HTTPException(status_code=404,detail="No integation exists for the current user")
    
    return integrationList

@router.delete("/integration/{id}")
def deleteIntegration(
    id: str, 
    db: Session = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user)
):
    # Find the WooIntegration object
    woo_integration = db.query(Integration.WooIntegration).filter(
        (Integration.WooIntegration.integration_id == id) &
        (Integration.WooIntegration.user_id == get_current_user.id)
    ).first()

    if not woo_integration:
        raise HTTPException(status_code=404, detail="Woocommerce Integration not found")

    # Delete WooIntegration object
    db.delete(woo_integration)
    db.commit()

    # Find the Integration object
    integration = db.query(Integration.Integration).filter(
        (Integration.Integration.id == id) &
        (Integration.Integration.user_id == get_current_user.id)
    ).first()

    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")

    # Delete the Integration object
    db.delete(integration)
    db.commit()

    # No need to refresh after deletion
    return {"detail": f"Successfully deleted Integration with id: {id}"}
