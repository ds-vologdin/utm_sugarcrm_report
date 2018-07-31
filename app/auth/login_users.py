import flask_login
from passlib.hash import pbkdf2_sha256
import logging

from .models import UsersReport


login_manager = flask_login.LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def user_loader(login):
    logging.debug('user_loader')
    user_report = UsersReport.query.filter(UsersReport.login == login).first()
    if not user_report:
        return None
    return user_report


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
    return user_report


def verify_password(password, hash):
    return pbkdf2_sha256.verify(password, hash)


def get_user(login, password):
    if not (login and password):
        return None
    user_report = UsersReport.query.filter(UsersReport.login == login).first()
    if not user_report:
        return None
    if not verify_password(password, user_report.password):
        return None
    return user_report
