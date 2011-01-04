from directory_watcher import MirrorDirectoriesHandler
from utils import compile_coffee

class CoffeeHandler(MirrorDirectoriesHandler):
    def __init__(self, source_dir, dest_dir):
        super(CoffeeHandler, self).__init__(source_dir, dest_dir, 'js', ['*.coffee'])

    def handle_file(self, source_path, dest_path):
        compile_coffee(source_path, dest_path)

 
if __name__ == "__main__":
    import sys
    import time
    from watchdog.observers import Observer
    import signal

    observer = Observer()

    def terminate(*args):
        print '\nCoffee watcher is stopping...'
        observer.stop()
        observer.join()
        sys.exit(0)
    signal.signal(signal.SIGINT, terminate)
    
    event_handler = CoffeeHandler(sys.argv[1], sys.argv[2])
    observer.schedule(event_handler, sys.argv[1], recursive=True)
    observer.start()
    print 'Coffee watcher is running'
    while True:
        time.sleep(1)