from directory_watcher import DirectoryWatcher
import os
import time

pjoin = os.path.join
splitext = os.path.splitext
relpath = os.path.relpath

class HamlCompiler(object):
    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    compile_line = "ruby haml.rb {0} {1}"
    def process(self, source_file):
        dest_file = pjoin(self.dest_dir, relpath(source_file, self.source_dir))
        dest_file = splitext(dest_file)[0] + '.html'
        print 'Recompiling {0} to {1}'.format(source_file, dest_file)
        time.sleep(10)
        print '   ...done.'

 
if __name__ == "__main__":
    import re
    import sys
    re_haml = re.compile('.*\.haml$')
    processor = HamlCompiler(sys.argv[1], sys.argv[2])
    watcher = DirectoryWatcher(sys.argv[1], re_haml)
    watcher.watch(processor.process)