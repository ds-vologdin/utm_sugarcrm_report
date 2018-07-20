import logging

from .settings import config


logging_config = config.get('LOGGING')
if logging_config:
    logging.basicConfig(
        filename=logging_config.get('FILE'),
        level=logging_config.get('LEVEL'),
        format='%(asctime)s:%(name)s %(levelname)s:%(message)s'
    )
    logging.debug('Инициализация logging')

logger = logging.getLogger('utm_sugarcrm_report')
