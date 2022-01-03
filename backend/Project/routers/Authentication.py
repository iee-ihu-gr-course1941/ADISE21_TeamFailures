from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm.session import Session
from .. import schemas,database,models,hashing,JWTtoken
from sqlalchemy.orm import Session
from ..repository import user

router=APIRouter(
    prefix='/Auth',
    tags=['Authentication']
)

@router.post('/login')
def login(request:schemas.Login,db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
    if not hashing.Hash.verify(user.password,request.password):
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incorrect Password"
        )
    #generate JWTtoken and return it 
    access_token = JWTtoken.create_access_token(
        #pass user.email
        data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/register',response_model=schemas.ShowUser)
def create_user(request:schemas.User,db:Session=Depends(database.get_db)):
    return user.create_user(request,db)
