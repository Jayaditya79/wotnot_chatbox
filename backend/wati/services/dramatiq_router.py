

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from dramatiq import Message
from fastapi import APIRouter, Depends, HTTPException
from ..models import Broadcast
from ..Schemas import broadcast, user
from ..oauth2 import get_current_user
from .tasks import send_broadcast
from datetime import datetime, timezone
import pytz
from sqlalchemy.orm import  Session
from dramatiq import Actor
from dramatiq import Message
from dramatiq.middleware import Middleware,SkipMessage
from ..database import database
router = APIRouter()


# custom middleware to delete the task



@router.post("/schedule-template-message/")
async def schedule_template_message(
    request: broadcast.input,
    # request: broadcast.input,
    db: Session = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user)

):
    contacts = [{"name": contact.name, "phone": contact.phone} for contact in request.recipients]
    
    broadcastList=Broadcast.BroadcastList(
        user_id=get_current_user.id,
        name=request.name,
        template=request.template,
        contacts=[contact.phone for contact in request.recipients],
        type=request.type,
        success=0,
        failed=0,
        status="Scheduled",
        scheduled_time=request.scheduled_time
        
    )
    db.add(broadcastList)
    db.commit()
    db.refresh(broadcastList)

    saved_broadcast_id = broadcastList.id


    """
    Endpoint to schedule a template message to be sent at a specified time.
    """
    API_url = f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {get_current_user.PAccessToken}",
        "Content-Type": "application/json"
    }

    # Convert 'scheduled_time' string to a datetime object
    try:
        scheduled_datetime = datetime.fromisoformat(request.scheduled_time).replace(tzinfo=timezone.utc)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use ISO 8601 format.")

    now = datetime.now(timezone.utc)  # Current time in UTC
    delay = (scheduled_datetime - now).total_seconds()

    if delay < 0:
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future.")

    # Ensure all necessary parameters are passed to send_broadcast
    if not request.body_parameters or not request.image_id:
        raise HTTPException(status_code=400, detail="Missing required body parameters or image ID.")
    
    # Schedule the task with the calculated delay and capture the task object
    task: Message = send_broadcast.send_with_options(
        args=[request.template, contacts,saved_broadcast_id,API_url, headers,get_current_user.id,request.image_id,request.body_parameters],
        delay=delay * 1000  # delay is in milliseconds
    )
    
    broadcastLogTaskid=db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.id==saved_broadcast_id).first()

    if not broadcastLogTaskid:
        raise HTTPException(status_code=404,detail="Broadcast not found")
    
    if saved_broadcast_id:
        broadcastLogTaskid.task_id=task.message_id
    db.add(broadcastLogTaskid)
    db.commit()
    db.refresh(broadcastLogTaskid) 


    # Return the message indicating the task was scheduled and include the task ID
    return {
        "message": f"Message {saved_broadcast_id}scheduled to be sent at {request.scheduled_time}.",
        "task_id": task.message_id  # Access the message_id attribute to get the task ID
    }
