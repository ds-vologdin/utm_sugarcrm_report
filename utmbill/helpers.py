from datetime import date, timedelta


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
