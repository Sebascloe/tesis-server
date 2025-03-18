from sqlmodel import Session, select
from models.users import Users
from schemas.users import UserCreate, UserUpdate


def create_user(session: Session, user_data: UserCreate):
    user = Users(**user_data.model_dump(exclude={"id"}))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_all_users(session: Session):
    user = session.exec(select(Users)).all()
    return user

def get_one_user(session: Session, user_id):
    return session.get(Users, user_id)

def update_one_user(session: Session, user: UserUpdate, user_id: int):
    db_user = session.get(Users, user_id)
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user