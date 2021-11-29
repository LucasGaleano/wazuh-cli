import logging
from logging import handlers, Formatter
from logging.handlers import SysLogHandler
from syslog import LOG_SYSLOG

log_format = '%(asctime)s %(levelname)s Wazuh-client[%(process)d]: %(message)s'
log_format_syslog = 'Wazuh-client[%(process)d]: %(message)s'
log_format_date = '%b %d %H:%M:%S'

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=log_format_date,
 )

handler = SysLogHandler('/dev/log',facility=LOG_SYSLOG)
handler.setFormatter(Formatter(fmt=log_format_syslog))

logger = logging.getLogger()
logger.addHandler(handler)

