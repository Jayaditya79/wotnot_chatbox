from fastapi import APIRouter,Depends,HTTPException
from ..models import User
from ..Schemas import user
from ..database import database
from sqlalchemy.orm import Session
from .. import hashing
import secrets
router=APIRouter(tags=['User'])

@router.post('/register')
def new_user(request: user.register_user, db: Session = Depends(database.get_db)):
    existing_user = db.query(User.User).filter((User.User.email == request.email) | (User.User.Phone_id == request.Phone_id)).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Account with this email or phone number already exists")
    
    else:
        api_key=secrets.token_hex(32)
        registeruser=User.User( 
            username=request.username,
            email=request.email,
            password_hash=hashing.Hash.bcrypt(request.password),  # Decode the hash to store it as a string
            WABAID=request.WABAID,
            PAccessToken=request.PAccessToken,
            Phone_id=request.Phone_id,
            api_key=api_key
            )
        db.add(registeruser)
        db.commit()
        db.refresh(registeruser)
        return {"success": True, "message": "Account created successfully"}
    
