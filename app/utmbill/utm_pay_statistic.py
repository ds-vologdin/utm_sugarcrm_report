from itertools import groupby
from operator import itemgetter
from sqlalchemy import func
from datetime import date, timedelta

from .utm_db import session_utm
from .utm_db import PaymentTransactions, BalanceHistory, Users
from .helpers import get_timestamp_from_date


def group_pays_by_date(pays_raw):
    if not pays_raw:
        return []

    pays_with_date = [
        (date.fromtimestamp(timestamp), payment)
        for timestamp, payment in pays_raw
    ]
    pays_group = []
    for date_pays, payments_gen in groupby(pays_with_date, itemgetter(0)):
        payments_list = list(map(itemgetter(1), payments_gen))
        pays_group.append({
            'date': date_pays,
            'summ': sum(payments_list),
            'count': len(payments_list),
        })
    return pays_group


def fetch_pays_from_utm(date_begin, date_end):
    '''Получить данные из БД UTM
    '''

    date_begin_timestamp = get_timestamp_from_date(date_begin)
    date_end_timestamp = get_timestamp_from_date(date_end + timedelta(days=1))
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
    # Запрашиваем помесячную статистику по исходящему остаткуна
    # на начало месяца и по количеству активных абонентов на начало месяца
    # Если статистика не помесячная, то balances_periods = None
    balances_periods = fetch_balances_periods(report_periods)

    # Объединяем pays_stat_periods и balances_periods
    if not balances_periods:
        return pays_periods_dicts
    for i in range(len(pays_periods_dicts)):
        pays_periods_dicts[i].update(
            {
                'count_active': balances_periods[i].get('count', 0),
                'avg_balance': balances_periods[i].get('avg', 0),
                'avg_balance_all': balances_periods[i].get('avg_all', 0),
                'sum_balance': balances_periods[i].get('summ', 0),
            }
        )
    return pays_periods_dicts


def calculate_summary_statistic_pays(pays_stat_periods, report_periods, last):
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

    return {
        'summ': summ_pay,
        'count': count_pay,
        'avg_summ': avg_summ,
        'avg_count': avg_count,
        'avg_pay': avg_pays,    # ARPU
    }


def fetch_balances_periods(report_periods):
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
