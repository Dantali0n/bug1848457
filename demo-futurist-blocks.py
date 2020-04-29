from rrwlock import ReentrantReadWriteLock

import futurist
from futurist import waiters

def get_read(rrwlock):
    return rrwlock.read_acquire()

def get_write(rrwlock):
    return rrwlock.write_acquire()

def main():
    # the behavior is specific to GreenThreadPoolExecutor
    threadpool = futurist.GreenThreadPoolExecutor(max_workers=4)
    rrwlock = ReentrantReadWriteLock()
    futures = []
    futures.append(threadpool.submit(get_write, rrwlock))
    futures.append(threadpool.submit(get_read, rrwlock))

    # Get the results and verify only one of the calls succeeded
    # assert that the other call is still pending
    # this call will block indefinitely, it should not block state of threads
    # in threadpool should not be able to cause wait_for_any to block
    # indefinitely.
    results = waiters.wait_for_any(futures)

    # these statements will never be reached
    print(results[0].pop().result == True)
    print(len(results[1]))

if  __name__ =='__main__':main()
