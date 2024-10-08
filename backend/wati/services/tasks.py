import dramatiq
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dramatiq import Middleware
from ..models import Broadcast  # Adjust this import as needed based on your project structure
import requests
import json
from dramatiq.middleware import Middleware,SkipMessage
from fastapi import HTTPException


# SQLAlchemy Database Configuration
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Jayadityapgadmin$@localhost:7903/watnot'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Denmarks123$@localhost/wati_clone'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function to get task status
def get_task_status(task_id: int, db: Session):
    """
    Fetches the status of a task based on the task_id from the database.
    """
    broadcast = db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.task_id == task_id).first()
    if broadcast:
        return broadcast.status
    
    return "unknown"

# Middleware to handle task cancellations
class CancelationMiddleware(Middleware):
    def before_process_message(self, broker, message):
        # Create a new database session
        db: Session = SessionLocal()
        print("run")
        try:
            task_id = message.message_id
            status = get_task_status(task_id, db)  # Pass the session directly
            if status == 'Cancelled':
                raise SkipMessage("Task has been canceled.")
        finally:
            db.close()  # Ensure the session is closed after use

# Add the middleware to your Dramatiq broker
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(url="redis://localhost:6379")
redis_broker.add_middleware(CancelationMiddleware())
dramatiq.set_broker(redis_broker)


@dramatiq.actor(max_retries=0)
def send_broadcast(template_name, recipients, broadcastId,API_url, headers,user_id,image_id,body_parameters):
    
    
    """
    Dramatiq actor to send broadcast messages.
    """

    success_count = 0
    failed_count=0
    errors = []

    # for recipient in recipients:
    #     data = {
    #         "messaging_product": "whatsapp",
    #         "to": recipient,
    #         "type": "template",
    #         "template": {
    #             "name": template_name,
    #             "language": {
    #                 "code": "en_US"
    #             }
    #         }
    #     }

    for contact in recipients:
        recipient_name = contact["name"]  # Adjusted to access the dictionary
        recipient_phone = contact["phone"]

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "en_US"},
                # You can insert recipient_name into your message template if needed
            }
        }

        if image_id:
            data["template"]["components"] = [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {"id": image_id}
                        }
                    ]
                }
            ]

        
        
        if body_parameters:
            if body_parameters == "Name":
                body_params = [{"type": "text","text": f"{recipient_name}"}]
                
            else:
                data["template"]["components"] = []

            if "components" not in data["template"]:
                data["template"]["components"] = []
            data["template"]["components"].append({
                "type": "body",
                "parameters": body_params
            })


        response = requests.post(API_url, headers=headers, data=json.dumps(data))
        
        response_data = response.json()
        

        if response.status_code == 200:
            db: Session = SessionLocal()
            success_count += 1
            wamid = response_data['messages'][0]['id']
            phone_num=response_data['contacts'][0]["wa_id"]

            MessageIdLog=Broadcast.BroadcastAnalysis(
            user_id=user_id,
            broadcast_id=broadcastId,
            message_id=wamid,
            status="sent",
            phone_no=phone_num,
            contact_name=recipient_name
             )
            
            db.add(MessageIdLog)
            db.commit()
            db.refresh(MessageIdLog) 
            db.close()

        else:
            failed_count += 1
            errors.append({"recipient": recipient_phone, "error": response.json()})
            db: Session = SessionLocal()
            MessageIdLog=Broadcast.BroadcastAnalysis(
            user_id=user_id,
            broadcast_id=broadcastId,
            status="failed",
            phone_no=recipient_phone,
            contact_name=recipient_name  
             )
            db.add(MessageIdLog)
            db.commit()
            db.refresh(MessageIdLog)
            db.close()


    db: Session = SessionLocal()
    broadcastLog = db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.id == broadcastId).first()
    print(f"Broadcast after update: {broadcastLog}")

    if not broadcastId:
        raise Exception(f"Broadcast not found for ID {broadcastId}")

    try:
        broadcastLog.success = success_count
        broadcastLog.status = "Successful"
        broadcastLog.failed = failed_count

        db.add(broadcastLog)
        db.commit()
        db.refresh(broadcastLog)
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        print(f"Error while updating broadcast: {str(e)}")
        raise e
    finally:
        db.close()  # Always close the session

    

    if errors:
        print(f"Failed to send some messages: {errors}")
        raise Exception(f"Failed to send broadcast: {errors}")
    
    print(f"Successfully sent {success_count} messages.{errors.count}")


   