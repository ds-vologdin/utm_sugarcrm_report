from flask import Flask

from .settings import config
from .logger import logger

from app.auth.admin import create_admin
from app.utmbill.controller import utmbill
from app.auth.login_users import login_manager
from app.auth.controller import blueprint as auth_blueprint


def create_app():
    app = Flask(__name__)
    logger.debug('Создали app (app = Flask(__name__))')
    app.register_blueprint(utmbill)
    logger.debug('Зарегистрировали blueprint utmbill')
    app.register_blueprint(auth_blueprint)
    logger.debug('Зарегистрировали blueprint auth')
    admin = create_admin(app)

    if 'APPLICATION' in config:
        app.secret_key = config['APPLICATION'].get(
            'SECRET',
            'aileechaiPh5ooDia9cioj2leibohsohque2Eim1aiJeetee3e'
        )
    login_manager.init_app(app)

    return app

app_utm_sugarcrm_report = create_app()

import app.controller
