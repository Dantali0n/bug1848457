from threading import Condition
from threading import RLock


class ReentrantReadWriteLock(object):
    def __init__(self):

        self._read_lock = RLock()
        self._write_lock = RLock()
        self._condition = Condition()
        self._num_readers = 0
        self._wants_write = False

    def read_acquire(self, blocking=True):
        int_lock = False
        try:
            if self._read_lock.acquire(blocking):
                int_lock = True
                while self._wants_write:
                    if not blocking:
                        return False
                    with self._condition:
                        self._condition.wait()
                    first_it = False
                self._num_readers += 1
                return True
            return False
        finally:
            if int_lock:
                 self._read_lock.release()

    def write_acquire(self, blocking=True):
        int_lock = False
        try:
            if self._write_lock.acquire(blocking):
                int_lock = True
                while self._num_readers > 0 or self._wants_write:
                    if not blocking:
                        return False
                    with self._condition:
                        self._condition.wait()
                    first_it = False
                self._wants_write = True
                return True
            return False
        finally:
            if int_lock:
                self._write_lock.release()