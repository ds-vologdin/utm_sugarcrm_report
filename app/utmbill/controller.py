from flask import Blueprint
import flask_login
from flask_restful import Api
from logging import getLogger


from .helpers import get_report_begin_end_date
from .helpers import get_report_periods, get_type_report
from .helpers import get_last_years, get_last_months
from app.helpers import render_template_with_today_date

from .utm_pay_statistic import fetch_pays_from_utm, calculate_pays_stat_periods
from .utm_pay_statistic import calculate_summary_statistic_pays
from .utm_block_user import fetch_users_block_month

from .restful import BlockUsers

logger = getLogger(__name__)


utmbill = Blueprint(
    'utmbill', __name__, template_folder='templates/utmpays/',
    url_prefix='/utmbill'
)

api = Api(utmbill)
api.add_resource(BlockUsers,
                 '/api/pays/block/<string:year>/<string:month>',
                 '/api/pays/block/')


@utmbill.route('/pays/')
@utmbill.route('/pays/<int:year>')
@utmbill.route('/pays/<int:year>/<int:month>')
@flask_login.login_required
def utmpays_statistic(year='', month='', last='year'):
    '''Функция формирует отчёт по платежам физ. лиц
    '''
    date_begin, date_end = get_report_begin_end_date(year, month, last)
    pays = fetch_pays_from_utm(date_begin, date_end)
    report_periods = get_report_periods(date_begin, date_end)
    pays_stat_periods = calculate_pays_stat_periods(pays, report_periods)
    pays_stat_summary = calculate_summary_statistic_pays(
        pays_stat_periods, report_periods, last
    )

    # Формируем переменные для меню шаблона
    months_report = get_last_months(last=12)
    years_report = get_last_years(last=5)
    type_report = get_type_report(year, month)

    context = {
        'pays_stat': pays_stat_periods,
        'pays_stat_summary': pays_stat_summary,
        'months': months_report,
        'years': years_report,
        'type': type_report,
        'date_begin': date_begin,
        'menu_url': '/audit/utmpays/',
    }
    print(type_report)
    if type_report == 'month':
        return render_template_with_today_date('pays_month.html', context)
    return render_template_with_today_date('pays_year.html', context)


@utmbill.route('/pays/block/')
@utmbill.route('/pays/block/<string:year>/<string:month>')
@flask_login.login_required
def block_users_month(year='2018', month='01', ods_flag=False):
    '''Функция формирования отчёта по заблокированным пользователям
    за заданный месяц
    '''
    # Формируем даты начала и конца периода
    date_start, date_stop = get_report_begin_end_date(year, month)

    # Получаем список пользователей с блокировкой
    users_blok = fetch_users_block_month(date_start, date_stop)

    # Формируем переменные для меню шаблона
    months_report = get_last_months(last=12)

#     if ods_flag:
#         # Запрошен отчёт в ods файле
#         response = HttpResponse(content_type='application/ods')
#         response['Content-Disposition'] = 'attachment; filename=\
# "block_users_%s%s.ods"' % (year, month)
#         # Формируем ods файл
#         report_ods = create_ods_user_block_month(
#             users_blok, date_start, date_stop
#         )
#         report_ods.write(response)
#         return response

    # ods файл не запрошен
    context = {'blocks': users_blok,
               'date_begin': date_start,
               'months': months_report,
               }
    return render_template_with_today_date('block_month.html', context)
