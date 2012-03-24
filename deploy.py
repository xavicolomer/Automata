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

def usage():
    print 'Deploy Help'
    print ''
    print '-s, --source  Use  source to define a source file'

def getVarFromFile(filename):
    import imp
    f = open(filename)
    global settings
    settings = imp.load_source('settings', '', f)
    f.close()

def checkOpt(argv):
    print 'Deploying....'
    
    opts, args = getopt.getopt(argv, "s:d", ["source"])
    global source
    source = ''
    for o, a in opts:
        if o == "-s":
            source = a

    if ( source == '' ):
        print 'You must define at least a source file'

        return False

    deploy()

def checkPackage(package):
    cache = apt.Cache()
    cache.update()
    stdout.write('    Checking ' + package + '...............................................................')
    
    pkg = cache[package]
    
    installed = False
    
    if ( pkg.installed ):
        stdout.write('[' + bcolors.OKGREEN + 'INSTALLED' + bcolors.ENDC + ']')
        installed = True
    else:
        stdout.write('['+ bcolors.FAIL + 'NOT INSTALLED' + bcolors.ENDC + ']')
        
    stdout.flush()    
    stdout.write("\r  \r\n")

    if ( not installed ):
        print 'Installing ' + package
        pkg.mark_install()
        cache.commit()

def checkModePackages(mode):
    packages = []
    try:
        packages = getattr(settings.packages, mode)
    except AttributeError:
        print 'Source has not configured any packages for ' + mode
        return False

    if ( packages ):
        print 'Packages required by ' + mode + ': ' + string.join(packages, ",")
        for package in packages:
            checkPackage(package)


def deploy():
    getVarFromFile(source)

    print ''
    print 'Setting mode: ' + bcolors.WARNING + settings.mode.upper() + bcolors.ENDC
    print ''
    
    if ( settings.mode == 'preproduction' ):
        try:
            settings.packages
        except AttributeError:
            print 'Source file has not been configured properly. \'packages\' Missing'
            return
    
        checkModePackages('preproduction') 
               
    if ( settings.mode == 'productionn' ):
        try:
            settings.packages
        except AttributeError:
            print 'Source file has not been configured properly. \'packages\' Missing'
            return
            
        checkModePackages('production')

    checkModePackages('normal')

def main(argv):                         
    try:                                
        checkOpt(argv) 
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)                     

if __name__ == "__main__":
    main(sys.argv[1:])

def getVarFromFile(filename):
    import imp
    f = open(filename)
    global settings
    settings = imp.load_source('settings', '', f)
    f.close()





