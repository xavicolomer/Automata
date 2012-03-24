import sys
import getopt
import apt
import string
from sys import stdout

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
