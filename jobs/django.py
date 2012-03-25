from job import Job
from util import bcolors, url_file, replace, run
import string
import sys
from subprocess import call
import os
import shutil
from tempfile import mkstemp
import subprocess
import re

class DjangoCreateAppJob(Job):
    def __init__(self, conf):
        Job.__init__(self,conf)
        self.name = 'Django Create App'
        self.addRequiredFields(['django_reload_template_url','base_dir','app_name','domain_name','modules','mysql_username', 'mysql_password' ])
        self.checkRequiredConf(conf)
    
    def install(self):
        print 'Installing ' + self.name + '...'
        
        p = subprocess.Popen("pwd", stdout=subprocess.PIPE)
        current_folder = p.communicate()[0].rstrip()

        """ Create app and modules """
        os.chdir( self.base_dir + '/' + self.domain_name + "/private/")
        result = call("django-admin.py startproject " + self.app_name,shell=True)
        os.chdir( self.app_name)
         
        for app in self.modules:
            result = call("python manage.py startapp " + app, shell=True)
        
        """ Configure settings.py according to source file """
        patterns = [ { "expr":"\'NAME\'(.*?),", "subst":"'NAME':'" + self.app_name + "'," },
                     { "expr":"\'ENGINE\'(.*?),", "subst":"'ENGINE':'django.db.backends.mysql'," },
                     { "expr":"\'USER\'(.*?),", "subst":"'USER':'" + self.mysql_username + "'," },
                     { "expr":"\'PASSWORD\'(.*?),", "subst":"'PASSWORD':'" + self.mysql_password + "'," }
                   ]					

        for pattern in patterns:
            replace(self.base_dir + '/' + self.domain_name + "/private/"+self.app_name+"/settings.py", pattern["expr"], pattern["subst"])
        
        """ Install reload script """
        os.chdir(current_folder)

        f = open(self.django_reload_template_url, 'r')
        template = f.read()
        
        template = re.sub('{{base_dir}}',self.base_dir, template)
        template = re.sub('{{domain_name}}', self.domain_name, template)
        template = re.sub('{{app_name}}', self.app_name, template)
        
        f = open( '/usr/local/bin/' + self.app_name + "-reload", 'w')
        f.write(template)
        f.close()

	result = call("chmod +rx /usr/local/bin/" + self.app_name + "-reload",shell=True)
         
 
        return True

    def uninstall(self):
        shutil.rmtree( self.base_dir + '/' + self.domain_name + "/private/" + self.app_name )
        return True

    def status(self):
        return True


class DjangoInstallJob(Job):
    
    def __init__(self, conf):
        Job.__init__(self,conf) 
        self.name = 'Django Install'
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
