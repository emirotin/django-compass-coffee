import os
import shutil
import re
from subprocess import call, STDOUT
from directory_watcher import enum_files, mirror_path

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
            
def copy_file(source_file, dest_file):
    dest_dir = dirname(dest_file)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    copyfile(source_file, dest_file)        

def extensions_patterns(exts):
    return ['*.' + s for s in exts.split('|')]

def compile_coffee(source_file, dest_file):
    dest_file = dirname(dest_file)
    try:
        os.makedirs(dest_file)
    except OSError:
        pass
    print 'Compiling {0} to {1}'.format(source_file, dest_file)        
    retcode = call(["coffee",  "-o", dest_file, "-c", source_file], stderr=STDOUT)        
    print '   ...done. Return code: {0}'.format(retcode)
    return retcode

def compile_haml(source_file, dest_file):
    dest_dir = dirname(dest_file)
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    print 'Compiling {0} to {1}'.format(source_file, dest_file)
    retcode = call(["ruby", "haml.rb", source_file, dest_file], stderr=STDOUT)        
    print '   ...done. Return code: {0}'.format(retcode)