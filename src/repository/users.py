from sqlalchemy.orm import Session
from libgravatar import Gravatar

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user by the email.

    :param email: The email.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The found user or None if it doesn't exist.
    :rtype: User | None
    """
    return db.query(User).filter(User.email == email).first()


async def confirmed_email(email: str, db: Session) -> User:
    """
    Confirmes the email.

    :param email: The email.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with confirmed email.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
    return user


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user.

    :param body: The data to create a user.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The new user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(username=body.username, email=body.email, password=body.password, avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> User:
    """
    Updates user's refresh token.

    :param user: The user.
    :type user: User
    :param token: The new refresh tocken.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: The user with updated refresh token.
    :rtype: User
    """
    user.refresh_token = token
    db.commit()
    return user


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates user's avatar.

    :param email: The email of a user whose avatar will be updated.
    :type email: str
    :param url: url of the new avatar.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user with a new avatar.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user