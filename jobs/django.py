from job import Job
from util import bcolors, url_file
import string
import sys
from subprocess import call
import os
import shutil

class DjangoJob(Job):
    
    def __init__(self, conf):
        Job.__init__(self,conf) 
        self.name = 'Django'
        self.required_conf = ['django_url'] 
	self.packages = ['python-mysqldb']

        Job.checkRequiredConf(self,conf)
          
    def dependencies(self):
        return []
    
    def install(self):
        print 'Installing ' + self.name + '...'

        temp_folder = '/home/installers/'
        
        Job.install_packages(self)     
   
        self.dir_already_created = True
        if not os.path.exists(temp_folder):
            self.dir_already_created = False
            os.makedirs(temp_folder)
        
        self.django_file_name = url_file(self.django_url) 
         
        """ Download and install Django from given URL """
        result = call("curl " + self.django_url + " >> " +temp_folder + self.django_file_name, shell=True )
        result = call("tar zxvf " + temp_folder + self.django_file_name  + " -C " + temp_folder, shell=True )
        result = call("python " + temp_folder + self.django_file_name[:-7] + '/setup.py install', shell = True )
        
        """ Clean Django Installers """
        result = call("rm -R " + temp_folder + self.django_file_name[:-7] + "*", shell=True)
        
        """ Install extras """
        extra1_url = "http://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11-py2.6.egg"
        result = call("curl " + extra1_url + " >> " + temp_folder + url_file(extra1_url), shell=True )
        result = call("sh " + temp_folder  + url_file(extra1_url), shell=True )

        extra2_url = "http://www.saddi.com/software/flup/dist/flup-1.0.2-py2.6.egg"
        result = call("curl " + extra2_url + " >> " + temp_folder + url_file(extra2_url), shell=True )
        result = call("easy_install " + temp_folder  + url_file(extra2_url),shell=True)
        
        """ Clean extras """
        result = call("rm -R " + temp_folder + url_file(extra1_url) + "*", shell=True)
        result = call("rm -R " + temp_folder + url_file(extra2_url) + "*", shell=True)
 
        return True
    
    def uninstall(self):
        if ( self.dir_already_created ):
            print 'a'
        return True
    
    def is_installed(self):
        return True
    
    def configure(self, options):
        return True

    def restart(self):
        return True

    def status(self):
        return "ON"
