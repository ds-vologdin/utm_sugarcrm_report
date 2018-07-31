from flask_restful import Resource
import flask_login
from datetime import date

from .utm_block_user import fetch_users_block_month
from .helpers import get_report_begin_end_date


class BlockUsers(Resource):
    method_decorators = {
        'get': [flask_login.login_required],
    }

    def get(self, year=str(date.today().year), month=str(date.today().month)):
        date_start, date_stop = get_report_begin_end_date(year, month)
        users_block = fetch_users_block_month(date_start, date_stop)
        for user in users_block:
            user['date'] = str(user['date'])
        return users_block
