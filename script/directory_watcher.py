from watchdog.events import PatternMatchingEventHandler
import os
pjoin = os.path.join
splitext = os.path.splitext
relpath = os.path.relpath
realpath = os.path.realpath
dirname = os.path.dirname

def enum_files(start_dir, mask=None):
    test = (lambda x : True) if mask is None else mask.match
    for (path, dirs, files) in os_walk(start_dir):
        for file in files:
            if not test(file):
                continue
            yield pjoin(path, file)


class MirrorDirectoriesHandler(PatternMatchingEventHandler):
    def __init__(self, source_dir, dest_dir, patterns=None, ignore_patterns=None):
        self.source_dir = realpath(source_dir)
        self.dest_dir = realpath(dest_dir)
        super(MirrorDirectoriesHandler, self).__init__(patterns, ignore_patterns,
                 ignore_directories=True, case_sensitive=False)
        
    def handle_file(self, source_path, dest_path):
        """Define this method in derived classes"""
        raise NotImplemented
        
    def _wrap_handle_file(self, path):
        dest_path = self.mirror_path(path)
#        if (os.path.exists(dest_path) and 
#            os.path.isfile(dest_path) and 
#            os.stat(dest_path).st_mtime >= os.stat(path).st_mtime):
#            return
        self.handle_file(path, dest_path)
    
    def mirror_path(self, path):
        return pjoin(self.dest_dir, relpath(path, self.source_dir))
    
    def create_dir(self, path):
        dest_dir = dirname(self.mirror_path(path))
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass
    
    def on_moved(self, event):
        self.create_dir(event.dest_path)
        if event.is_directory:
            return
        self._wrap_handle_file(event.dest_path)

    def on_created(self, event):
        self.create_dir(event.src_path)
        if event.is_directory:
            return
        self._wrap_handle_file(event.src_path)

    def on_deleted(self, event):
        try:
            os.remove(self.mirror_path(event.src_path))
        except OSError:
            pass

    def on_modified(self, event):
        if event.is_directory:
            return
        self._wrap_handle_file(event.src_path)

