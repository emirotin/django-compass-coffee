# The script to monitor directory changes and execute specific files on changed files
# Tasks are executed one by one, on keyboard interrupt the last task is waited to finish (not terminated)
# written by Eugene Mirotin, December 2010
# heavily based on http://www.bryceboe.com/2010/08/26/python-multiprocessing-and-keyboardinterrupt/

import sys
import os
import multiprocessing, Queue
from signal import signal, SIGINT, SIG_IGN

os_walk = os.walk
pjoin = os.path.join
realpath = os.path.realpath
os_stat = os.stat
    
class DirectoryWatcher(object):
    
    def __init__(self, start_dir, mask=None):
        self.start_dir = realpath(start_dir)
        self.mask = mask

    def __enum_files(self):
        for (path, dirs, files) in os_walk(self.start_dir):
            for file in files:
                if self.mask is not None and not self.mask.match(file):
                    continue
                yield pjoin(path, file)
                
    @staticmethod
    def __process_file(job_queue, process):
        signal(SIGINT, SIG_IGN)
        if job_queue.empty():
            return
        try:
            file = job_queue.get(block=False)
            process(file)
        except Queue.Empty:
            pass
    
    def watch(self, process):
        print 'Watching {0}'.format(self.start_dir)
        filestamps = {}
        
        job_queue = multiprocessing.Queue()
        current_worker = None
        try:
            while True:
                workers = []
                for file_name in self.__enum_files():
                    try:
                        mtime = os_stat(file_name).st_mtime
                    except OSError:
                        continue
                    if file_name not in filestamps or mtime > filestamps[file_name]:
                        filestamps[file_name] = mtime            
                        job_queue.put(file_name)
                        worker = multiprocessing.Process(target=DirectoryWatcher.__process_file,
                                          args=(job_queue, process))
                        workers.append(worker)
                for worker in workers:
                    current_worker = worker
                    worker.start()
                    worker.join()
                current_worker = None
                
        except KeyboardInterrupt:
            if current_worker:
                print 'Received ctrl-c, waiting for running task to complete'
                current_worker.join()
                print '   ...done.'
            else:
                print 'Received ctrl-c, exiting'
            return
