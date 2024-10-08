#  these are the webhooks routes for integration with woocommerce
from fastapi import FastAPI, Depends, HTTPException, Request,APIRouter
from sqlalchemy.orm import Session
from ..database import database  # Your database connection
from ..models import User,Integration,Broadcast
import json # Your models
import requests
from ..Schemas import user,integration
from ..oauth2 import get_current_user
from typing import List
router=APIRouter(tags=['woocommerce'])



# Function to verify API key from request headers or query params
def verify_api_key(request: Request, db: Session ):
    api_key = request.headers.get("Authorization")
    
    # If the API key is passed as a query parameter
    if not api_key:
        api_key = request.query_params.get("api_key")
        
    # Remove "Bearer " if passed in the Authorization header
    if api_key and api_key.startswith("Bearer "):
        api_key = api_key[7:]
    
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    # Check if API key exists in the database
    user = db.query(User.User).filter(User.User.api_key == api_key).first()
    
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return user



def send_order_confirmation_message(order_data, whatsapp_token, phone_id, db: Session,user_id):
    """
    Sends a user-specific message template when a new order is created in WooCommerce.
    """
    
    # Fetch the integration details from the database
    integration=db.query(Integration.WooIntegration).filter((Integration.WooIntegration.user_id==user_id)&(Integration.WooIntegration.type=="woo/order_confirmation")).first()
    
    if not integration:
        raise ValueError("No WooCommerce order confirmation integration found")

    template_name = integration.template
    parameters = integration.parameters

    customer_phone = order_data["billing"]["phone"]
    customer_name = order_data["billing"]["first_name"]
    order_id = order_data["id"]
    order_total = order_data["total"]

    success_count = 0
    failed_count = 0

    # Make list of contacts (expected format by database)
    contacts_list=[customer_phone]
    

    # Map parameters to values from order_data
    parameter_values = {
        "customer_name": customer_name,
        "order_id": order_id,
        "order_total": order_total
    }

    # Define the message components
    components = [
        {
            "type": "body",
            "parameters": []
        }
    ]
    
    for param in parameters:
         
        param_key = param["key"]
        # Use the parameter key to fetch the corresponding value from order_data
        if param_key == "billing.first_name":
            value = customer_name
        elif param_key == "id":
            value = order_id
        elif param_key == "total":
            value = order_total
        else:
            value = ""  # Handle unknown parameters

        
        components[0]["parameters"].append({"type": "text", "text": value})
        
    # Define the message template data
    message_data = {
        "messaging_product": "whatsapp",
        "to": customer_phone,
        "type": "template",
        "template": {
            "name": template_name,  # Use the template name from the database
            "language": {
                "code": "en_US"
            },
            "components": components
        }
    }

 
    # WhatsApp API endpoint and headers
    API_URL = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    API_HEADERS = {
        "Authorization": f"Bearer {whatsapp_token}",  # Use user-specific token
        "Content-Type": "application/json"
    }
    
    # Send message to WhatsApp API
    response = requests.post(API_URL, headers=API_HEADERS, json=message_data)

    if response.status_code == 200:
        print(f"Message sent successfully to {customer_phone}")
        success_count += 1
        confirmation_status="Successful"
    else:
        print(f"Failed to send message. Response: {response.text}")
        failed_count += 1
        confirmation_status="Failed"

    # log to the broadcast to daatbase
    
    

    db_broadcastList=Broadcast.BroadcastList(
        user_id=user_id,
        name=customer_name,
        template=template_name,
        contacts=contacts_list,
        type="woo/integration",
        success=success_count,
        failed=failed_count,
        status= confirmation_status,
        
    )
    db.add(db_broadcastList)
    db.commit()
    db.refresh(db_broadcastList)

# webhook for the order cofirmation
@router.post("/webhook/woocommerce")
async def handle_woocommerce_webhook(request: Request, db: Session = Depends(database.get_db)):
    # Verify API key
    user = verify_api_key(request, db)

    body = await request.body()
    print(f"Webhook received: {body.decode('utf-8')},user id is {user.id}")  # Log the raw body for debugging
    
    # Try to parse the body as JSON
    try:
        
        payload = await request.json()
        send_order_confirmation_message(payload,user.PAccessToken,user.Phone_id,db,user.id)
    except Exception as e:
        return {"error": "Invalid JSON", "detail": str(e)}

    # Continue processing the webhook data

    print(payload)
    return {"status": "success"}
    

# route for fetchapi key
@router.get("/webhooklink")
def apikey(request:Request,get_current_user: user.newuser=Depends(get_current_user)):
    apikey=get_current_user.api_key

    base_url = request.url.scheme + "://" + request.url.netloc

    webhooklink=f"{base_url}/webhook/woocommerce?api_key={apikey}"

    return{"webkook_link":webhooklink}
    

@router.post("/integrate/woocommerce")
def saveWooIntegartion(request:integration.wooIntegration,get_current_user: user.newuser=Depends(get_current_user),db: Session = Depends(database.get_db)):
    parameters_list = [{"key": param.key} for param in request.parameters]
    
    exixsting=db.query(Integration.WooIntegration).filter((Integration.WooIntegration.user_id==get_current_user.id)&(Integration.WooIntegration.type=="woo/order_confirmation")).first()

    if exixsting:
        raise HTTPException(status_code=400, detail="Integration already exists")
   
   # Create the WooIntegrationDB model instance
    integration=Integration.Integration(
        user_id=get_current_user.id,
        type=request.type,
        api_key=get_current_user.api_key,
        app="woocommerce"
    )
    # Add and commit the data to the database
    db.add(integration)
    db.commit()
    db.refresh(integration)

    integration_search=db.query(Integration.Integration).filter((Integration.Integration.user_id==get_current_user.id)&(Integration.Integration.type==request.type)).first()

    woo_integration = Integration.WooIntegration(
        integration_id=integration_search.id,
        parameters=parameters_list,
        api_key=get_current_user.api_key,
        type=request.type,
        template=request.template_id,
        user_id=get_current_user.id

    )

    # Add and commit the data to the database
    db.add(woo_integration)
    db.commit()
    db.refresh(woo_integration)

    # Create the WooIntegrationDB model instance
   

    return {"template": request.template_id, "parameters": request.parameters}