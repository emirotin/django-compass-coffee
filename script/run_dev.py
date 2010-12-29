commands = [
    "python ./coffee_watch.py ../src/django_compass_coffee/assets/coffee ../src/django_compass_coffee/media/js", # compile coffee scripts
    "python ./files_watch.py ../src/django_compass_coffee/assets/js ../src/django_compass_coffee/media/js js", # copy js libraries

    "python ./haml_watch.py ../src/django_compass_coffee/assets/haml ../src/django_compass_coffee/templates", # compile haml templates
    "python ./files_watch.py ../src/django_compass_coffee/assets/html ../src/django_compass_coffee/media/html html", # copy regular html

    ("compass watch -c compass-config.rb", "../src/django_compass_coffee/assets/"), # run compass in watch mode to build sass
    "python ./files_watch.py ../src/django_compass_coffee/assets/css ../src/django_compass_coffee/media/css css", # copy plain css

    "python ./files_watch.py ../src/django_compass_coffee/assets/img ../src/django_compass_coffee/media/img \"gif|jpg|jpeg|png\"", # copy images
    
#    ("python manage.py runserver", "../src/django_compass_coffee") # run django server
]

from subprocess import STDOUT, Popen
import shlex
import signal
import sys
import types
import time

processes = []
for c in commands:
    if isinstance(c, types.StringTypes):
        p = Popen(shlex.split(c), stderr=STDOUT)
    else:
        p = Popen(shlex.split(c[0]), cwd=c[1], stderr=STDOUT)
    processes.append(p)

def terminate(*args):
    for p in processes:
        p.send_signal(signal.SIGINT)
        p.wait()
    sys.exit(0)

signal.signal(signal.SIGINT, terminate)
while True:
    # make it run until Ctrl-C pressed
    time.sleep(1)
