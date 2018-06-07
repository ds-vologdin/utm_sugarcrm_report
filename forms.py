from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, required


class LoginForm(FlaskForm):
    login = StringField('login', validators=[required(), DataRequired()])
    password = PasswordField(
        'password', validators=[required(), DataRequired()]
    )
