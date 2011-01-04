import shlex
from utils import *


for folder in [
   '../src/django_compass_coffee/site_media/js',
   '../src/django_compass_coffee/site_media/css',
   '../src/django_compass_coffee/site_media/img',
   '../src/django_compass_coffee/templates'
]:
    clear_folder(folder)
    
# build coffee files
source_dir = '../src/django_compass_coffee/assets/site_media/js/'
dest_dir = '../src/django_compass_coffee/site_media/js/'
print 'Compiling coffee files to {0}'.format(dest_dir) 
for file in enum_files(source_dir, ['*.coffee']):
    compile_coffee(file, mirror_path(file, source_dir, dest_dir, 'js'))  

# check these files with jslint
for file in enum_files('../src/django_compass_coffee/site_media/js'):
    print "Running {0} through Javascript Lint".format(file)
    call(shlex.split("../tools/jsl -conf ../tools/jsl.conf -nologo -process {0}".format(file)), stderr=STDOUT)

    
# build scss / sass with compass
print 'Compiling stylesheets with compass'
call(shlex.split("compass compile -c compass-config.rb"), cwd="../src/django_compass_coffee/assets/site_media/", stderr=STDOUT)


        
# build haml files
source_dir = '../src/django_compass_coffee/assets/templates/'
dest_dir = '../src/django_compass_coffee/templates/'
print 'Compiling haml files to {0}'.format(dest_dir)
for file in enum_files(source_dir, ['*.haml']):
    compile_haml(file, mirror_path(file, source_dir, dest_dir, 'html'))

    
# copy static files
for folder, exts in (
        ('site_media/js', 'js'), 
        ('site_media/css', 'css'), 
        ('site_media/img', 'gif|png|jpg|jpeg'),
        ('templates', 'html'), 
        
    ):
    patterns = extensions_patterns(exts)
    source_dir = '../src/django_compass_coffee/assets/' + folder
    print 'Copying files from {0}'.format(source_dir)
    dest_dir = '../src/django_compass_coffee/' + folder
    for file in enum_files(source_dir, patterns):
        print '    {0}'.format(file)
        copy_file(file, mirror_path(file, source_dir, dest_dir))


