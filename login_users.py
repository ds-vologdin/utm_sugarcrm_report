import flask_login
from passlib.hash import pbkdf2_sha256
import logging

from models import UsersReport


login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(login):
    logging.debug('user_loader')
    user_report = UsersReport.query.filter(UsersReport.login == login).first()
    if not user_report:
        return None
    user = User()
    user.id = user_report.login
    user.login = user_report.login
    user.name = user_report.name
    user.email = user_report.email
    return user


@login_manager.request_loader
def request_loader(request):
    logging.debug('request_loader')
    login = request.form.get('login')
    password = request.form.get('password')
    user_report = UsersReport.query.filter(UsersReport.login == login).first()
    if not user_report:
        return None
    if not verify_password(password, user_report.password):
        return None
    user = User()
    user.id = user_report.login
    user.login = user_report.login
    user.name = user_report.name
    user.email = user_report.email

    return user


def verify_password(password, hash):
    return pbkdf2_sha256.verify(password, hash)


def get_user(login, password):
    if not (login and password):
        return None
    user_report = UsersReport.query.filter(UsersReport.login == login).first()
    print(user_report)
    if not user_report:
        return None
    if not verify_password(password, user_report.password):
        return None
    user = User()
    user.id = user_report.login
    user.login = user_report.login
    user.name = user_report.name
    user.email = user_report.email
    return user
