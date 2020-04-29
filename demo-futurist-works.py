from rrwlock import ReentrantReadWriteLock

import futurist
from futurist import waiters

def get_read(rrwlock):
    return rrwlock.read_acquire()

def get_write(rrwlock):
    return rrwlock.write_acquire()

def main():
    # the behavior is specific to GreenThreadPoolExecutor
    threadpool = futurist.ThreadPoolExecutor(max_workers=4)
    rrwlock = ReentrantReadWriteLock()
    futures = []
    futures.append(threadpool.submit(get_write, rrwlock))
    futures.append(threadpool.submit(get_read, rrwlock))

    # Get the results and verify only one of the calls succeeded
    # assert that the other call is still pending
    results = waiters.wait_for_any(futures)

    # these statements will be printed
    print(results[0].pop().result == True)
    print(len(results[1]))

    # will block after this, __exit__ of threadpool will try to shutdown threads
    # which is blocked by the lock.

if  __name__ =='__main__':main()
