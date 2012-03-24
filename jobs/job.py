class Job:
    
    packages = []

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
