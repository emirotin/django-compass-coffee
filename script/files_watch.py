from directory_watcher import DirectoryWatcher
import os
import time
from utils import *
#from shutil import copyfile
#
#pjoin = os.path.join
#splitext = os.path.splitext
#relpath = os.path.relpath
#realpath = os.path.realpath

class FileCopier(object):
    def __init__(self, source_dir, dest_dir):
        self.source_dir = realpath(source_dir)
        self.dest_dir = realpath(dest_dir)

    def process(self, source_file):
        dest_file = copy_file(source_file, self.source_dir, self.dest_dir)
        print 'Copied {0} to {1}'.format(source_file, dest_file)        

 
if __name__ == "__main__":
    import re
    import sys
    if len(sys.argv) < 3:
        print "Usage: python files_watch.py SOURCE_DIR DEST_DIR [EXT], like: \n" + \
              "       python files_watch.py source/some_folder dest/some_folder\n" + \
              "or\n" + \
              "       python files_watch.py source/javascript dest/javascript js\n" + \
              "or\n" + \
              "       python files_watch.py source/img dest/img \"gif|jpg|jpeg|png\"\n"
        sys.exit(1)
    if len(sys.argv) > 3:
        re_exts = extensions_re(sys.argv[3])
    else:
        re_exts = None

    print 'Files watcher is running'

    processor = FileCopier(sys.argv[1], sys.argv[2])
    watcher = DirectoryWatcher(sys.argv[1], re_exts)
    watcher.watch(processor.process)