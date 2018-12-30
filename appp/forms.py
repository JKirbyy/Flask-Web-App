from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired

class UserForm(Form):
    username = StringField('string1', validators=[DataRequired()])
    password = StringField('string2', validators=[DataRequired()])

class PasswordForm(Form):
    password = StringField('string1', validators=[DataRequired()])


class SearchForm(Form):
    search = StringField('string1', validators=[DataRequired()])

class EmptySearchForm(Form):
    search = StringField('string1')

class BlogForm(Form):
    title = StringField('string1', validators=[DataRequired()])
    main = TextAreaField('Text', render_kw={"rows": 10, "cols": 11}, validators=[DataRequired()])

class BlogUpdateForm(Form):
    title = StringField('string1', validators=[DataRequired()])
    main = TextAreaField('Text', render_kw={"rows": 10, "cols": 11}, validators=[DataRequired()])
    comment =  TextAreaField('Text', render_kw={"rows": 5, "cols": 9}, validators=[DataRequired()])


class CompleteForm(Form):
    complete = BooleanField()
