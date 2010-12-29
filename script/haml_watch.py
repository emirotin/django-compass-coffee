from directory_watcher import DirectoryWatcher
import os
import time
from subprocess import call, STDOUT

pjoin = os.path.join
splitext = os.path.splitext
relpath = os.path.relpath
realpath = os.path.realpath

class HamlCompiler(object):
    def __init__(self, source_dir, dest_dir):
        self.source_dir = realpath(source_dir)
        self.dest_dir = realpath(dest_dir)

    def process(self, source_file):
        dest_file = pjoin(self.dest_dir, relpath(source_file, self.source_dir))
        dest_file = splitext(dest_file)[0] + '.html'
        print 'Recompiling {0} to {1}'.format(source_file, dest_file)        
        retcode = call(["ruby", "haml.rb", source_file, dest_file], stderr=STDOUT)        
        print '   ...done. Return code: {0}'.format(retcode)
 
if __name__ == "__main__":
    import re
    import sys
    re_haml = re.compile('.*\.haml$')
    processor = HamlCompiler(sys.argv[1], sys.argv[2])
    watcher = DirectoryWatcher(sys.argv[1], re_haml)
    watcher.watch(processor.process)