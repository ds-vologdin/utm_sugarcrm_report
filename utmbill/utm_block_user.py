from datetime import datetime, date, timedelta

from .helpers import get_timestamp_from_date
from .utm_db import session_utm
from .utm_db import Users, BlocksInfo, ServiceLinks, ServicesData
from .utm_db import TariffsHistory


def fetch_users_block_month(date_start, date_stop):
    ''' Функция для получения данных по блокировке пользователей UTM
    в промежутке между date_start, date_stop
    '''
    # Запрашиваем в БД список заблокированных пользователей
    timestamp_begin = get_timestamp_from_date(date_start)
    timestamp_end = get_timestamp_from_date(date_stop + timedelta(days=1))
    timestamp_expire = get_timestamp_from_date(date(2030, 1, 1))
    blocks = session_utm.query(
        Users.id, Users.login, Users.full_name, Users.actual_address,
        Users.mobile_telephone, BlocksInfo.start_date
    ).join(
        BlocksInfo,  Users.basic_account == BlocksInfo.account_id
    ).filter(
        BlocksInfo.start_date >= timestamp_begin
    ).filter(
        BlocksInfo.start_date < timestamp_end
    ).filter(
        BlocksInfo.expire_date > timestamp_expire
    ).filter(
        Users.login.op('~')('^\d\d\d\d\d$')
    ).order_by(BlocksInfo.start_date).all()

    users_id = [id for id, *block in blocks]

    # Запрашиваем активные сервисные связки
    services_users = session_utm.query(
        Users.id, ServicesData.service_name, ServicesData.comment,
        ServicesData.id
    ).join(
        ServiceLinks, Users.basic_account == ServiceLinks.account_id
    ).join(
        ServicesData, ServiceLinks.service_id == ServicesData.id
    ).filter(
        Users.id.in_(users_id)
    ).filter(
        ServicesData.is_deleted == 0
    ).filter(
        ServiceLinks.is_deleted == 0
    ).filter(
        Users.is_deleted == 0
    ).filter(
        ServicesData.id != 614
    ).order_by(Users.id).all()

    users_block = []
    # Получаем тарифы пользователя и формируем список словарей с информацией
    # об ушёдшим в блок пользователям
    for block in blocks:
        services = [
            services_user for id, *services_user in services_users
            if id == block[0]
        ]
        service = ''

        if len(services) == 0:
            # Активных сервисных связок нет, запрашиваем историю тарифов
            tarif_history = session_utm.query(
                TariffsHistory.tariff_name, TariffsHistory.unlink_date
            ).join(
                Users, TariffsHistory.account_id == Users.basic_account
            ).filter(
                Users.id == block[0]
            ).order_by(TariffsHistory.unlink_date.desc()).all()
            service = tarif_history[0][0] if len(tarif_history) > 0 else ''
        else:
            # Есть активные сервисные связки
            service_names = [ser[0] for ser in services]
            service = '; '.join(service_names)

        users_block.append(
            {
                'login': block[1],
                'user': block[2],
                'address': block[3],
                'phone': block[4],
                'date': datetime.fromtimestamp(block[5]),
                'tarif': service,
            }
        )
    return users_block
