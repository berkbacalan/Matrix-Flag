from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ....models.user import UserCreate, User, Token
from ....services.user import user_service
from ....core.auth import verify_password, create_access_token
from ....core.deps import get_current_active_user
from ....core.metrics import record_user_operation, record_login_attempt

router = APIRouter()


@router.post("/register", response_model=User)
async def register(user: UserCreate):
    try:
        db_user = await user_service.get_user_by_email(user.email)
        if db_user:
            record_user_operation("register", "email_exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        new_user = await user_service.create_user(user)
        record_user_operation("register", "success")
        return new_user
    except Exception as e:
        record_user_operation("register", "error")
        raise e


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await user_service.get_user_by_email(form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            record_login_attempt("invalid_credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            record_login_attempt("inactive_user")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

        await user_service.update_last_login(user.id)
        record_login_attempt("success")

        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        record_login_attempt("error")
        raise e


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
