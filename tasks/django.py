from task import Task
from util import bcolors, url_file, replace, run, load_template
import string
import sys
from subprocess import call
import os
import shutil
from tempfile import mkstemp
import subprocess
import re

class DjangoCreateApp(Task):
    def __init__(self, conf):
        Task.__init__(self,conf)
        self.name = 'Django Create App'
        self.addRequiredFields(['django_settings_template','django_reload_template_url','base_dir','app_name','domain_name','modules','mysql_username', 'mysql_password' ])
        self.checkRequiredConf(conf)
    
    def install(self):
        print 'Installing ' + self.name + '...'
        
        p = subprocess.Popen("pwd", stdout=subprocess.PIPE)
        current_folder = p.communicate()[0].rstrip()

        """ Create app and modules """
        os.chdir( self.base_dir + '/' + self.domain_name + "/private/")
        run("django-admin.py startproject {{app_name}}")
        os.chdir( self.app_name)
         
        for app in self.modules:
            run("python manage.py startapp " + app)
       
        """ Install reload script """
        os.chdir(current_folder)
 
        """ Configure settings.py according to source file """
        load_template(self.django_settings_template, "{{base_dir}}/{{domain_name}}/private/{{app_name}}/settings.py")  

        f = open(self.django_reload_template_url, 'r')
        template = f.read()
        
        template = re.sub('{{base_dir}}',self.base_dir, template)
        template = re.sub('{{domain_name}}', self.domain_name, template)
        template = re.sub('{{app_name}}', self.app_name, template)
        
        f = open( '/usr/local/bin/' + self.app_name + "-reload", 'w')
        f.write(template)
        f.close()

	#result = call("chmod +rx /usr/local/bin/" + self.app_name + "-reload",shell=True)
        run('chmod +rx /usr/local/bin/{{app_name}}-reload') 
 
        return True

    def uninstall(self):
        if os.path.exists(self.base_dir + '/' + self.domain_name + "/private/" + self.app_name):
            shutil.rmtree( self.base_dir + '/' + self.domain_name + "/private/" + self.app_name )
        run('rm -R /usr/local/bin/{{app_name}}-reload')
        return True

    def status(self):
        return True


class DjangoInstall(Task):
    
    def __init__(self, conf):
        Task.__init__(self,conf) 
        self.name = 'Django Install'
        self.required_conf = ['django_url,base_dir,domain_name'] 
	self.packages = ['python-mysqldb']

        Task.checkRequiredConf(self,conf)
          
    def dependencies(self):
        return []
    
    def install(self):
        print 'Installing ' + self.name + '...'
        
        #modules = map(__import__, moduleNames)
        django_installed = False
        try:
            modules = map(__import__, ['django'])
            django_installed = True
        except Exception:
            django_installed = False
        
        temp_folder = '/home/installers/'
 
        if ( not django_installed ):
            Job.install_packages(self)     
   
            self.dir_already_created = True
            if not os.path.exists(temp_folder):
                self.dir_already_created = False
                os.makedirs(temp_folder)
        
            self.django_file_name = url_file(self.django_url) 
         
            """ Download and install Django from given URL """
            run("curl " + self.django_url + " >> " +temp_folder + self.django_file_name)
            run("tar zxvf " + temp_folder + self.django_file_name  + " -C " + temp_folder)
            run("python " + temp_folder + self.django_file_name[:-7] + '/setup.py install')
         
            """ Copy styles """
            run("sudo cp -Rf " + temp_folder +self.django_file_name[:-7]+"/django/contrib/admin/media {{base_dir}}/{{domain_name}}/static/admin")
        
            """ Clean Django Installers """
            run("rm -R " + temp_folder + self.django_file_name[:-7] + "*")
        
        """ Install extras """
        extra1_url = "http://pypi.python.org/packages/2.6/s/setuptools/setuptools-0.6c11-py2.6.egg"
        run("curl " + extra1_url + " >> " + temp_folder + url_file(extra1_url))
        run("sh " + temp_folder  + url_file(extra1_url) )

        extra2_url = "http://www.saddi.com/software/flup/dist/flup-1.0.2-py2.6.egg"
        run("curl " + extra2_url + " >> " + temp_folder + url_file(extra2_url))
        run("easy_install " + temp_folder  + url_file(extra2_url))
        
        """ Clean extras """
        run("rm -R " + temp_folder + url_file(extra1_url) + "*")
        run("rm -R " + temp_folder + url_file(extra2_url) + "*")
 
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
