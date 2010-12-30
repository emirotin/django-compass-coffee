import os
import shutil
import re
from subprocess import call, STDOUT
from directory_watcher import enum_files

pjoin = os.path.join
splitext = os.path.splitext
relpath = os.path.relpath
realpath = os.path.realpath
copyfile = shutil.copyfile
dirname = os.path.dirname


def clear_folder(folder):
    folder = realpath(folder)
    for name in os.listdir(folder):
        name = pjoin(folder, name)
        if os.path.isdir(name):
            shutil.rmtree(name, True)
        else:
            try:
                os.remove(name)
            except OSError:
                pass
            
def copy_file(file, source_dir, dest_dir):
    dest_file = pjoin(dest_dir, relpath(file, source_dir))
    dest_dir = dirname(dest_file)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    copyfile(file, dest_file)        
    return dest_file

def extensions_re(exts):
    return re.compile('|'.join('.*\.' + s + '$' for s in exts.split('|')))

def compile_coffee(source_file, source_dir, dest_dir):
    dest_file = pjoin(dest_dir, relpath(source_file, source_dir))
    dest_dir = dirname(dest_file)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    print 'Compiling {0} to {1}'.format(source_file, dest_file)        
    retcode = call(["coffee",  "-o", dest_file, "-c", source_file], stderr=STDOUT)        
    print '   ...done. Return code: {0}'.format(retcode)
    return retcode

def compile_haml(source_file, source_dir, dest_dir):
    dest_file = pjoin(dest_dir, relpath(source_file, source_dir))
    dest_file = splitext(dest_file)[0] + '.html'
    dest_dir = dirname(dest_file)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    print 'Compiling {0} to {1}'.format(source_file, dest_file)
    retcode = call(["ruby", "haml.rb", source_file, dest_file], stderr=STDOUT)        
    print '   ...done. Return code: {0}'.format(retcode)