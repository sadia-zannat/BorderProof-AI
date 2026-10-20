"""Explicitly synthetic development fixtures; never enabled in production."""
import os
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import User, PaymentCase
from .security import password_hash

SEED_USERS = [
 ('student@borderproof.test','Demo Student','student'),
 ('reviewer@borderproof.test','Demo Reviewer','reviewer'),
 ('auditor@borderproof.test','Demo Auditor','auditor'),
 ('admin@borderproof.test','Demo Admin','admin'),
]
def seed_demo(db: Session):
    if os.getenv('APP_ENV','development') != 'development' or os.getenv('ENABLE_DEMO_SEED','0') != '1': return
    password = os.getenv('DEMO_SEED_PASSWORD','')
    if len(password) < 12: raise RuntimeError('DEMO_SEED_PASSWORD must be >=12 chars when seeding is enabled')
    for email,name,role in SEED_USERS:
        if db.scalar(select(User).where(User.email==email)): continue
        user = User(email=email,name=name,role=role,password_hash=password_hash(password),institution='SYNTHETIC Demo University')
        db.add(user);db.flush()
        if role=='student':
            db.add(PaymentCase(user_id=user.id,title='Sample tuition planning case',institution='SYNTHETIC Northbridge University',origin_country='Bangladesh',destination_country='United Kingdom',amount='12500.00',currency='GBP',is_synthetic=True))
    db.commit()
