from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app import database, schemas, models, utils, oauth2  
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login",response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    # Query user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # If user does not exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Changed from NOT_FOUND (404) to FORBIDDEN (403)
            detail="INVALID CREDENTIALS",
        )

    # Verify password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="INVALID CREDENTIALS",
        )

    # Generate access token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
