from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta
from app.utils.enums import UserRole



def register_user(db: Session, email: str, password: str, role):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise Exception("Email already exists")
    if role not in [UserRole.USER.value, UserRole.BUSINESS.value]:
         raise Exception("Input should be 'user' or 'business'")

    user = User(
        email=email,
        password=hash_password(password),
        role = role.lower()
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db, email, password):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise Exception("Invalid credentials")

    access_token = create_access_token({
    "sub": user.email,
    "role": user.role
    })
    refresh_token = create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def verify_refresh_token(token: str):
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise Exception("Invalid token type")
    return payload

def logout_user(db: Session, email: str):
    """Invalidate refresh tokens by clearing them from the database"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise Exception("User not found")

    user.reset_token = None
    user.token_expiry = None
    db.commit()

def save_otp(db: Session, user_id: int, otp: str):
    """Save OTP and expiry time in DB for the user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception("User not found")

    user.reset_token = otp
    user.token_expiry = datetime.utcnow() + timedelta(minutes=10)  # OTP valid for 10 mins
    db.commit()

def get_user_by_email(db: Session, email: str):
    """Fetch user by email"""
    return db.query(User).filter(User.email == email).first()

# This function can be used in the reset password endpoint to verify OTP and fetch user
def verify_otp_and_get_user(db: Session, email: str, otp: str):
    """Verify OTP and return user if valid"""
    user = get_user_by_email(db, email)
    if not user:
        raise Exception("User not found")
    if (
    user.reset_token != otp
    or not user.token_expiry
    or user.token_expiry < datetime.utcnow()
    ):
     raise Exception("Invalid or expired OTP")
    return user

def update_password(db: Session, user: User, new_password: str):
    """Update user password and clear OTP"""
    
    user.password = hash_password(new_password)
    #clear OTP after use
    user.reset_token = None
    user.token_expiry = None

    db.commit()