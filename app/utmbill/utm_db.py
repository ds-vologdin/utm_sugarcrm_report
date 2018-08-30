import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.settings import config


logger = logging.getLogger(__name__)


databases = config.get('DATABASES')
if not databases:
    logger.error('В конфиге не описана БД')

utm_db = databases.get('utm')
if not utm_db:
    logger.error('Проблемы с конфигом БД. Надо смотреть settings.py и конфиг')

engine_utm = create_engine(
    'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        utm_db.get('USER'),
        utm_db.get('PASSWD'),
        utm_db.get('HOST'),
        utm_db.get('PORT'),
        utm_db.get('DB')
    ),
    echo=True,
    pool_recycle=600
)
logger.debug('Создали engine_utm')

session_factory_utm = sessionmaker(bind=engine_utm)
Session_utm = scoped_session(session_factory_utm)
session_utm = Session_utm()
