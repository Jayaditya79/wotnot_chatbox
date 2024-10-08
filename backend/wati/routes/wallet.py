from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from datetime import datetime
from ..oauth2 import get_current_user
from ..Schemas import user  
from ..database import database 
import logging
from ..models import User

router = APIRouter(tags=['Wallet'])

@router.get("/conversation-analytics/{account_id}")
async def get_conversation_analytics(account_id: int, db: Session = Depends(database.get_db), get_current_user: user.newuser = Depends(get_current_user)):
    
    ACCESS_TOKEN = get_current_user.PAccessToken
    
    account_creation_time = db.query(User.User).filter(User.User.WABAID == account_id).first()
    if not account_creation_time:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Convert account creation time to UNIX timestamp
    since = int(account_creation_time.created_at.timestamp())
    until = int(datetime.now().timestamp())

    url = f"https://graph.facebook.com/v20.0/{account_id}?fields=conversation_analytics.start({since}).end({until}).granularity(DAILY).phone_numbers([]).dimensions([\"CONVERSATION_CATEGORY\",\"CONVERSATION_TYPE\",\"COUNTRY\",\"PHONE\"])"
    
    response = requests.get(url, params={"access_token": ACCESS_TOKEN})
    logging.info(response)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", "Error fetching data"))

    return response.json()


@router.get("/conversation-cost-history/{account_id}")
async def get_conversation_cost_history(account_id: int, db: Session = Depends(database.get_db), get_current_user: user.newuser = Depends(get_current_user)):
    
    ACCESS_TOKEN = get_current_user.PAccessToken
    
    # Fetch account creation time from the database
    account_creation_time = db.query(User.User).filter(User.User.WABAID == account_id).first()
    if not account_creation_time:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Convert account creation time to UNIX timestamp
    since = int(account_creation_time.created_at.timestamp())
    until = int(datetime.now().timestamp())

    # URL for fetching conversation analytics data
    url = f"https://graph.facebook.com/v20.0/{account_id}?fields=conversation_analytics.start({since}).end({until}).granularity(DAILY).phone_numbers([]).dimensions([\"CONVERSATION_CATEGORY\",\"CONVERSATION_TYPE\",\"COUNTRY\",\"PHONE\"])"
    
    # Send request to the API
    response = requests.get(url, params={"access_token": ACCESS_TOKEN})

    # Check if the response is successful
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", "Error fetching data"))
    
    # Extract relevant data from the response
    conversation_data = response.json().get("conversation_analytics", {}).get("data", [])
    processed_data = []
    
    for data_entry in conversation_data:
        data_points = data_entry.get("data_points", [])
        for point in data_points:
            # Convert UNIX timestamps to readable format
            start_time = datetime.utcfromtimestamp(point["start"]).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.utcfromtimestamp(point["end"]).strftime('%Y-%m-%d %H:%M:%S')
            
            # Extract cost and template details
            cost = point.get("cost")
            conversation_type = point.get("conversation_type")
            conversation_category = point.get("conversation_category")
            
            # Add the processed data to the result list
            processed_data.append({
                "start_time": start_time,
                "end_time": end_time,
                "cost": cost,
                "conversation_type": conversation_type,
                "conversation_category": conversation_category
            })

    # Return the processed data
    return {"conversation_analytics": processed_data}




@router.get("/conversations-cost/{account_id}")
async def get_conversation_costs(account_id: int, db: Session = Depends(database.get_db), get_current_user: user.newuser = Depends(get_current_user)):
    ACCESS_TOKEN = get_current_user.PAccessToken
    
    # Fetch the account creation time
    account_details = db.query(User.User).filter(User.User.WABAID == account_id).first()
    if not account_details:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Convert account creation time to UNIX timestamp
    since = int(account_details.created_at.timestamp())
    until = int(datetime.now().timestamp())

    # Construct the API URL
    url = f"https://graph.facebook.com/v20.0/{account_id}?fields=conversation_analytics.start({since}).end({until}).granularity(DAILY).phone_numbers([]).dimensions([\"CONVERSATION_CATEGORY\",\"CONVERSATION_TYPE\",\"COUNTRY\",\"PHONE\"])"
    
    # Make the request
    response = requests.get(url, params={"access_token": ACCESS_TOKEN})
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", "Error fetching data"))
    
    # Extract cost values
    data = response.json()
    conversation_data_points = data.get("conversation_analytics", {}).get("data", [])
    
    total_cost = 0
    for entry in conversation_data_points:
        for data_point in entry.get("data_points", []):
            total_cost += data_point.get("cost", 0)

    Paid_Amount = account_details.paid_amount
    
    return Paid_Amount-total_cost