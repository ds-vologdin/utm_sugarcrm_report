import flask
import flask_login
from urllib.parse import urlparse, urljoin

from app.logger import logger
from .forms import LoginForm
from .login_users import get_user


blueprint = flask.Blueprint(
    'auth', __name__, template_folder='templates/auth/',
    url_prefix='/auth'
)


def is_safe_url(target):
    ref_url = urlparse(flask.request.host_url)
    test_url = urlparse(urljoin(flask.request.host_url, target))
    return (test_url.scheme in ('http', 'https') and
            ref_url.netloc == test_url.netloc)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    logger.debug('login url: {} {} {}'.format(
        flask.request.url, flask.request.method, flask.request.data
    ))
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login = flask.request.form['login']
        password = flask.request.form['password']
        user = get_user(login, password)
        if not user:
            logger.warning(
                'Не удачная попытка авторизоваться (login: {})'.format(login)
            )
            return flask.render_template(
                flask.url_for('auth.login'),
                form=form,
                error='Не корректен логин или пароль. Попробуйте ещё раз.'
            )
        flask_login.login_user(user)
        flask.flash('Logged in successfully.')
        logger.debug('Logged in successfully.')
        next = flask.request.args.get('next')
        logger.debug('Redirect: next({}) or {}'.format(
            next, flask.url_for('utmbill.utmpays_statistic')
        ))
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(
            next or flask.url_for('index')
        )
    return flask.render_template('login.html', form=form)


@blueprint.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('auth.login'))
