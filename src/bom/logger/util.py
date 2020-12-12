""" util.py """


import logging
import logging.config
import logging.handlers
from multiprocessing import Lock
from typing import Union

from bom.configuration.config import Config  # pylint: disable=import-error

from . import formatter  # pylint: disable=import-error
from . import handler  # pylint: disable=import-error


def setup_logger(
    config: Config, lock: Union[None, Lock] = None  # pylint: disable=unsubscriptable-object
) -> Lock:
    """ setup_logger """

    assert config

    if not lock:
        lock = Lock()
    json_formatter = formatter.JsonFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(json_formatter)
    stream_handler.set_name("root_stream_handler")
    file_handler = handler.MultiprocessingFileHandler(
        filename="bomt1me.log", lock=lock, mode="a"
    )
    file_handler.setFormatter(json_formatter)
    file_handler.set_name("root_file_handler")
    root = logging.getLogger()
    while root.hasHandlers():
        root.removeHandler(root.handlers[0])
    root.addHandler(stream_handler)
    root.addHandler(file_handler)
    root.setLevel(logging.DEBUG)
    return lock
