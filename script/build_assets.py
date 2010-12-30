import shlex
from utils import *

for folder in [
   '../src/django_compass_coffee/media/js',
   '../src/django_compass_coffee/media/css',
   '../src/django_compass_coffee/media/img',
   '../src/django_compass_coffee/templates'
]:
    clear_folder(folder)
    
# build coffee files
source_dir = '../src/django_compass_coffee/assets/media/js/'
dest_dir = '../src/django_compass_coffee/media/js/'
re_coffee = re.compile('.*\.coffee$')
print 'Compiling coffee files to {0}'.format(dest_dir) 
for file in enum_files(source_dir, re_coffee):
    compile_coffee(file, source_dir, dest_dir)  
    
# build scss / sass with compass
print 'Compiling stylesheets with compass'
call(shlex.split("compass compile -c compass-config.rb"), cwd="../src/django_compass_coffee/assets/media/", stderr=STDOUT)

    
# copy static files
for folder, exts in (
        ('js', 'js'), 
        ('css', 'css'), 
        ('img', 'gif|png|jpg|jpeg')
    ):
    re_exts = extensions_re(exts)
    source_dir = '../src/django_compass_coffee/assets/media/' + folder
    print 'Copying files from {0}'.format(source_dir)
    dest_dir = '../src/django_compass_coffee/media/' + folder
    for file in enum_files(source_dir, re_exts):
        print '    Copied {0}'.format(copy_file(file, source_dir, dest_dir))

# check js files with jslint
for file in enum_files('../src/django_compass_coffee/media/js'):
    print "Running {0} through Javascript Lint".format(file)
    call(shlex.split("../tools/jsl -conf ../tools/jsl.conf -nologo -process {0}".format(file)), stderr=STDOUT)
        
# build haml files
re_haml = re.compile('.*\.haml')
source_dir = '../src/django_compass_coffee/assets/templates/'
dest_dir = '../src/django_compass_coffee/templates/'
print 'Compiling haml files to {0}'.format(dest_dir)
for file in enum_files(source_dir, re_haml):
    compile_haml(file, source_dir, dest_dir)


# copy html files   
re_html =  re.compile('.*\.html')
source_dir = '../src/django_compass_coffee/assets/templates/'
dest_dir = '../src/django_compass_coffee/templates/'
print 'Copying html files to {0}'.format(dest_dir)
for file in enum_files(source_dir, re_html):
    print '    Copied {0}'.format(copy_file(file, source_dir, dest_dir))
