import flask_login


# Our mock database.
users = {
    'admin': {'password': 'admin', 'name': 'Vasya', 'email': 'vasya@mail.ru'}
}


login_manager = flask_login.LoginManager()


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
    user.email = users.get(login).get('email')
    return user


@login_manager.request_loader
def request_loader(request):
    login = request.form.get('login')
    if login not in users:
        return

    user = User()
    user.id = login

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = (
        request.form['password'] == users[login]['password']
    )
    return user


def get_user(login, password):
    if not (login and password):
        return None
    if login not in users:
        return None
    if password != users[login]['password']:
        return None
    user = User()
    user.id = login
    user.login = login
    user.name = users.get(login).get('name')
    user.email = users.get(login).get('email')
    return user
