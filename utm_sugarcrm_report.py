import flask
import flask_login
from forms import LoginForm
from urllib.parse import urlparse, urljoin
import logging


from login_users import login_manager, get_user
from settings import config
from admin import create_admin


app = flask.Flask(__name__)
logging.debug('Создали app (app = Flask(__name__))')
admin = create_admin(app)

if 'APPLICATION' in config:
    app.secret_key = config['APPLICATION'].get(
        'SECRET',
        'aileechaiPh5ooDia9cioj2leibohsohque2Eim1aiJeetee3e'
    )
login_manager.init_app(app)


def is_safe_url(target):
    ref_url = urlparse(flask.request.host_url)
    test_url = urlparse(urljoin(flask.request.host_url, target))
    return (test_url.scheme in ('http', 'https') and
            ref_url.netloc == test_url.netloc)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
            logging.warning(
                'Не удачная попытка авторизоваться (login: {})'.format(login)
            )
            return flask.render_template(
                'login.html',
                form=form,
                error='Не корректен логин или пароль. Попробуйте ещё раз.'
            )
        flask_login.login_user(user)
        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))


@app.route('/')
def index():
    return flask.render_template(
        'index.html', current_user=flask_login.current_user
    )

if __name__ == '__main__':
    app.run(debug=True)
