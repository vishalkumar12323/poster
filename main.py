from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

from utils.auth_forms import LoginForm, RegisterFrom
from utils.post_form import CreateForm, EditForm
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app=app)

login_manager = LoginManager(app=app)
# use setattr to avoid static type checker assignment error
setattr(login_manager, "login_view", "login")

# -- User Model --
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(500), nullable=False)
    # The 'posts' relationship is defined here.
    # The 'author' backref will be automatically added to the Post model.
    posts = db.relationship("Post", backref="author", lazy=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String, nullable=False)
    # Remove the redundant 'author' string column if it's meant to be the relationship object.
    # author = db.Column(db.String, nullable=False) 

    # This is the foreign key column. Note the tablename in db.ForeignKey is lowercase.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Remove this explicit relationship definition when using backref in User model.
    # user = db.relationship("User", backref="posts", lazy=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html", user=current_user)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("login"))

    return render_template('forms/register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
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



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message="You have been logged out")
    return redirect(url_for('login'))



@app.route("/new-post", methods=["GET", "POST"])
def create_post():
    form =  CreateForm()

    if form.validate_on_submit():

        pass
    return render_template('forms/create_post.html', form=form)



if __name__ == "__main__":
    if not os.path.exists("instance/poster.db"):
        with app.app_context():
            db.create_all()
    
    app.run(debug=True)