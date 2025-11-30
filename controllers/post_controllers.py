from flask import render_template, redirect, url_for
from utils.post_form import CreateForm, EditForm
import re
from lib.models import Post, db
from flask_login import current_user


def create_slug(title:str) -> str:
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)

    slug = re.sub(r'\s+', '-', title).strip('-')
    
    return slug


def view(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('view_post.html', post=post, user=current_user)


def create():
    form =  CreateForm()

    if form.validate_on_submit():
        slug = create_slug(form.title.data)
        post = Post(title=form.title.data, content=form.content.data, slug=slug, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("dashboard"), code=302)
    return render_template('forms/create_post.html', form=form, user=current_user)


def edit(post_id):
    form = EditForm()
    post = Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.slug = create_slug(form.title.data)
        db.session.commit()
        return redirect(url_for("dashboard"), code=302)
    return render_template('forms/edit_post.html', form=form, user=current_user, post=post)


def delete(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("dashboard"), code=302)