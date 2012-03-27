import sys
#from jobs.mysql import MysqlJob 
import getopt
from tasks.util import bcolors

def usage():
    print 'Deploy Help'
    print ''
    print '-s, --source  Use  source to define a source file'

def importTask(module,klass):
    mod = __import__(module, fromlist=[klass])
    klass = getattr(mod, klass)
    return klass

def getVarFromFile(filename):
    import imp
    f = open(filename)
    global settings
    settings = imp.load_source('settings', '', f)
    f.close()

def checkOpt(argv):
    print 'Deploying....'
    
    opts, args = getopt.getopt(argv, "s:a:", ["source","action"])
    global source
    source = ''
    action = ''
    for o, a in opts:
        if o == "-s":
            source = a
        elif o == "-a":
            action = a

    if ( source == '' ):
        print 'You must define at least a source file'
        return False

    if ( action == 'install' ):
        install()
    elif ( action == 'uninstall' ):
        uninstall()
    elif ( action == 'status' ):
        status()
    elif ( action == '' ):
        print 'No action has been defined'
        return False

def uninstall():
    getVarFromFile(source)

    for task in settings.tasks:
        x = task.rfind(".")
        klass = task[x+1:]
        module = task[:-len(task)+x]
        aTask = importTask(module,klass)(settings)
        aTask.uninstall()

def status():
    return False

def install():
    getVarFromFile(source)

    print ''
    print 'Setting mode: ' + bcolors.WARNING + settings.mode.upper() + bcolors.ENDC
    print ''

    for task in settings.tasks:
        x = task.rfind(".")
        klass = task[x+1:]
        module = task[:-len(task)+x]
        aTask = importTask(module,klass)(settings)
        aTask.install()

def main(argv):
    print 'Running JobManager'
    checkOpt(argv)

if __name__ == "__main__":
    main(sys.argv[1:])
