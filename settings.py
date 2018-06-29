import os
import configparser
import logging


def convert_str_to_logging_level(level_str):
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    return level.get(level_str.lower(), logging.WARNING)


def get_all_parameters_in_section_from_config(config, section):
    if section not in config:
        return {}
    return {
        key.upper(): config[section][key] for key in config[section]
    }


def parse_config_section_base(config=None):
    databases = {
        'default': get_all_parameters_in_section_from_config(
            config, 'FLASK_DB'
        ),
        'utm': get_all_parameters_in_section_from_config(config, 'UTM_DB')
     }
    return databases


def parse_config_section_logging(config=None):
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
        format='%(asctime)s:%(name)s %(levelname)s:%(message)s'
    )
    logging.debug('Инициализация logging')
