from subprocess import Popen, PIPE
from os.path import abspath, dirname, join, isfile
from .classes.gitstatus import GitStatus
from .constants import ST_VIEW_NAME, VIEW_PREFIX
from sublime import Region
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

def lastCommand(historyIndex=0):
    if isfile(lastCommandFile):
        lastCommands = open(lastCommandFile).readlines()
        if len(lastCommands) > 10:
            open(lastCommandFile, 'w').write(''.join(lastCommands[1:]))
        else:
            open(lastCommandFile, 'w').write(''.join(lastCommands[:-historyIndex]))
        return loads(lastCommands[-historyIndex].strip())
    else:
        return {'RemoteGitSt': {}}

def currentLineNo(view):
    currentLineNo, _ = view.rowcol(view.sel()[0].a)
    return currentLineNo

def findFilenameAndCommands(view):
    row, col = view.rowcol(view.sel()[0].a)
    gitStatus = GitStatus.fromMessage(view.substr(Region(0, view.size())))
    return gitStatus.fileAndCommandsForLine(row)

def gotoLine(view, lineno, atTop=False):
    if lineno is None:
        return
    textPoint = view.text_point(lineno, 0)
    pointRegion = Region(textPoint, textPoint)
    view.sel().clear()
    view.sel().add(pointRegion)
    if not atTop:
        view.show(pointRegion)
    else:
        top_offset = (lineno - 1) * view.line_height()
        view.set_viewport_position((0, top_offset), True)

def createView(window, name=ST_VIEW_NAME):
    view = window.new_file()
    view.set_name(name)
    view.set_scratch(True)
    view.settings().set('line_numbers', False)
    view.set_read_only(True)
    view.set_syntax_file('Packages/SublimeRemoteGit/%s.tmLanguage' % name)
    return view

def replaceView(view, edit, content, name=ST_VIEW_NAME):
    if not view.name().startswith(VIEW_PREFIX):
        view = createView(view.window(), name=name)
    view.set_name(name)
    view.set_read_only(False)
    view.erase(edit, Region(0, view.size()))
    view.insert(edit, 0, content)
    view.set_read_only(True)
    view.set_syntax_file('Packages/SublimeRemoteGit/%s.tmLanguage' % name)
