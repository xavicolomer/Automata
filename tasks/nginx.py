from task import Task
from util import bcolors
import string
import sys
from subprocess import call
import os
import shutil
import re

class Nginx(Task):
    
    def __init__(self, conf):
        Task.__init__(self,conf) 
        self.name = 'Nginx'
        self.addRequiredFields(['base_dir','domain_name','nginx_template_url'])
        self.packages = ['nginx']

        self.checkRequiredConf(conf)
          
    def dependencies(self):
        return []
    
    def install(self):
        print 'Installing ' + self.name + '...'
         
        Task.install_packages(self)      
        
        """ Open template and substitute variables """ 
        f = open(self.nginx_template_url, 'r')
        template = f.read()
         
        template = re.sub('{{domain_name}}', self.domain_name, template)
        template = re.sub('{{base_dir}}', self.base_dir, template)
       
        f = open( self.base_dir + '/' + self.domain_name + '/conf/nginx.conf', 'w')
        f.write(template)
        f.close()               

        """ Link files to nginx """
	result = call("ln -s " + self.base_dir + '/' + self.domain_name + "/conf/nginx.conf /etc/nginx/sites-available/" + self.domain_name,shell=True)
        result = call("ln -s /etc/nginx/sites-available/" + self.domain_name  + "  /etc/nginx/sites-enabled/" + self.domain_name,shell=True)
       
        """ Restart Nginx """
        result = call("/etc/init.d/nginx restart", shell=True)
 
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
