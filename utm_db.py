from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, scoped_session
import logging

from settings import config


logger = logging.getLogger(__name__)


databases = config.get('DATABASES')
if not databases:
    logger.error('В конфиге не описана БД')

utm_db = databases.get('utm')
if not utm_db:
    logger.error('Проблемы с конфигом БД. Надо смотреть settings.py и конфиг')

logger.debug(utm_db)

engine_utm = create_engine(
    'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        utm_db.get('USER'),
        utm_db.get('PASSWD'),
        utm_db.get('HOST'),
        utm_db.get('PORT'),
        utm_db.get('DB')
    ),
    echo=True,
    pool_recycle=3600
)
logger.debug('Создали engine_utm')

metadata = MetaData()
metadata.reflect(engine_utm, only=[
    'payment_transactions', 'balance_history', 'users', 'blocks_info',
    'service_links', 'services_data', 'tariffs_history'
])
Base = automap_base(metadata=metadata)

session_factory_utm = sessionmaker(bind=engine_utm)
Session_utm = scoped_session(session_factory_utm)
session_utm = Session_utm()
Base.query = Session_utm.query_property()
logger.debug('Создали session')

Base.prepare()

PaymentTransactions = Base.classes.payment_transactions
logger.debug('Создали модель PaymentTransactions')
BalanceHistory = Base.classes.balance_history
logger.debug('Создали модель BalanceHistory')
Users = Base.classes.users
logger.debug('Создали модель Users')
BlocksInfo = Base.classes.blocks_info
logger.debug('Создали модель BlocksInfo')
ServiceLinks = Base.classes.service_links
logger.debug('Создали модель ServiceLinks')
ServicesData = Base.classes.services_data
logger.debug('Создали модель ServicesData')
TariffsHistory = Base.classes.tariffs_history
logger.debug('Создали модель TariffsHistory')
