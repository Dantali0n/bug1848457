from rrwlock import ReentrantReadWriteLock

from concurrent.futures import ThreadPoolExecutor

def read_lock(lock):
	lock.read_acquire()

def write_lock(lock):
	lock.write_acquire()

def main():
	local_lock = ReentrantReadWriteLock()

	import pdb; pdb.set_trace()

	executor = ThreadPoolExecutor(max_workers=2)

	futures = []
	future = executor.submit(read_lock, local_lock)
	futures.append(future)

	future2 = executor.submit(write_lock, local_lock)
	futures.append(future2)

	# This will loop indefinitely as one future will
	# never be done but it shouldn't block.
	# although similiar to waiters.wait_for_any this
	# would rather be 'spin_for_any' since it does
	# not use wait().
	while len(futures) > 0:
		for f in futures:
			if f.done():
				futures.remove(f)
				f.result()
				print("Future done")

if  __name__ =='__main__':main()
