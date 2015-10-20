# coding: utf-8

from __future__ import unicode_literals
from functools import wraps
import inspect
from itertools import izip
import logging
import sys


def setup_logging(stream_or_file=None, debug=False, name=None):
    """
    Create a logger for communicating with the user or writing to log files.
    By default, creates a root logger that prints to stdout.

    :param stream_or_file:
        The destination of the log messages. If None, stdout will be used.
    :type stream_or_file:
        `unicode` or `file` or None
    :param debug:
        Whether or not the logger will be at the DEBUG level (if False, the logger will be at the INFO level).
    :type debug:
        `bool` or None
    :param name:
        The logging channel. If None, a root logger will be created.
    :type name:
        `unicode` or None
    :return:
        A logger that's been set up according to the specified parameters.
    :rtype:
        :class:`Logger`
    """
    logger = logging.getLogger(name)
    if isinstance(stream_or_file, basestring):
        handler = logging.FileHandler(stream_or_file, mode='w')
    else:
        handler = logging.StreamHandler(stream_or_file or sys.stdout)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    return logger


def log_on_success(message, log_level=logging.INFO):
    """
    Decorator for logging a message after a method has completed.
    The message is formatted with the method's arguments.

    :param message:
        The message to log after a method has completed.
    :param log_level:
        The logging level to use for logging the message.
    """
    def wrapper(func):
        # Get the list of arguments to the function for use in formatting the message.
        argspec = inspect.getargspec(func)

        @wraps(func)
        def wrapped(self, *args, **kwargs):
            # Call the method and get its result.
            result = func(self, *args, **kwargs)
            # kwargs contains arguments passed by name.
            # args contains arguments passed positionally.
            # match up positional arg names and values
            for name, value in izip(argspec.args[1:], args):
                kwargs[name] = value
            # Log the message, formatted with the arguments, at the specified log level.
            logging.log(log_level, message.format(**kwargs))
            return result
        return wrapped
    return wrapper