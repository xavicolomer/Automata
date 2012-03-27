import sys
import getopt
import apt
import string
from sys import stdout
from os import remove, close
from tempfile import mkstemp
from shutil import move
import re
import inspect 
import pickle
from subprocess import call

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = "\033[1m"

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def translate(text):
    if "{{" in text:
        settings,instance = get_settings() 
        for setting in settings:
            value = instance.__dict__[setting]
            if ( isinstance(value,str)):
                text = re.sub("\{\{"+setting+"\}\}",value,text)
        return text        
    return text

def load_template(template_url, save_to=''):
    """ Install reload script """
    f1 = open(template_url, 'r')
    template = f1.read()
    template = translate(template)    
     
    if ( not save_to == '' ):
        f2 = open( translate(save_to), 'w')
        f2.write(template)
        f2.close()

    f1.close()
    return template

def get_settings():
    max_depth = 5
    current_depth = 1
        
    while current_depth <= 5: 
        m = inspect.stack()[current_depth][1]
        if not "util.py" in m:
            break
        else:
            current_depth = current_depth + 1
           
    frame, module, line, function, context, index = inspect.stack()[current_depth]
    self = frame.f_code.co_varnames[0]
    instance = frame.f_locals[self]
    try:
        return instance.settings, instance
    except Exception:
        print 'Only Task classes can execute run command'



def run(command):
    result = call(translate(command),shell=True)

def replace(file, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file)
    
    for line in old_file:
        new_file.write(re.sub(pattern, subst, line))
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    
    #Remove original file
    remove(file)
    
    #Move new file
    move(abs_path, file)


def url_file(url):
    slugs = url.split('/')
    return slugs[len(slugs)-1]


def is_package_installed(package, verbose = False):
    cache = apt.Cache()
    cache.update()

    if ( verbose ):
        stdout.write('    Checking ' + package + '...............................................................')

    pkg = cache[package]

    installed = False

    if ( pkg.installed ):
        if ( verbose ):
            stdout.write('[' + bcolors.OKGREEN + 'INSTALLED' + bcolors.ENDC + ']')
        installed = True
    else:
        if ( verbose ):
            stdout.write('['+ bcolors.FAIL + 'NOT INSTALLED' + bcolors.ENDC + ']')

    if ( verbose ):
        stdout.flush()
        stdout.write("\r  \r\n")

    return installed

def uninstall_package(package):
    print 'Installing ' + package
    
    cache = apt.Cache()
    cache.update()
    pkg = cache[package]
    pkg.mark_delete(True, True)
    cache.commit()

def install_package(package):
    print 'Installing ' + package

    cache = apt.Cache()
    cache.update()
    pkg = cache[package]
    pkg.mark_install()
    cache.commit()
