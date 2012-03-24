from job import Job
from util import bcolors
import string
import sys
from subprocess import call
import os

class InitFolders(Job):
    
    def __init__(self, conf):
        Job.__init__(self,conf) 
        self.name = 'Init Folders'
        self.required_conf = ['base_dir','app_name','domain_name'] 
  
        Job.checkRequiredConf(self,conf)
          
    def dependencies(self):
        return []
    
    def install(self):
        print 'Installing ' + self.name + '...'
      
        """ Create all folders in cascade """
        path = ''  
        temp = self.base_dir + '/' + self.domain_name
         
        folders = temp.split('/')
        for folder in folders:
            print path + folder
            path = path + folder + "/"
            if not os.path.exists(path):
                os.makedirs(path)
        
        """ Create a basic set of folders for the Django App """
        special_folders = ['public','private','log','backup','static','conf']
        for folder in special_folders:
            tmp = path + folder
            if not os.path.exists(tmp):
                os.makedirs(tmp)

        return True
    
    def uninstall(self):
        folder = self.base_dir + '/' + self.domain_name
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e
        
        return True
    
    def is_installed(self):
        return True
    
    def configure(self, options):
        return True

    def restart(self):
        return True

    def status(self):
        return "ON"
