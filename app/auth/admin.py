from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from passlib.hash import pbkdf2_sha256
from flask_login import current_user
import logging

from .models import UsersReport, session_global


class UsersReportAdmin(ModelView):
    def on_model_change(self, form, model, is_created):
        if 'pbkdf2-sha256' not in model.password:
            model.password = pbkdf2_sha256.hash(model.password)

    def is_accessible(self):
        if current_user.is_anonymous:
            logging.warning('anonymous пытается зайти в админку')
            return False

        if not current_user.is_active or not current_user.is_authenticated:
            logging.warning('кто-то ломится в админку')
            return False
        logging.debug(
            'UsersReportAdmin current_user: {}'.format(current_user.id)
        )

        # if current_user.has_role('superuser'):
        #     return True

        return True


def create_admin(app):
    admin = Admin(app, name='utm-sugarcrm-reports', template_mode='bootstrap3')
    admin.add_view(UsersReportAdmin(UsersReport, session_global))
    logging.debug('Создали админку')
    return admin
