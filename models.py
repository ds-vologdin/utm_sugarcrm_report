from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import json
import logging

from settings import config


databases = config.get('DATABASES')
if not databases:
    logging.error('В конфиге не описана БД')

default_db = databases.get('default')
if not default_db:
    logging.error('Проблемы с конфигом БД. Надо смотреть settings.py и конфиг')

engine = create_engine(
    '{0}://{1}:{2}@{3}:{4}/{5}'.format(
        default_db['ENGINE'], default_db['USER'], default_db['PASSWORD'],
        default_db['HOST'], default_db['PORT'], default_db['DB']
    ),
    json_serializer=json.dumps,
    echo=False,
)
logging.debug('Создали engine')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
# Используем не общеупотребимое имя session, что б было меньше соблазна
# пользоваться глобальной переменной напрямую
session_global = Session()
logging.debug('Создали session')

Base = declarative_base()
Base.query = Session.query_property()
logging.debug('Создали Base')


class UsersReport(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(20), unique=True)
    name = Column(String(200))
    email = Column(String(200))

    def __init__(self, login, password, name, email):
        self.login = login
        self.password = password
        self.name = name
        self.email = email
