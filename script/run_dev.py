from haml_watch import HamlHandler
from coffee_watch import CoffeeHandler
from files_watch import MirrorHandler
event_handlers = [
    (CoffeeHandler, "../src/django_compass_coffee/assets/site_media/js", "../src/django_compass_coffee/site_media/js"), # compile coffee files
    (MirrorHandler, "../src/django_compass_coffee/assets/site_media/js", "../src/django_compass_coffee/site_media/js", "js"), # copy js libraries

    (HamlHandler, "../src/django_compass_coffee/assets/templates", "../src/django_compass_coffee/templates"), # compile haml templates
    (MirrorHandler, "../src/django_compass_coffee/assets/templates", "../src/django_compass_coffee/templates", "html"), # copy regular html

    (MirrorHandler, "../src/django_compass_coffee/assets/site_media/css", "../src/django_compass_coffee/site_media/css", "css"), # copy plain css

    (MirrorHandler, "../src/django_compass_coffee/assets/site_media/img", "../src/django_compass_coffee/site_media/img", "gif|jpg|jpeg|png"), # copy images

]

commands = [
    ("compass watch -c compass-config.rb", "../src/django_compass_coffee/assets/site_media/"), # run compass in watch mode to build sass    
    ("python manage.py runserver", "../src/django_compass_coffee") # run django server
]

from subprocess import STDOUT, Popen, call
import psutil
import shlex
import signal
import sys
import types
import time
import os
from watchdog.observers import Observer

processes = []
observers = {}

def terminate(*args):
    print '\nExiting, stopping running processes...'
    for observer in observers.values():
        observer.stop()
        observer.join()
    for p in processes:
        pp = psutil.Process(p.pid)
        for child in pp.get_children():
            child.send_signal(signal.SIGINT)
            os.waitpid(child.pid)
        p.send_signal(signal.SIGINT)
        p.wait()
    print '   ...done.'
    sys.exit(0)
signal.signal(signal.SIGINT, terminate)

print "Initially building assets..."
call(shlex.split("python build_assets.py"), stderr=STDOUT)
print '   ...done.'

for h in event_handlers:
    dir = os.path.realpath(h[1])
    
    if dir in observers:
        observer = observers[dir]
    else:
        observer = Observer()
        observers[dir] = observer
        observer.start()
    event_handler = h[0](*h[1:])
    observer.schedule(event_handler, h[1], recursive=True)

for c in commands:
    if isinstance(c, types.StringTypes):
        p = Popen(shlex.split(c), stderr=STDOUT)
    else:
        p = Popen(shlex.split(c[0]), cwd=c[1], stderr=STDOUT)
    processes.append(p)

print 'Everything is up and running.'

while True:
    # make it run until Ctrl-C pressed
    time.sleep(1)
