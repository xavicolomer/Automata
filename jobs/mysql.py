from job import Job
from util import is_package_installed, install_package, uninstall_package, bcolors
import string
import sys
from subprocess import call

class MysqlJob(Job):
    
    def __init__(self, conf):
        self.name = 'MySql'
        self.packages = ['mysql-server','mysql-client']
        self.required_conf = ['mysql_username','mysql_database_name','mysql_password'] 
  
        for attr in self.required_conf:
            try:
                setattr(self,attr,getattr(conf,attr))
            except AttributeError:
                print bcolors.FAIL + self.name + ' requires you to specify [' + attr + '] attribute.' + bcolors.ENDC 
                sys.exit()                     
    
    def dependencies(self):
        return []
    
    def install(self):
        print 'Installing ' + self.name + '...'
        
        """ We save the password in the system for a non attended installation  """
        
        result = call("echo mysql-server mysql-server/root_password select " + self.mysql_password +  " | debconf-set-selections",shell=True)
        result = call("echo mysql-server mysql-server/root_password_again select " + self.mysql_password + " | debconf-set-selections", shell=True)
        
        """ Package installation """
	if ( self.packages ):
            print 'Packages required by ' + self.name + ': ' + string.join(self.packages, ",")
            for package in self.packages:
                if ( not is_package_installed(package, True) ):
                    install_package(package)

 
        return True
    
    def uninstall(self):
        print 'Uninstalling ' + self.name + '...'

        if ( self.packages ):
            print 'Packages required by ' + self.name + ': ' + string.join(self.packages, ",")
            for package in self.packages:
                if ( is_package_installed(package)):
                    uninstall_package(package)

        return True
    
    def is_installed(self):
        return True
    
    def configure(self, options):
        return True

    def restart(self):
        return True

    def status(self):
        return "ON"
