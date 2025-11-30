from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    title = StringField(label="Post Title", validators=[DataRequired("post title is required")])
    content = StringField(label="Content", validators=[DataRequired('post content is required')])

    submit = SubmitField(label="create post")


class EditForm(FlaskForm):
    title = StringField(label="Post Title", validators=[DataRequired("post title is required")])
    content = StringField(label="Content", validators=[DataRequired('post content is required')])

    submit = SubmitField(label="update post")