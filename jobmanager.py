import sys
from jobs.mysql import MysqlJob 
import getopt
from jobs.util import bcolors

def usage():
    print 'Deploy Help'
    print ''
    print '-s, --source  Use  source to define a source file'

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

    job = MysqlJob(settings)
    job.uninstall()

def status():
    return False

def install():
    getVarFromFile(source)

    print ''
    print 'Setting mode: ' + bcolors.WARNING + settings.mode.upper() + bcolors.ENDC
    print ''

    job = MysqlJob(settings)
    job.install()

def main(argv):
    print 'Running JobManager'
    checkOpt(argv)

if __name__ == "__main__":
    main(sys.argv[1:])
