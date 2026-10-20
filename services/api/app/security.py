"""Local-mode authentication; no bearer credentials exposed to the JS app."""
from __future__ import annotations
import hashlib, hmac, os, secrets
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from .db import db_session
from .models import User, LoginSession

hasher = PasswordHasher(time_cost=2, memory_cost=32768, parallelism=2)
COOKIE = 'bp_session'
SESSION_HOURS = 8

def password_hash(value: str): return hasher.hash(value)
def verify_password(hash_: str, value: str):
    try: return hasher.verify(hash_, value)
    except (VerifyMismatchError, VerificationError): return False

def sha(value: str) -> str: return hashlib.sha256(value.encode()).hexdigest()

def create_login(db: Session, user: User):
    token = secrets.token_urlsafe(36)
    csrf = sha('csrf:' + token)
    s = LoginSession(user_id=user.id, token_hash=sha(token), csrf_hash=sha(csrf), expires_at=datetime.now(timezone.utc)+timedelta(hours=SESSION_HOURS))
    db.add(s); db.commit()
    return token, csrf

def get_login(request: Request, db: Session):
    raw = request.cookies.get(COOKIE)
    if not raw: raise HTTPException(401, 'Sign in required')
    sess = db.scalar(select(LoginSession).where(LoginSession.token_hash == sha(raw)))
    if not sess or sess.expires_at.replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc):
        raise HTTPException(401, 'Session expired')
    user = db.get(User, sess.user_id)
    if not user or user.role not in ('student','reviewer','auditor','admin'):
        raise HTTPException(401, 'Account not found or role disabled')
    return user, sess

def current_user(request: Request, db: Session = Depends(db_session)):
    return get_login(request, db)[0]

def csrf_user(request: Request, db: Session = Depends(db_session)):
    user, sess = get_login(request, db)
    origin = request.headers.get('origin')
    allowed = {x.strip() for x in os.getenv('ALLOWED_ORIGINS','http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000').split(',')}
    if origin and origin not in allowed:
        raise HTTPException(403, 'Untrusted origin')
    incoming = request.headers.get('x-csrf-token', '')
    if not incoming or not hmac.compare_digest(sha(incoming), sess.csrf_hash):
        raise HTTPException(403, 'Missing or invalid CSRF token')
    return user

def require_roles(*roles):
    def check(user: User=Depends(current_user)):
        if user.role not in roles: raise HTTPException(403, 'Insufficient role')
        return user
    return check

def require_mutation_roles(*roles):
    def check(user: User=Depends(csrf_user)):
        if user.role not in roles: raise HTTPException(403, 'Insufficient role')
        return user
    return check
