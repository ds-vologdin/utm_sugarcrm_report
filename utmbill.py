from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from logging import getLogger
from datetime import datetime, date, timedelta
from itertools import groupby
from sqlalchemy import func

from utm_db import session_utm, engine_utm
from utm_db import PaymentTransactions, BalanceHistory, Users


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


# TODO: вынести в отдельный модуль
def get_report_begin_end_date(year='', month='', last='month'):
    '''Функция формирования даты начала и конца отчётного периода'''
    if year == '':
        # не задан год
        date_end = date.today()
        # Год не задан, берём период - последние 30 дней
        if last == 'week':
            date_begin = date_end - timedelta(days=6)
        elif last == 'month':
            date_begin = date_end - timedelta(days=30)
        elif last == 'quarter':
            date_begin = date_end - timedelta(days=90)
        elif last == 'year':
            date_begin = date_end.replace(year=(date_end.year-1), day=1)
        elif last == '2years':
            date_begin = date_end.replace(year=(date_end.year-2), day=1)
        elif last == '3years':
            date_begin = date_end.replace(year=(date_end.year-3), day=1)

        return date_begin, date_end

    if month == '':
        # Не задан месяц
        # Берём период - весь год
        date_begin = date(int(year), 1, 1)
        date_end = date(int(year), 12, 31)

        return date_begin, date_end

    # Задан месяц и год
    date_begin = date(int(year), int(month), 1)
    if int(month) < 12:
        date_end = date(int(year), int(month)+1, 1) - timedelta(days=1)
    else:
        date_end = date(int(year), 12, 31)

    return date_begin, date_end


def get_type_report(year, month):
    '''Частая конструкция для определения типа отчёта: last, year, month
    '''
    if year == '' and month == '':
        return 'last'
    if not year == '' and month == '':
        return 'year'
    if not year == '' and not month == '':
        return 'month'
    return ''


def get_last_months(last=12):
    ''' Функция генерации списка последних месяцев для выпадающего списка меню
    >>> len(get_last_months(12))
    12
    >>> len(get_last_months(2))
    2
    '''
    date_iter = date.today().replace(day=1)

    # Расчитываем дату последнего месяца
    if date_iter.month > last % 12:
        year_end = date_iter.year - last//12
        month_end = date_iter.month - last % 12
    else:
        year_end = date_iter.year - last//12 - 1
        month_end = date_iter.month - last % 12 + 12
    date_end = date(year=year_end, month=month_end, day=1)

    # Формируем список месяцев
    months_report = []
    while date_iter > date_end:
        months_report.append(date_iter)
        if date_iter.month == 1:
            date_iter = date_iter.replace(year=date_iter.year - 1, month=12)
        else:
            date_iter = date_iter.replace(month=date_iter.month - 1)
    return months_report


def get_last_years(last=5):
    ''' Функция генерации списка последних лет для выпадающего списка меню
    '''
    date_cur = date.today().replace(month=1, day=1)

    years_report = [
        date_cur.replace(year=date_cur.year - i)
        for i in range(last)
    ]
    return years_report


def next_month(date_val):
    if date_val.month < 12:
        return date_val.replace(month=date_val.month+1, day=1)
    else:
        return date(year=date_val.year+1, month=1, day=1)


def get_report_periods(date_begin, date_end):
    '''
    Формируем список дат: помесячный, если период более 120 дней
    понедельный, если от 31 до 120 дней
    подневной, если до 31 дня
    Возвращаем period
    period = [(d1, d2), (d2, d3), ..., (d(n-1), dn)]
    используем date >= d1 and date < d2, ... date >= d(n-1) and date < dn
    '''
    delta = date_end - date_begin

    # Подневная разбивка
    if delta < timedelta(days=31):
        return [
            (date_begin + timedelta(days=i), date_begin + timedelta(days=i+1))
            for i in range(delta.days + 1)
        ]
    # Понедельная разбивка
    if delta < timedelta(days=120):
        # Нас интересуют только полные недели
        days_to_new_week = (7 - date_begin.weekday()) % 7
        data_cur = date_begin + timedelta(days=days_to_new_week)
        delta = date_end - data_cur

        return [
            (data_cur + timedelta(days=i), data_cur + timedelta(days=i+7))
            for i in range(0, delta.days, 7)
        ]

    # Помесячная разбивка
    period = []

    # Нас интересуют только полные месяцы
    date_cur = next_month(date_begin) if date_begin.day > 1 else date_begin

    while date_cur <= date_end:
        period.append((date_cur, next_month(date_cur)))
        date_cur = next_month(date_cur)

    return period
# TODO: вынести в отдельный модуль


def group_pays_by_date(pays_raw):
    if not pays_raw:
        return []

    pays_with_date = (
        (date.fromtimestamp(timestamp), payment)
        for timestamp, payment in pays_raw
    )
    pays_group = []
    for date_pays, payments_gen in groupby(pays_with_date, lambda x: x[0]):
        payments_map = map(lambda x: x[1], payments_gen)
        payments_list = list(payments_map)
        pays_group.append({
            'date': date_pays,
            'summ': sum(payments_list),
            'count': len(payments_list),
        })
    return pays_group


def get_timestamp_from_date(date_current):
    if not date_current:
        return None
    return datetime.combine(
        date_current, datetime.min.time()
    ).timestamp()


def fetch_pays_from_utm(db, date_begin, date_end):
    '''Получить данные из БД UTM
    '''

    date_begin_timestamp = get_timestamp_from_date(date_begin)
    date_end_timestamp = get_timestamp_from_date(date_end)
    pays_raw = session_utm.query(
        PaymentTransactions.payment_enter_date,
        PaymentTransactions.payment_absolute
    ).filter(
        PaymentTransactions.method == 5
    ).filter(
        PaymentTransactions.payment_enter_date >= date_begin_timestamp
    ).filter(
        PaymentTransactions.payment_enter_date < date_end_timestamp
    ).all()

    return group_pays_by_date(pays_raw)


def calculate_pays_stat_periods(pays, report_periods):
    '''Функция рассчитывает статистику по платежам за каждый период
       в report_periods
    '''
    pays_periods_dicts = []
    # sum_tmp и count_tmp используется для расчёта смещения относительно
    # предыдущего отчётного периода
    sum_tmp = 0
    count_tmp = 0
    for date_begin, date_end in report_periods:
        pays_period = [
            pay for pay in pays
            if (pay.get('date') >= date_begin and pay.get('date') < date_end)
        ]
        # Расчитываем среднее значение и количество
        summ = 0
        count = 0
        for pay in pays_period:
            summ += pay.get('summ', 0)
            count += pay.get('count', 0)

        # Считаем среднее значение платежа (ARPU)
        avg_pay = summ/count if count > 0 else 0

        # Расчитываем изменение относительно предыдущего отчетного периода
        sum_dif = 0
        sum_dif_p = 0
        count_dif = 0
        count_dif_p = 0

        if sum_tmp > 0 and count_tmp > 0:
            sum_dif = summ - sum_tmp
            sum_dif_p = sum_dif*100/sum_tmp
            count_dif = count - count_tmp
            count_dif_p = count_dif*100/count_tmp

        sum_tmp = summ
        count_tmp = count

        pays_periods_dicts.append(
            {'date': date_begin,
             'summ': summ,
             'count': count,
             'avg': round(avg_pay, 2),
             'sum_dif': sum_dif,
             'sum_dif_p': round(sum_dif_p, 2),
             'count_dif': count_dif,
             'count_dif_p': round(count_dif_p, 2),
             }
        )
    return pays_periods_dicts


def fetch_balances_periods(db, report_periods):
    '''Функция расчёта баланса по заданным периодам
    '''
    # Расчитываем только в случае если отчёт помесячный
    date_begin, date_end = report_periods[0]
    if (date_end - date_begin) < timedelta(days=28):
        return None

    balances_dicts = []
    for date_begin, date_end in report_periods:
        # считаем сколько людей с положительным балансом перешло
        # на текущий месяц, какой у них средний баланс
        timestamp_begin = get_timestamp_from_date(date_begin)
        timestamp_end = get_timestamp_from_date(date_begin+timedelta(days=1))

        active_balance = session_utm.query(
            func.count(BalanceHistory.out_balance),
            func.avg(BalanceHistory.out_balance),
            func.sum(BalanceHistory.out_balance),
        ).join(
            Users, BalanceHistory.account_id == Users.basic_account
        ).filter(
            BalanceHistory.date >= timestamp_begin
        ).filter(
            BalanceHistory.date < timestamp_end
        ).filter(
            Users.login.op('~')('^\d\d\d\d\d$')
        ).filter(
            BalanceHistory.out_balance >= 0
        ).filter(
            BalanceHistory.out_balance < 15000
        ).all()

        # Смотрим средний баланс среди всех абонентов
        all_balance = session_utm.query(
            func.count(BalanceHistory.out_balance),
            func.avg(BalanceHistory.out_balance),
            func.sum(BalanceHistory.out_balance),
        ).join(
            Users, BalanceHistory.account_id == Users.basic_account
        ).filter(
            BalanceHistory.date >= timestamp_begin
        ).filter(
            BalanceHistory.date < timestamp_end
        ).filter(
            Users.login.op('~')('^\d\d\d\d\d$')
        ).filter(
            BalanceHistory.out_balance > -15000
        ).filter(
            BalanceHistory.out_balance < 15000
        ).all()

        count, avg, summ = active_balance[0] if len(active_balance) == 1 \
            else (0, 0, 0)

        avg_all = all_balance[0][0] if len(all_balance) == 1 else 0

        balances_dicts.append(
            {'date': date_begin,
             'count': count,
             'avg': avg,
             'summ': summ,
             'avg_all': avg_all,
             }
        )
    return balances_dicts


@utmbill.route('/pays/')
def utmpays_statistic(year='', month='', last='year', csv_flag=False):
    '''Функция формирует отчёт по платежам физ. лиц
    '''
    # if not request.user.groups.filter(name__exact='utmpays').exists():
    #     context = {'user': request.user.username,
    #                'error': 'Не хватает прав!'
    #                }
    #     return render_template(request, 'audit/error.html', context)

#     logger.info(
#         'user "%s" run function %s whith arguments last="%s" year="%s" \
# month="%s"' %
#         (request.user, utmpays_statistic.__name__, last, year, month)
#     )

    # Формируем даты начала и конца периода
    date_begin, date_end = get_report_begin_end_date(year, month, last)

    # Получаем данные из БД UTM
    # db = PgSqlDB()
    db = engine_utm
    pays = fetch_pays_from_utm(db, date_begin, date_end)

    # Формируем отчётные периоды (разбиваем date_begin - date_end на отрезки)
    report_periods = get_report_periods(date_begin, date_end)

    # Расчитываем помесячную статистику
    pays_stat_periods = calculate_pays_stat_periods(pays, report_periods)

    # Считаем статистику по всем платежам
    summ_pay, count_pay = 0, 0
    for pay in pays_stat_periods:
        summ_pay += pay['summ']
        count_pay += pay['count']

    if last == '':
        count_period = len(report_periods)
        avg_summ = summ_pay/count_period if count_period > 0 else 0
        avg_count = count_pay/count_period if count_period > 0 else 0
    else:
        # Не учитываем последний месяц (он чаще всего не полный)
        count_period = len(report_periods) - 1
        avg_summ = (summ_pay - pays_stat_periods[-1]['summ'])/count_period \
            if count_period > 0 else 0
        avg_count = (count_pay - pays_stat_periods[-1]['count'])/count_period \
            if count_period > 0 else 0

    avg_pays = summ_pay/count_pay if count_pay > 0 else 0

    pays_stat_summary = {
        'summ': summ_pay,
        'count': count_pay,
        'avg_summ': avg_summ,
        'avg_count': avg_count,
        'avg_pay': avg_pays,
    }

    # Запрашиваем помесячную статистику по исходящему остатку на начало месяца
    # и по количеству активных абонентов на начало месяца
    # Если статистика не помесячная, то balances_periods = None
    balances_periods = fetch_balances_periods(db, report_periods)

    # Объединяем pays_stat_periods и balances_periods
    if balances_periods:
        for i in range(len(pays_stat_periods)):
            pays_stat_periods[i]['count_active'] = \
                balances_periods[i].get('count', 0)

            pays_stat_periods[i]['avg_balance'] = \
                balances_periods[i].get('avg', 0)

            pays_stat_periods[i]['avg_balance_all'] = \
                balances_periods[i].get('avg_all', 0)

            pays_stat_periods[i]['sum_balance'] = \
                balances_periods[i].get('summ', 0)

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
    if balances_periods:
        return render_template('pays_year.html', **context)
    return render_template('index.html', **context)
