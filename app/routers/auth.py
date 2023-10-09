from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oath2


router = APIRouter(tags=['A uthentication'])


@router.post("/login", response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print("------+++++")
    print(user_credential)
    user = db.query(models.User).filter(
        models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials user not found")
    print("------")
    print(user.password)
    print(user_credential.password)
    print("------")
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials password")

    acces_token = oath2.create_acces_token(data={"user_id": user.id})

    return {"acces_token": acces_token, "token_type": "bearer"}
