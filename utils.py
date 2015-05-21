from subprocess import Popen
from os.path import abspath, dirname, join, isfile
from json import dumps, loads
from SublimeUtils.sublimeutils import executeCommand

mydir = dirname(abspath(__file__))
lastCommandFile = join(mydir, "last-command")

def remoteCommand(view, command):
    def _do():
        return executeCommand(view, command.asList())
    result = _do()
    if 'Permission denied' in result:
        Popen("/usr/local/bin/cmc -X", shell=True).wait()
        result = _do()
    return command.parseResult(result)

def logCommand(view, command, args=None):
    view.lastcommand = [command, args]
    open(lastCommandFile, 'a').write(dumps([command, args]) + '\n')

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
    tags.sort(key=lambda v: list(map(lambda i: int(''.join(x for x in i if x.isdigit())), v.split()[0].split('.'))))
    return list(reversed(tags))