from directory_watcher import MirrorDirectoriesHandler
from utils import copy_file

class MirrorHandler(MirrorDirectoriesHandler):
    def __init__(self, source_dir, dest_dir, extensions=None):
        if extensions is not None:
            extensions = ['*.{0}'.format(x) for x in extensions.split('|')]
        super(MirrorHandler, self).__init__(source_dir, dest_dir, patterns=extensions)

    def handle_file(self, source_path, dest_path):
        copy_file(source_path, dest_path)
        print 'Copied {0} to {1}'.format(source_file, dest_file)        

 
if __name__ == "__main__":
    import sys
    import time
    from watchdog.observers import Observer
    import signal

    observer = Observer()

    def terminate(*args):
        print '\nDirectory watcher is stopping...'
        observer.stop()
        observer.join()
        sys.exit(0)
    signal.signal(signal.SIGINT, terminate)
    
    if len(sys.argv) < 3:
        print "Usage: python files_watch.py SOURCE_DIR DEST_DIR [EXT], like: \n" + \
              "       python files_watch.py source/some_folder dest/some_folder\n" + \
              "or\n" + \
              "       python files_watch.py source/javascript dest/javascript js\n" + \
              "or\n" + \
              "       python files_watch.py source/img dest/img \"gif|jpg|jpeg|png\"\n"
        sys.exit(1)
    if len(sys.argv) > 3:
        exts = sys.argv[3]
    else:
        exts = None

    event_handler = MirrorHandler(sys.argv[1], sys.argv[2], exts)
    observer.schedule(event_handler, sys.argv[1], recursive=True)
    observer.start()
    print 'Directory watcher is running'
    while True:
        time.sleep(1)