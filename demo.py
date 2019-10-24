from rrwlock import ReentrantReadWriteLock

from concurrent.futures import ThreadPoolExecutor

def read_lock(lock):
	lock.read_acquire()

def write_lock(lock):
	lock.write_acquire()

def main():
	local_lock = ReentrantReadWriteLock()

	import pdb; pdb.set_trace()

	with ThreadPoolExecutor(max_workers=2) as executor:
		# First task will submit fine
		future = executor.submit(read_lock, local_lock)
		# Second one will block indefinitely
		future2 = executor.submit(write_lock, local_lock)

if  __name__ =='__main__':main()