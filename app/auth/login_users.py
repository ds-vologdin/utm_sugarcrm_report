import flask_login
from passlib.hash import pbkdf2_sha256
import logging
import base64

from .models import UsersReport


login_manager = flask_login.LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def user_loader(id):
    logging.debug('user_loader: {}'.format(id))
    user_report = UsersReport.query.filter(UsersReport.id == id).first()
    if not user_report:
        return None
    return user_report


def get_user_with_api_key(api_key):
    if not api_key:
        return
    return UsersReport.query.filter_by(api_key=api_key).first()


@login_manager.request_loader
def request_loader(request):
    logging.debug('request_loader')
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    user = get_user_with_api_key(api_key)
    if user:
        return user
    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
    user = get_user_with_api_key(api_key)
    if user:
        return user
    # next, try to login using form
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
