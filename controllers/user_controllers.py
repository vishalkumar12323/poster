from flask import redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user
from utils.auth_forms import LoginForm, RegisterFrom
from lib.models import User, db
from werkzeug.security import generate_password_hash
from flask import flash

# function for register/signup new user
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterFrom()
    if form.validate_on_submit():
        exisiting = User.query.filter_by(email=form.email.data).first()
        if exisiting:
            print("existing", exisiting)
            flash("Email already registered")
            return redirect(url_for('register'))

        user = User(name=form.name.data, email=form.email.data, hashed_password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for("signin"))

    return render_template('forms/register.html', form=form)


def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user) 
            return redirect(url_for("dashboard"))
        flash("Invalid email or password")

    return render_template('forms/login.html', form=form)

def logout():
    logout_user()
    flash(message="You have been logged out")
    return redirect(url_for('signin'))
