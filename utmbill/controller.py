from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from logging import getLogger

from .helpers import get_report_begin_end_date
from .helpers import get_report_periods, get_type_report
from .helpers import get_last_years, get_last_months

from .utm_pay_statistic import fetch_pays_from_utm, calculate_pays_stat_periods
from .utm_pay_statistic import fetch_balances_periods
from .utm_pay_statistic import calculate_summary_statistic_pays

logger = getLogger(__name__)


utmbill = Blueprint(
    'utmbill', __name__, template_folder='templates/utmpays/',
    url_prefix='/utmbill'
)


@utmbill.route('/', defaults={'page': 'index'})
@utmbill.route('/<page>')
def show(page):
    logger.debug('blueprint utmbill')
    template = '{}.html'.format(page)
    try:
        return render_template(template)
    except TemplateNotFound:
        logger.debug(
            'blueprint utmbill: TemplateNotFound ({})'.format(template)
        )
        abort(404)


@utmbill.route('/pays/')
def utmpays_statistic(year='', month='', last='year', csv_flag=False):
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

    return render_template('pays_year.html', **context)
