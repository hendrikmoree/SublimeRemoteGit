from subprocess import Popen, PIPE
from os.path import abspath, dirname, join, isfile
from json import dumps, loads
from select import select

mydir = dirname(abspath(__file__))
lastCommandFile = join(mydir, "last-command")

def remoteCommand(view, command):
    rootDir = view.rootDir if hasattr(view, 'rootDir') else projectRoot(view)
    args = ["bash", "remote_command.sh", '"%s"' % rootDir] + command.asList()
    proc = Popen(' '.join(args), cwd=mydir, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True)
    r, _, _ = select([proc.stdout, proc.stderr], [], [], 5)
    if not r:
        print ('Popen timeout for command ' + str(args))
        proc.kill()
        return ""
    result = ""
    for out in r:
        result += ''.join([l.decode('utf-8') for l in out.readlines()])
        out.close()
    proc.wait()
    return command.parseResult(result)

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

def sortTags(tags):
    tags.sort(key=lambda v: list(map(int, v.split()[0].split('.'))))
    return list(reversed(tags))