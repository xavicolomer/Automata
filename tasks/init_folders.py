from task import Task
from util import bcolors
import string
import sys
from subprocess import call
import os
import shutil

class InitFolders(Task):
    
    def __init__(self, conf):
        Task.__init__(self,conf) 
        self.name = 'Init Folders'
        self.addRequiredFields(['base_dir','app_name','domain_name'])
  
        self.checkRequiredConf(conf)
          
    def dependencies(self):
        return []
    
    def install(self):
        print 'Installing ' + self.name + '...'
      
        """ Create all folders in cascade """
        path = ''  
        temp = self.base_dir + '/' + self.domain_name
         
        folders = temp.split('/')
        for folder in folders:
            path = path + folder + "/"
            if not os.path.exists(path):
                os.makedirs(path)
        
        """ Create a basic set of folders for the Django App """
        special_folders = ['public','private','log','backup','static','conf']
        for folder in special_folders:
            tmp = path + folder
            if not os.path.exists(tmp):
                print 'Creating folder: ' + folder
                os.makedirs(tmp)

        return True
    
    def uninstall(self):
        try:
            shutil.rmtree(self.base_dir + '/' + self.domain_name)
        except OSError:
            """ Directory was already deleted """
            return False
        return True
    
    def is_installed(self):
        return True
    
    def configure(self, options):
        return True

    def restart(self):
        return True

    def status(self):
        return "ON"
