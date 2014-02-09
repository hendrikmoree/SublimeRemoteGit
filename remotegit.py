
from sublime_plugin import TextCommand, WindowCommand
from sublime import Region, message_dialog

from .classes.gitstatus import GitStatus
from .commands import GIT_STATUS, GIT_ADD, GIT_RESET, GIT_CHECKOUT, GIT_COMMIT, GIT_DIFF, GIT_PUSH
from .utils import remoteCommand

class RemoteGitSt(TextCommand):
    def run(self, edit):
        result = remoteCommand(self.view, GIT_STATUS)
        result += remoteCommand(self.view, GIT_DIFF)

        if self.view.name() == "RemoteGitSt":
            replaceView(self.view, edit, result)
            view = self.view
        else:
            newView = self.view.window().new_file()
            newView.set_name("RemoteGitSt")
            newView.set_scratch(True)
            newView.set_syntax_file('Packages/SublimeRemoteGit/RemoteGitSt.tmLanguage')
            newView.insert(edit, 0, result)
            newView.set_read_only(True)
            view = newView
        gitStatus = GitStatus.fromMessage(view.substr(Region(0, view.size())))
        gotoLine(view, gitStatus.firstlineno())

def replaceView(view, edit, content):
    view.set_read_only(False)
    view.erase(edit, Region(0, view.size()))
    view.insert(edit, 0, content)
    view.set_read_only(True)

class RemoteGitCommand(TextCommand):
    def run(self, edit):
        filename, commands = findFilenameAndCommands(self.view)
        if self.command in commands:
            if self.addFilename and filename:
                result = remoteCommand(self.view, self.command, filename)
            else:
                result = remoteCommand(self.view, self.command)
            if not self.showOuput:
                self.view.run_command("remote_git_st")
            else:
                replaceView(self.view, edit, result)

class RemoteGitAdd(RemoteGitCommand):
    command = GIT_ADD
    showOuput = False
    addFilename = True

class RemoteGitReset(RemoteGitCommand):
    command = GIT_RESET
    showOuput = False
    addFilename = True

class RemoteGitCheckout(RemoteGitCommand):
    command = GIT_CHECKOUT
    showOuput = False
    addFilename = True

class RemoteGitDiff(RemoteGitCommand):
    command = GIT_DIFF
    showOuput = True
    addFilename = True

class RemoteGitPush(RemoteGitCommand):
    command = GIT_PUSH
    showOuput = True
    addFilename = False

class RemoteGitCommit(WindowCommand):
    def run(self):
        self.window.show_input_panel("Commit message: ", "", self.commit, None, None)

    def commit(self, message):
        view = self.window.active_view()
        remoteCommand(view, GIT_COMMIT, message)
        view.run_command("remote_git_st")

class RemoteGitChangeLine(TextCommand):
    def run(self, edit, up=False):
        currentLineNo, _ = self.view.rowcol(self.view.sel()[0].a)
        gitStatus = GitStatus.fromMessage(self.view.substr(Region(0, self.view.size())))
        gotoLine(self.view, gitStatus.nextlineno(currentLineNo, up))

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
