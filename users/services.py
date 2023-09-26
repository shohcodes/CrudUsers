from users.models import User


def get_user_by_id(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db, username):
    return db.query(User).filter(User.username == username).first()


def create_user(db, user):
    model = User(**user.dict())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def get_users(skip, limit, db):
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db, model):
    db.delete(model)
    db.commit()


def update_user_by_id(db, user, model):
    for key, val in user.dict().items():
        setattr(model, key, val)
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def partial_update_user_by_id(db, user, update_data):
    for key, value in update_data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
