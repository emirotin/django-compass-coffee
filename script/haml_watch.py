# written by Eugene Mirotin
# heavily based on http://www.bryceboe.com/2010/08/26/python-multiprocessing-and-keyboardinterrupt/

import sys
import time
import os
import re

import multiprocessing, signal, Queue

SLEEP_INTERVAL = 5

os_walk = os.walk
pjoin = os.path.join
re_haml = re.compile('.*\.haml$')
compile_line = "ruby haml.rb {0} {1}"

ROOT_DIR = os.path.realpath(pjoin(os.path.dirname(os.path.realpath(__file__)), '..'))
ASSETS_DIR = os.path.realpath(pjoin(ROOT_DIR, 'src', 'django_compass_coffee', 'assets'))
MEDIA_DIR = os.path.realpath(pjoin(ROOT_DIR, 'src', 'django_compass_coffee', 'media'))

HAML_DIR = pjoin(ASSETS_DIR, 'haml')
TEMPLATES_DIR = os.path.realpath(pjoin(ROOT_DIR, 'src', 'django_compass_coffee', 'templates'))

def compile(source_file):
    dest_file = pjoin(TEMPLATES_DIR, os.path.relpath(source_file, HAML_DIR))
    dest_file = os.path.splitext(dest_file)[0] + '.html'
    print 'Recompiling {0} to {1}'.format(source_file, dest_file)
    print '   ...done.'

def compile_next(job_queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    if job_queue.empty():
        return
    try:
        job = job_queue.get(block=False)
        compile(job)
    except Queue.Empty:
        pass

def enum_files(start_dir, mask):
    for (path, dirs, files) in os_walk(start_dir):
        for file in files:
            if not mask.match(file):
                continue
            yield pjoin(path, file)

def main():
    print 'Watching {0}'.format(HAML_DIR)
    filestamps = {}

    os_stat = os.stat
    
    job_queue = multiprocessing.Queue()
    current_worker = None
    try:
        while True:
            workers = []
            for file_name in enum_files(HAML_DIR, re_haml):
                try:
                    mtime = os_stat(file_name).st_mtime
                except OSError:
                    continue
                if file_name not in filestamps or mtime > filestamps[file_name]:
                    filestamps[file_name] = mtime            
                    job_queue.put(file_name)
                    worker = multiprocessing.Process(target=compile_next,
                                      args=(job_queue,))
                    workers.append(worker)
            for worker in workers:
                current_worker = worker
                worker.start()
                worker.join()
            current_worker = None
            
            #time.sleep(SLEEP_INTERVAL)
                
    except KeyboardInterrupt:
        print 'Received ctrl-c, waiting for running task to complete'
        if current_worker:
            current_worker.join()
        print '   ...done.'
        sys.exit(1)
 
if __name__ == "__main__":
    main()