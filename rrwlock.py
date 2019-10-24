from threading import Condition
from threading import RLock

class ReentrantReadWriteLock(object):
    def __init__(self):

        self._read_lock = RLock()
        self._write_lock = RLock()
        self._rcondition = Condition(lock=self._read_lock)
        self._wcondition = Condition(lock=self._write_lock)
        self._num_readers = 0
        self._wants_write = False

    def read_acquire(self, blocking=True, timeout=-1):
        waitout = None if timeout == -1 else timeout
        first_it = True
        try:
            if self._read_lock.acquire(blocking, timeout):
                while self._wants_write:
                    if not blocking or not first_it:
                        return False
                    self._rcondition.wait(waitout)
                    first_it = False
                self._num_readers += 1
                return True
            return False
        finally:
            self._read_lock.release()

    def write_acquire(self, blocking=True, timeout=-1):
        waitout = None if timeout == -1 else timeout
        first_it = True
        try:
            if self._write_lock.acquire(blocking, timeout):
                while self._num_readers > 0 or self._wants_write:
                    if not blocking or not first_it:
                        return False
                    self._wcondition.wait(waitout)
                    first_it = False
                self._wants_write = True
                return True
            return False
        finally:
            self._write_lock.release()