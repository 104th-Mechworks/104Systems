import datetime
import os
from pathlib import Path
import logging
from logging import Formatter, getLogger, StreamHandler


class Color(object):
    """
     utility to return ansi colored text.
    """

    colors = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'bgred': 41,
        'bggrey': 100
    }

    prefix = '\033['

    suffix = '\033[0m'

    def colored(self, text, color=None):
        if color not in self.colors:
            color = 'white'

        clr = self.colors[color]
        return (self.prefix+'%dm%s'+self.suffix) % (clr, text)


colored = Color().colored




class ColoredFormatter(Formatter):

    def format(self, record):

        message = record.getMessage()

        mapping = {
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bgred',
            'DEBUG': 'bggrey',
            'SUCCESS': 'green'
        }

        clr = mapping.get(record.levelname, 'white')

        return colored(record.levelname, clr) + ': ' + message

logger = logging.getLogger("Datacore")
handler = StreamHandler()
formatter = ColoredFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

# set success level
logging.SUCCESS = 25  # between WARNING and INFO
logging.addLevelName(logging.SUCCESS, 'SUCCESS')
setattr(logger, 'success', lambda message, *args: logger._log(logging.SUCCESS, message, args))

if not Path("logs").exists():
    os.mkdir("logs")
if len(os.listdir("logs")) > 7:
    for file in os.listdir("logs"):
        os.remove("logs/" + file)
        break

log_path = f"logs/{logger.name} {datetime.datetime.now().strftime('%Y-%m-%d')}.log"
file_format = logging.Formatter(
    "[{levelname:^9}] [{asctime}] [{name}] [{module:^4}:{lineno:^4}] | {message}",
    style="{",
    datefmt="%d-%m-%y %H:%M:%S",
)
file_handler = logging.FileHandler(log_path, "a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.info('info')
    logger.success('success')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')