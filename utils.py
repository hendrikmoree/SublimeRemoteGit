from subprocess import Popen, PIPE
from os.path import abspath, dirname, join, isfile
from json import dumps, loads

mydir = abspath(dirname(__file__))
lastCommandFile = join(mydir, "last-command")

def remoteCommand(view, command):
    rootDir = view.rootDir if hasattr(view, 'rootDir') else projectRoot(view)
    args = ["bash", "remote_command.sh", rootDir] + command.asList()
    proc = Popen(' '.join(args), cwd=mydir, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    stdout, stderr = proc.communicate(timeout=2)
    return stderr.decode('utf-8') + stdout.decode('utf-8')

def logCommand(view, command, args=None):
    view.lastcommand = [command, args]
    open(lastCommandFile, 'a').write(dumps([command, args]) + '\n')

def projectRoot(view):
    currentFile = view.file_name()
    if currentFile and view.window():
        for folder in view.window().folders():
            if folder in currentFile:
                return folder
    elif view.window() and view.window().folders():
        return view.window().folders()[0]

def lastCommand(historyIndex=0, remove=True):
    if isfile(lastCommandFile):
        lastCommands = open(lastCommandFile).readlines()
        command = lastCommands[-historyIndex]
        if len(lastCommands) > 10:
            lastCommands = lastCommands[-10:]
        if remove:
            lastCommands = lastCommands[:-historyIndex]
        open(lastCommandFile, 'w').write(''.join(lastCommands))
        return loads(command.strip())
    else:
        return {'RemoteGitSt': {}}
