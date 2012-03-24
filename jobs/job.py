class Job:
    
    packages = []
    
    def checkRequiredConf(self, conf):
        for attr in self.required_conf:
            try:
                setattr(self,attr,getattr(conf,attr))
            except AttributeError:
                print bcolors.FAIL + self.name + ' requires you to specify [' + attr + '] attribute.' + bcolors.ENDC
                sys.exit()

    def __init__(self, conf):
        self.name = 'Basic'
        self.required_conf = ['server_user','server_password']

        self.checkRequiredConf(conf) 

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
