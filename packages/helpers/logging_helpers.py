import logging
import os

# os.system('COLOR 12')
class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    blue = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format_long = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    _format_line = "\x1b[0m%(name)s \x1b[0m- {in_color}%(levelname)s - (%(filename)s:%(lineno)d) - %(message)s"
    _format = "\x1b[0m%(name)s - {in_color}%(levelname)s\x1b[0m - %(message)s"

    FORMATS = {
        logging.DEBUG: _format.format(in_color = grey),
        logging.INFO: _format.format(in_color = blue),
        logging.WARNING: _format_line.format(in_color = yellow),
        logging.ERROR: _format_line.format(in_color = red),
        logging.CRITICAL: _format_line.format(in_color = bold_red)
        # logging.DEBUG: reset + grey + _format + reset,
        # logging.INFO: reset + grey + _format + reset,
        # logging.WARNING: reset + yellow + _format + reset,
        # logging.ERROR: reset + red + _format + reset,
        # logging.CRITICAL: reset + bold_red + _format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    

def setup_logger(name: str, level = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)
    return logger
