# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .database import database
# from .routes import user,broadcast,contacts,auth,woocommerce,integration,wallet
# from .services import dramatiq_router
# from . import oauth2
# # models creation
# database.Base.metadata.create_all(bind=database.engine)

# app = FastAPI()

# # adding the routes

# app.include_router(broadcast.router)
# app.include_router(contacts.router)
# app.include_router(user.router)
# app.include_router(auth.router)
# app.include_router(wallet.router)
# app.include_router(oauth2.router)
# app.include_router(dramatiq_router.router)
# app.include_router(woocommerce.router)
# app.include_router(integration.router)

# # defining origin for cors
# origins = [
#     "http://localhost:8080", "http://localhost",     
#     "http://127.0.0.1","http://localhost:5173","http://localhost:8081",    
#     # Add other origins if needed
# ]


# # CORS middleware configuration
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,  # Adjust this to specific origins in production
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )




# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:8080",  # Your frontend origin
#         "http://localhost",       
#         "http://127.0.0.1",
#         "http://localhost:5173",
#         "http://localhost:8081"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

 









     
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .database import database
from .routes import user, broadcast, contacts, auth, woocommerce, integration, wallet
from .services import dramatiq_router
from . import oauth2
from .models import ChatBox
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# Models creation
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Adding the routes
app.include_router(broadcast.router)
app.include_router(contacts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(oauth2.router)
app.include_router(dramatiq_router.router)
app.include_router(woocommerce.router)
app.include_router(integration.router)

# Defining origins for CORS
origins = [
    "http://localhost:8080", "http://localhost",     
    "http://127.0.0.1", "http://localhost:5173", "http://localhost:8081",    
]

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the scheduler
scheduler = BackgroundScheduler()

def close_expired_chats():
    db = next(database.get_db())  # Get the database session
    now = datetime.now()
    expired_conversations = db.query(ChatBox.First_Conversation).filter(
        ChatBox.First_Conversation.active == True,
        (now - ChatBox.First_Conversation.first_chat_time) > timedelta(minutes=5)
        # (now - ChatBox.First_Conversation.first_chat_time) > timedelta(hours=24)
    ).all()

    for conversation in expired_conversations:
        conversation.active = False
        
    db.commit()

# Schedule the job (do not start the scheduler here)
scheduler.add_job(close_expired_chats, 'interval', minutes=1)

@app.on_event("startup")
async def startup_event():
    # Start the scheduler here
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    # Shut down the scheduler
    scheduler.shutdown()