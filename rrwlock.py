from threading import Condition
from threading import RLock


class ReentrantReadWriteLock(object):
    """Dual lock wrapper to facilitate reentrant read / write lock pattern

    Implements second reader-writer problem (writer preference).

    Once python 2,7 is officially deprecated use this instead:
    https://pypi.org/project/readerwriterlock/

    """

    def __init__(self):

        self._read_lock = RLock()
        self._write_lock = RLock()
        self._condition = Condition()
        self._num_readers = 0
        self._wants_write = False

    def read_acquire(self, blocking=True):
        """Acquire a reentrant read lock

        Allows reentrant and multiple concurrent readers

        :param blocking: If the method is allowed to block or not
        :return: True if the lock was acquired false otherwise
        """
        int_lock = False
        try:
            if self._read_lock.acquire(blocking):
                int_lock = True
                while self._wants_write:
                    if not blocking:
                        return False
                    with self._condition:
                        self._condition.wait()
                self._num_readers += 1
                return True
            return False
        finally:
            if int_lock:
                self._read_lock.release()

     def write_acquire(self, blocking=True):
        """Acquire a reentrant write lock

        Allows reentrant writers.

        :param blocking: If the method is allowed to block or not
        :return: True if the lock was acquired false otherwise
        """
        int_lock = False
        try:
            if self._write_lock.acquire(blocking):
                int_lock = True
                while self._num_readers > 0 or self._wants_write:
                    if not blocking:
                        return False
                    with self._condition:
                        self._condition.wait()
                self._wants_write = True
                return True
            return False
        finally:
            if int_lock:
                self._write_lock.release()

