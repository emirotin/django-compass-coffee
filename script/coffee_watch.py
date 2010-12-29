from directory_watcher import DirectoryWatcher
import os
import time
from subprocess import call, STDOUT

pjoin = os.path.join
relpath = os.path.relpath
realpath = os.path.realpath
dirname = os.path.dirname

class CoffeeCompiler(object):
    def __init__(self, source_dir, dest_dir):
        self.source_dir = realpath(source_dir)
        self.dest_dir = realpath(dest_dir)

    def process(self, source_file):
        dest_file = pjoin(self.dest_dir, relpath(source_file, self.source_dir))
        dest_file = dirname(dest_file)
        try:
            os.mkdir(dest_file)
        except OSError:
            pass
        print 'Recompiling {0} to {1}'.format(source_file, dest_file)        
        retcode = call(["coffee",  "-o", dest_file, "-c", source_file], stderr=STDOUT)        
        print '   ...done. Return code: {0}'.format(retcode)

 
if __name__ == "__main__":
    import re
    import sys

    print 'Coffee watcher is running'

    re_coffee = re.compile('.*\.coffee$')
    processor = CoffeeCompiler(sys.argv[1], sys.argv[2])
    watcher = DirectoryWatcher(sys.argv[1], re_coffee)
    watcher.watch(processor.process)