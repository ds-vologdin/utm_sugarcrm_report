import flask
import flask_login
from urllib.parse import urlparse, urljoin

from forms import LoginForm


app = flask.Flask(__name__)
# Change this!
app.secret_key = 'aileechaiPh5ooDia9cioj2leibohsohque2Eim1aiJeetee3e'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {
    'admin': {'password': 'admin', 'name': 'Vasya', 'email': 'vasya@mail.ru'}
}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(login):
    if login not in users:
        return

    user = User()
    user.id = login
    user.login = login
    user.name = users.get(login).get('name')
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = (
        request.form['password'] == users[email]['password']
    )
    return user


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if flask.request.method == 'GET':
#         return '''
#                <form action='login' method='POST'>
#                 <input type='text' name='email' id='email' placeholder='email'/>
#                 <input type='password' name='password' id='password' placeholder='password'/>
#                 <input type='submit' name='submit'/>
#                </form>
#                '''
#
#     email = flask.request.form['email']
#     print(email)
#     if email not in users:
#         return 'Bad login'
#     if flask.request.form['password'] == users[email]['password']:
#         user = User()
#         user.id = email
#         flask_login.login_user(user)
#         return flask.redirect(flask.url_for('protected'))
#
#     return 'Bad login'


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
        print('login: {}\npasword: {}'.format(login, password))
        if login not in users:
            print('Bad login')
            return 'Bad login'
        if password != users[login]['password']:
            print('Bad password')
            return 'Bad password'

        user = User()
        user.id = login
        user.login = login
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
    return 'Logged out'


@app.route('/')
def index():
    print('user: {}'.format(flask_login.current_user))
    print(flask_login.current_user.__dict__)
    return flask.render_template(
        'index.html', current_user=flask_login.current_user
    )

if __name__ == '__main__':
    app.run(debug=True)
