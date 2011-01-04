commands = [
    "python ./coffee_watch.py ../src/django_compass_coffee/assets/site_media/js ../src/django_compass_coffee/site_media/js", # compile coffee scripts
    "python ./files_watch.py ../src/django_compass_coffee/assets/site_media/js ../src/django_compass_coffee/site_media/js js", # copy js libraries

    "python ./haml_watch.py ../src/django_compass_coffee/assets/templates ../src/django_compass_coffee/templates", # compile haml templates
    "python ./files_watch.py ../src/django_compass_coffee/assets/templates ../src/django_compass_coffee/templates html", # copy regular html

    ("compass watch -c compass-config.rb", "../src/django_compass_coffee/assets/site_media/"), # run compass in watch mode to build sass
    "python ./files_watch.py ../src/django_compass_coffee/assets/site_media/css ../src/django_compass_coffee/site_media/css css", # copy plain css

    "python ./files_watch.py ../src/django_compass_coffee/assets/site_media/img ../src/django_compass_coffee/site_media/img \"gif|jpg|jpeg|png\"", # copy images
    
    ("python manage.py runserver", "../src/django_compass_coffee") # run django server
]

from subprocess import STDOUT, Popen, call
import psutil
import shlex
import signal
import sys
import types
import time

print "Initially building assets"
call(shlex.split("python build_assets.py"), stderr=STDOUT)

processes = []
for c in commands:
    if isinstance(c, types.StringTypes):
        p = Popen(shlex.split(c), stderr=STDOUT)
    else:
        p = Popen(shlex.split(c[0]), cwd=c[1], stderr=STDOUT)
    processes.append(p)

def terminate(*args):
    for p in processes:
        pp = psutil.Process(p.pid)
        for child in pp.get_children():
            child.send_signal(signal.SIGINT)
            child.wait()
        p.send_signal(signal.SIGINT)
        p.wait()
    sys.exit(0)

signal.signal(signal.SIGINT, terminate)
while True:
    # make it run until Ctrl-C pressed
    time.sleep(1)
