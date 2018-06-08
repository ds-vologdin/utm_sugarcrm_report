import os
import configparser
import logging


def convert_str_to_logging_level(level_str=None):
    if level_str == 'DEBUG':
        return logging.DEBUG
    if level_str == 'INFO':
        return logging.INFO
    if level_str == 'WARNING':
        return logging.WARNING
    if level_str == 'ERROR':
        return logging.ERROR
    if level_str == 'CRITICAL':
        return logging.CRITICAL
    # Значение по умолчанию
    return logging.WARNING


def parse_config_section_base(config=None):
    if not config:
        return {}
    if 'FLASK_DB' not in config:
        return {}

    databases = {
        'default': {
            key.upper(): config['FLASK_DB'][key]
            for key in config['FLASK_DB']
        }
    }
    # Эта секция приведена для примера, как расширять конфиг
    # Можно разделить TEST БД и PROD БД
    # if 'TEST_DB' not in config:
    #     databases.update({
    #         'test': {
    #             key.upper(): config['TEST_DB'][key]
    #             for key in config['TEST_DB']
    #         }
    #     })
    return databases


def parse_config_section_logging(config=None):
    if not config:
        return {}
    logging_config = {}
    if 'LOGGING' not in config:
        return {}
    # Если FILE не задано, то будет None - логи будут писаться в stdout
    logging_config['FILE'] = config['LOGGING'].get('FILE')
    logging_config['LEVEL'] = convert_str_to_logging_level(
        config['LOGGING'].get('LEVEL', logging.DEBUG)
    )
    return logging_config


def parse_config_section_application(config):
    if not config:
        return {}
    if 'APPLICATION' not in config:
        return {}
    return {
        key.upper(): config['APPLICATION'][key]
        for key in config['APPLICATION']
    }


def parse_config(file_config='/etc/utm_sugarcrm_report.conf'):
    # Берём данные из конфига (по умлочанию /etc/utm_sugarcrm_report.conf)
    # что бы не коммитить пароли
    # Пример конфига в flask_market.conf
    if not os.path.isfile(file_config):
        return None

    config = configparser.ConfigParser()
    try:
        config.read(file_config)
    except:
        return None

    databeses_config = parse_config_section_base(config)
    logging_config = parse_config_section_logging(config)
    application_config = parse_config_section_application(config)

    return {
        'DATABASES': databeses_config,
        'LOGGING': logging_config,
        'APPLICATION': application_config,
    }


file_config = '/etc/utm_sugarcrm_report.conf'
config = parse_config(file_config)
if not config:
    # если /etc/flask_market.conf не смогли прочитать, берём конфиг из примера
    logging.error('config file "{}" not found'.format(file_config))
    config = parse_config('flask_market.conf')

logging_config = config.get('LOGGING')
if logging_config:
    logging.basicConfig(
        filename=logging_config.get('FILE'),
        level=logging_config.get('LEVEL'),
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    logging.debug('Инициализация logging')
