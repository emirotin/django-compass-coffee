from directory_watcher import DirectoryWatcher
from subprocess import call, STDOUT
from utils import compile_haml, realpath


class HamlCompiler(object):
    def __init__(self, source_dir, dest_dir):
        self.source_dir = realpath(source_dir)
        self.dest_dir = realpath(dest_dir)

    def process(self, source_file):
        compile_haml(source_file, self.source_dir, self.dest_dir)

 
if __name__ == "__main__":
    import re
    import sys
    
    import signal
    def terminate(*args):
        raise KeyboardInterrupt
    signal.signal(signal.SIGINT, terminate)
    
    print 'HAML watcher is running'
    
    re_haml = re.compile('.*\.haml$')
    processor = HamlCompiler(sys.argv[1], sys.argv[2])
    watcher = DirectoryWatcher(sys.argv[1], re_haml)
    watcher.watch(processor.process)