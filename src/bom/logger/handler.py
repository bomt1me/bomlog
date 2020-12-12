""" handler.py """


import logging
import logging.handlers
import multiprocessing


class MultiprocessingFileHandler(logging.handlers.RotatingFileHandler):
    """ MultiprocessingFileHandler """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        filename,
        lock: multiprocessing.Lock,
        mode="a",
        maxBytes=1000000 * 10,
        backupCount=int(1000 / 10),
        encoding=None,
        delay=False,
        errors=None,
    ):
        """ __init__ """

        super().__init__(
            filename,
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            errors=errors,
        )
        self._lock = lock

    def emit(self, record):
        """
        Emit a record.
        Output the record to the file, catering for rollover as described
        in doRollover().
        """

        self._lock.acquire()
        try:
            if self.shouldRollover(record):
                self.doRollover()
            logging.FileHandler.emit(self, record)
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)
        finally:
            self._lock.release()
