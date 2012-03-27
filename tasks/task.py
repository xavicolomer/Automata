import string
from util import is_package_installed, install_package, bcolors
import sys


class Task:
    
    packages = []
    
    def addRequiredFields(self,fields):
        self.settings = fields
 
    def checkRequiredConf(self, conf):
        for attr in self.settings:
            try:
                setattr(self,attr,getattr(conf,attr))
            except AttributeError:
                print bcolors.FAIL + self.name + ' requires you to specify [' + attr + '] attribute.' + bcolors.ENDC
                sys.exit()

    def __init__(self, conf):
        print 'init'
        self.name = 'Basic'
        self.settings = []
        self.addRequiredFields( ['server_user','server_password'])

        self.checkRequiredConf(conf) 
    
    def install_packages(self):
        """ Package installation """
        if ( self.packages ):
            print 'Packages required by ' + self.name + ': ' + string.join(self.packages, ",")
            for package in self.packages:
                if ( not is_package_installed(package, True) ):
                    install_package(package)    

    """A simple job class"""
    def dependencies(self):
        return []   

    def install(self):
        print 'Installing self'
        return True

    def uninstall(self):
        return True
    
    def is_installed(self):
        return True

    def configure(self, options):
        return True

    def restart(self):
        return True

    def status(self):
        return "ON"
