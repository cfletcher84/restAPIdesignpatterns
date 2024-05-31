from sqlalchemy.orm import Session
from database import db
from models.user import User
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from utils.utils import encode_token

def save(user_data):
    with Session(db.engine) as session:
        with session.begin():
            user_query = select(User).where(User.username == user_data['username'])
            user_check = session.execute(user_query).scalars().first()
            if user_check is not None:
                raise ValueError("Username already exists! Try again!")
            new_user = User(username=user_data['username'], password=generate_password_hash(user_data['password']), role=user_data['role'])
            session.add(new_user)
            session.commit()
        session.refresh(new_user)
        return new_user
    
def find_all(page=1, per_page=10):
    query = select(User).offset((page-1) * per_page).limit(per_page)
    users = db.session.execute(query).scalars().all()
    return users

def get_user(username):
    return db.session.get(User, username)

def get_token(username, password):
    query = db.select(User).where(User.username == username)
    user = db.session.execute(query).scalars().first()
    if user is not None and check_password_hash(user.password, password):
        auth_token = encode_token(user.id)
        return auth_token
    else:
        return None
    