from pathtools.patterns import match_path
from watchdog.events import PatternMatchingEventHandler, \
    EVENT_TYPE_CREATED, EVENT_TYPE_MODIFIED, EVENT_TYPE_DELETED, EVENT_TYPE_MOVED
import os
from shutil import rmtree

pjoin = os.path.join
splitext = os.path.splitext
relpath = os.path.relpath
realpath = os.path.realpath
dirname = os.path.dirname
remove = os.remove
makedirs = os.makedirs
exists = os.path.exists

def enum_files(start_dir, mask=None):
    test = (lambda x : True) if mask is None else mask.match
    for (path, dirs, files) in os_walk(start_dir):
        for file in files:
            if not test(file):
                continue
            yield pjoin(path, file)


class PatternOrDirHandler(PatternMatchingEventHandler):
    def dispatch(self, event):
        """Overrides original method for better fine-tune - skip if
           * self.ignore_directories and event.is_directory
           * not event.is_directory and not path match 
        """
        
        is_directory = event.is_directory
        if self.ignore_directories and is_directory:
            return 
        
        event_type = event.event_type
        def match(path):
            return match_path(path, 
                              included_patterns=self.patterns,
                              excluded_patterns=self.ignore_patterns,
                              case_sensitive=self.case_sensitive)
                    
        has_match = ((event_type in (EVENT_TYPE_CREATED, EVENT_TYPE_MODIFIED, EVENT_TYPE_DELETED) and match(event.src_path) ) 
                    or (event_type == EVENT_TYPE_MOVED and match(event.dest_path)))
        if not has_match and not is_directory:
            return

        self.on_any_event(event)
        _method_map = {
            EVENT_TYPE_MODIFIED: self.on_modified,
            EVENT_TYPE_MOVED: self.on_moved,
            EVENT_TYPE_CREATED: self.on_created,
            EVENT_TYPE_DELETED: self.on_deleted,
        }
        _method_map[event_type](event)

class MirrorDirectoriesHandler(PatternOrDirHandler):
    def __init__(self, source_dir, dest_dir, change_ext=None, patterns=None, ignore_patterns=None):
        self.source_dir = realpath(source_dir)
        self.dest_dir = realpath(dest_dir)
        self.change_ext = change_ext
        super(MirrorDirectoriesHandler, self).__init__(patterns, ignore_patterns,
                 ignore_directories=False, case_sensitive=False)
        
    def handle_file(self, source_path, dest_path):
        """Define this method in derived classes"""
        raise NotImplemented
        
    def _wrap_handle_file(self, path):
        dest_path = self._mirror_path(path, False)
#        if (os.path.exists(dest_path) and 
#            os.path.isfile(dest_path) and 
#            os.stat(dest_path).st_mtime >= os.stat(path).st_mtime):
#            return
        self.handle_file(path, dest_path)
    
    def _mirror_path(self, path, is_directory):
        dest_path = pjoin(self.dest_dir, relpath(path, self.source_dir)) 
        if not is_directory and self.change_ext is not None:
            dest_path = '{0}.{1}'.format(splitext(dest_path)[0], self.change_ext)
        return dest_path
    
    def _create_dir(self, path, is_directory=False):
        dest_dir = self._mirror_path(path, is_directory)
        if not is_directory:
            dest_dir = dirname(dest_dir)
        if exists(dest_dir):
            return
        try:
            makedirs(dest_dir)
        except OSError as e:
            print "Error creating {0}: {1}".format(dest_dir, e)
    
    def _delete_path(self, path, is_directory):
        path_to_delete = self._mirror_path(path, is_directory)
        if exists(path_to_delete):
            return
        try:
            (rmtree if is_directory else remove)(path_to_delete)
        except OSError as e:
            print "Error deleting {0}: {1}".format(path, e)
    
    def on_moved(self, event):
        is_directory = event.is_directory
        self._create_dir(event.dest_path, is_directory)
        self._delete_path(event.src_path, is_directory)
        if is_directory:
            return
        self._wrap_handle_file(event.dest_path)

    def on_created(self, event):
        self._create_dir(event.src_path, event.is_directory)
        if event.is_directory:
            return
        self._wrap_handle_file(event.src_path)

    def on_deleted(self, event):
        self._delete_path(event.src_path, event.is_directory)

    def on_modified(self, event):
        if event.is_directory:
            return
        self._wrap_handle_file(event.src_path)

