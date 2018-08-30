from datetime import datetime, date, timedelta

from .helpers import get_timestamp_from_date
from .utm_db import session_utm
from .models import User, BlocksInfo, ServiceLink, ServicesDatum
from .models import TariffsHistory


def fetch_users_block_month(date_start, date_stop):
    ''' Функция для получения данных по блокировке пользователей UTM
    в промежутке между date_start, date_stop
    '''
    # Запрашиваем в БД список заблокированных пользователей
    timestamp_begin = get_timestamp_from_date(date_start)
    timestamp_end = get_timestamp_from_date(date_stop + timedelta(days=1))
    timestamp_expire = get_timestamp_from_date(date(2030, 1, 1))
    blocks = session_utm.query(
        User.id, User.login, User.full_name, User.actual_address,
        User.mobile_telephone, BlocksInfo.start_date
    ).join(
        BlocksInfo, User.basic_account == BlocksInfo.account_id
    ).filter(
        BlocksInfo.start_date >= timestamp_begin
    ).filter(
        BlocksInfo.start_date < timestamp_end
    ).filter(
        BlocksInfo.expire_date > timestamp_expire
    ).filter(
        User.login.op('~')('^\d\d\d\d\d$')
    ).order_by(BlocksInfo.start_date).all()

    User_id = [id for id, *block in blocks]

    # Запрашиваем активные сервисные связки
    services_User = session_utm.query(
        User.id, ServicesDatum.service_name, ServicesDatum.comment,
        ServicesDatum.id
    ).join(
        ServiceLink, User.basic_account == ServiceLink.account_id
    ).join(
        ServicesDatum, ServiceLink.service_id == ServicesDatum.id
    ).filter(
        User.id.in_(User_id)
    ).filter(
        ServicesDatum.is_deleted == 0
    ).filter(
        ServiceLink.is_deleted == 0
    ).filter(
        User.is_deleted == 0
    ).filter(
        ServicesDatum.id != 614
    ).order_by(User.id).all()

    User_block = []
    # Получаем тарифы пользователя и формируем список словарей с информацией
    # об ушёдшим в блок пользователям
    for block in blocks:
        services = [
            services_user for id, *services_user in services_User
            if id == block[0]
        ]
        service = ''

        if len(services) == 0:
            # Активных сервисных связок нет, запрашиваем историю тарифов
            tarif_history = session_utm.query(
                TariffsHistory.tariff_name, TariffsHistory.unlink_date
            ).join(
                User, TariffsHistory.account_id == User.basic_account
            ).filter(
                User.id == block[0]
            ).order_by(TariffsHistory.unlink_date.desc()).all()
            service = tarif_history[0][0] if len(tarif_history) > 0 else ''
        else:
            # Есть активные сервисные связки
            service_names = [ser[0] for ser in services]
            service = '; '.join(service_names)

        User_block.append(
            {
                'login': block[1],
                'user': block[2],
                'address': block[3],
                'phone': block[4],
                'date': datetime.fromtimestamp(block[5]),
                'tarif': service,
            }
        )
    return User_block
