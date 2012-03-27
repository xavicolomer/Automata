from task import Task
from util import is_package_installed, install_package, uninstall_package, bcolors,run
import string
import sys
from subprocess import call

class Mysql(Task):
    
    def __init__(self, conf):
        Task.__init__(self,conf) 
        self.name = 'MySql'
        self.packages = ['mysql-server','mysql-client']
        self.addRequiredFields(['mysql_username','mysql_database_name','mysql_password'])
        
        Task.checkRequiredConf(self,conf) 
         
    def dependencies(self):
        return []
    
    def executeQuery(self, query):
        return call("mysql -uroot -p" + self.mysql_password + " -e \"" + query + "\"" ,shell=True)

    def install(self):
        print 'Installing ' + self.name + '...'
        
        """ We save the password in the system for a non attended installation  """
        
        run("echo mysql-server mysql-server/root_password select {{mysql_password}} | debconf-set-selections")
        run("echo mysql-server mysql-server/root_password_again select {{mysql_password}} | debconf-set-selections")
        
        Task.install_packages(self)
 
        """ Create user and tables specified on the config file  """
        result = self.executeQuery("CREATE DATABASE " + self.mysql_database_name + ";")
        result = self.executeQuery("CREATE USER '" + self.mysql_username + "'@'localhost' IDENTIFIED BY '" + self.mysql_password + "';")         
        result = self.executeQuery("GRANT ALL PRIVILEGES ON " + self.mysql_database_name + " . * TO '" + self.mysql_username + "'@'localhost';")
        result = self.executeQuery("FLUSH PRIVILEGES;")

        return True
    
    def uninstall(self):
        print 'Uninstalling ' + self.name + '...'
        
        result = self.executeQuery("DROP USER '" + self.mysql_username + "'@'localhost';")
        result = self.executeQuery("DROP DATABASE " + self.mysql_database_name + ";")

        if ( self.packages ):
            print 'Packages required by ' + self.name + ': ' + string.join(self.packages, ",")
            for package in self.packages:
                if ( is_package_installed(package)):
                    uninstall_package(package)
        
        result = call("apt-get -y autoremove", shell=True)

        return True
    
    def is_installed(self):
        return True
    
    def configure(self, options):
        return True

    def restart(self):
        return True

    def status(self):
        return "ON"
