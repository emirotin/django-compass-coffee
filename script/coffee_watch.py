from directory_watcher import DirectoryWatcher
from utils import compile_coffee, realpath

class CoffeeCompiler(object):
    def __init__(self, source_dir, dest_dir):
        self.source_dir = realpath(source_dir)
        self.dest_dir = realpath(dest_dir)

    def process(self, source_file):
        compile_coffee(source_file, self.source_dir, self.dest_dir)

 
if __name__ == "__main__":
    import re
    import sys

    print 'Coffee watcher is running'

    re_coffee = re.compile('.*\.coffee$')
    processor = CoffeeCompiler(sys.argv[1], sys.argv[2])
    watcher = DirectoryWatcher(sys.argv[1], re_coffee)
    watcher.watch(processor.process)