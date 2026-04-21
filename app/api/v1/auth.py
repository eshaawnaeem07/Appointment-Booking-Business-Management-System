from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.schemas import auth as auth_schema
from app.services import auth_service as AuthService
from app.core import security
from app.db.session import get_db
from app.schemas import auth as auth_schema
from app.services import auth_service as AuthService
from app.services.email_service import EmailService

router = APIRouter(prefix="/auth", tags=["auth"])

#Register
@router.post("/register", response_model=auth_schema.UserResponse)
def register(user_in: auth_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        return AuthService.register_user(
    db,
    email=user_in.email,
    password=user_in.password
)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Login (Returns JWT + Refresh Token)
@router.post("/login")
def login(user_in: auth_schema.UserLogin, db: Session = Depends(get_db)):
    try:
        return AuthService.login_user(
            db,
            email=user_in.email,
            password=user_in.password
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Refresh Token
@router.post("/refresh-token")
def refresh_token(token_in: auth_schema.RefreshTokenRequest):
    # Logic: Verify refresh token and issue new access token
    try:
        payload = AuthService.verify_refresh_token(token_in.refresh_token)
        new_access_token = security.create_token(
            payload["sub"], timedelta(minutes=30), security.SECRET_KEY
        )
        return {"access_token": new_access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 4. Forgot Password (Generates OTP & Sends via SendGrid)
@router.post("/forgot-password")
def forgot_password(request: auth_schema.ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService.get_user_by_email(db, request.email)
        if not user:
            raise HTTPException(status_code=404, detail="Email not found")

        otp = "5678"  # replace later with random OTP

        AuthService.save_otp(db, user.id, otp)
        EmailService.send_otp_email(user.email, otp)

        return {"message": "OTP sent to your email"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 5. Reset Password (OTP Verification + Password Match)
@router.post("/reset-password")
def reset_password(req: auth_schema.ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
    # Check if passwords match
        if req.new_password != req.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        # Validate OTP
        user = AuthService.verify_otp_and_get_user(db, req.email, req.otp)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
        # Update Password
        AuthService.update_password(db, user, req.new_password)
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Logout (Handled on client by deleting tokens; server can blacklist)
@router.post("/logout")
def logout():
    try:
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
