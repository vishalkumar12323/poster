from flask import redirect, session, url_for
from typing import TypedDict, Optional
from lib.connection import client, User


class TUser(TypedDict, total=False):
    name: Optional[str]
    email: str
    password: str

def login_user(user: TUser):
    email = user.get('email')
    password = user.get("password")

    user_by_email = client.query(User).filter_by(email=email).first()

    if user_by_email:
        stored_password = getattr(user_by_email, "password", None)
        if stored_password is None and isinstance(user_by_email, dict):
            stored_password = user_by_email["password"]

        if stored_password == password:
            session["user_id"] = user_by_email.id
            session["is_logged_in"] = True
            return redirect(url_for("/"), code=302)
    
    return redirect("/login")


def register_user(user: TUser):
    name = user.get("name")
    email = user.get("email")
    password = user.get("password")

    exists = client.query(User).filter_by(email=email).first()

    if exists:
        return redirect("/register")
    
    new_user = User(name=name, email=email, password=password)
    client.add(new_user)
    client.commit()

    return redirect("/login")