from sqlalchemy.orm import Session


from src.core.exceptions import UserAlreadyExistsException,UserEmailNotExists,UserPasswordNotMatched
from src.auth.utils import create_access_token
from src.auth import model,schema
from src.auth.utils import hash_password,verify_password


async def createUser(req :schema.UserInfo , db :Session)-> schema.UserResponse :
    # 1. Check if the user already exists in the system
    existing_user = db.query(model.User).filter(model.User.email == req.email).first()
    
    if existing_user:
        raise UserAlreadyExistsException("Email Already Registered")
    
    # 2. Create User
    new_user = model.User(
        email = req.email , 
        hashed_password = hash_password(req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #create response user which doesnt contain private data
    res = schema.UserResponse(
        id = new_user.id ,
        email= new_user.email,
        is_active= new_user.is_active
    )

    return res

async def authenticateUser(req :schema.UserInfo , db :Session) -> schema.TokenSchema:
    #query if user with email exists
    user = db.query(model.User).filter(model.User.email == req.email).first()

    if not user:
        raise UserEmailNotExists
    if not verify_password(req.password ,user.hashed_password):
        raise UserPasswordNotMatched
    # The use of "sub" is not an arbitrary choice—it stands for Subject. It is a globally recognized, standardized key defined by the OpenID Connect and OAuth 2.0 specifications (specifically RFC 7519 for JSON Web Tokens).
    #
    token = create_access_token( data = { "sub" : str(user.id) })

    new_token = schema.TokenSchema(access_token=token , token_type="bearer")
    return new_token
