from subprocess import Popen, PIPE
from os.path import abspath, dirname
from .classes.gitstatus import GitStatus
from .constants import ST_VIEW_NAME, VIEW_PREFIX
from sublime import Region
from sublime_plugin import TextCommand

mydir = abspath(dirname(__file__))

def remoteCommand(view, command, option=None):
    args = ["bash", "remote_command.sh", projectRoot(view), '"%s"' % command]
    if option:
        args.append('"%s"' % option)
    proc = Popen(' '.join(args), cwd=mydir, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    stdout, stderr = proc.communicate(timeout=2)
    return stderr.decode('utf-8') + stdout.decode('utf-8')

def projectRoot(view):
    currentFile = view.file_name()
    if currentFile and view.window():
        for folder in view.window().folders():
            if folder in currentFile:
                return folder
    elif view.window() and view.window().folders():
        return view.window().folders()[0]

def currentLineNo(view):
    currentLineNo, _ = view.rowcol(view.sel()[0].a)
    return currentLineNo

def findFilenameAndCommands(view):
    row, col = view.rowcol(view.sel()[0].a)
    gitStatus = GitStatus.fromMessage(view.substr(Region(0, view.size())))
    return gitStatus.fileAndCommandsForLine(row)

def gotoLine(view, lineno):
    textPoint = view.text_point(lineno, 0)
    pointRegion = Region(textPoint, textPoint)
    view.sel().clear()
    view.sel().add(pointRegion)
    view.show(pointRegion)

def createView(window, name=ST_VIEW_NAME):
    view = window.new_file()
    view.set_name(name)
    view.set_scratch(True)
    view.settings().set('line_numbers', False)
    view.set_read_only(True)
    view.set_syntax_file('Packages/SublimeRemoteGit/RemoteGitSt.tmLanguage')
    return view


class ReplaceViewContent(TextCommand):
    def run(self, edit, content):
        replaceView(self.view, edit, content, name=VIEW_PREFIX)

def replaceView(view, edit, content, name=ST_VIEW_NAME):
    if not view.name().startswith(VIEW_PREFIX):
        view = createView(view.window(), name=name)
    view.set_name(name)
    view.set_read_only(False)
    view.erase(edit, Region(0, view.size()))
    view.insert(edit, 0, content)
    view.set_read_only(True)
