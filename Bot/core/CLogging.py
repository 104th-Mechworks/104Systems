# class Color(object):
#     """
#     utility to return ansi colored text.
#     """

#     colors = {
#         "black": 30,
#         "red": 31,
#         "green": 32,
#         "yellow": 33,
#         "blue": 34,
#         "magenta": 35,
#         "cyan": 36,
#         "white": 37,
#         "bgred": 41,
#         "bggrey": 100,
#     }

#     prefix = "\033["

#     suffix = "\033[0m"

#     def colored(self, text, color=None):
#         if color not in self.colors:
#             color = "white"

#         clr = self.colors[color]
#         return (self.prefix + "%dm%s" + self.suffix) % (clr, text)


# colored = Color().colored

# import logging
# from logging import Formatter, StreamHandler, getLogger


# class ColoredFormatter(Formatter):
#     def format(self, record):
#         message = record.getMessage()

#         mapping = {
#             "INFO": "cyan",
#             "WARNING": "yellow",
#             "ERROR": "red",
#             "CRITICAL": "bgred",
#             "DEBUG": "bggrey",
#             "SUCCESS": "green",
#         }

#         clr = mapping.get(record.levelname, "white")

#         return colored(record.levelname, clr) + ": " + message


# logger = logging.getLogger(__name__)
# handler = StreamHandler()
# formatter = ColoredFormatter()
# handler.setFormatter(formatter)
# logger.addHandler(handler)

# # customist the log style to:  "[%(asctime)s %(levelname)s] %(name)s: %(message)s", %d/%m/%y %H:%M:%S"
# formatter = logging.Formatter(
#     "%(levelname)s [%(asctime)s] %(name)s: %(message)s", "%d/%m/%y %H:%M:%S"
# )
# handler.setFormatter(formatter)
# logger.addHandler(handler)


# # set success level
# logging.SUCCESS = 25  # between WARNING and INFO
# logging.addLevelName(logging.SUCCESS, "SUCCESS")
# setattr(
#     logger,
#     "success",
#     lambda message, *args: logger._log(logging.SUCCESS, message, args),
# )

# file = logging.FileHandler("botlog.log")
# logger.addHandler(file)

# if __name__ == "__main__":
#     logger.setLevel(logging.DEBUG)
#     logger.info("info")
#     logger.warning("warning")
#     logger.error("error")
#     logger.critical("critical")
#     logger.debug("debug")
#     logger.success("success")


import logging

log = logging.getLogger("ether")
logging.SUCCESS = 25  # between WARNING and INFO
logging.addLevelName(logging.SUCCESS, "SUCCESS")
setattr(
    log,
    "success",
    lambda message, *args: log._log(logging.SUCCESS, message, args),
)


class CustomFormatter(logging.Formatter):
    blue = "\x1b[34;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    green = "\x1b[32;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format_string = "%(asctime)s %(levelname)-8s | %(message)s"
    FORMATS = {
        logging.DEBUG: blue + format_string + reset,
        logging.INFO: blue + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
        logging.CRITICAL: bold_red + format_string + reset,
        logging.SUCCESS: green + format_string + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setFormatter(CustomFormatter())
log.addHandler(stream)


file = logging.FileHandler("logs.log")

log.addHandler(file)
