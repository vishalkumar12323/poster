from flask import render_template, url_for, request, session
from datetime import datetime
from lib.connection import Post, client
from typing import TypedDict
import re


# class TPost(TypedDict, total=False):
#     id: int
#     title: str
#     content: str
#     user_id: int
#     author: str
#     created_at: datetime


def create_slug(title:str) -> str:
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)

    slug = re.sub(r'\s+', '-', title).strip('-')
    
    return slug

def get_latest_post():
    pass

def get_user_post():
    pass

def create_post():
    title = request.form.get("title", "")
    content = request.form.get("content", "")
    slug = create_slug(title)
    user_id = session["user_id"]

    
    pass

def edit_post():
    pass

def delete_post():
    pass