
from sublime_plugin import TextCommand, WindowCommand
from sublime import Region, message_dialog

from .classes.gitstatus import GitStatus
from .commands import GIT_STATUS, GIT_ADD, GIT_RESET, GIT_CHECKOUT, GIT_COMMIT, GIT_DIFF
from .utils import remoteCommand

class RemoteGitSt(TextCommand):
    def run(self, edit):
        result = remoteCommand(self.view, GIT_STATUS)
        result += remoteCommand(self.view, GIT_DIFF)
        if result.startswith("nothing to commit"):
            message_dialog(result)
            return

        if self.view.name() == "RemoteGitSt":
            self.view.set_read_only(False)
            self.view.erase(edit, Region(0, self.view.size()))
            self.view.insert(edit, 0, result)
            self.view.set_read_only(True)
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

class RemoteGitCommand(TextCommand):
    def run(self, edit):
        filename, commands = findFilenameAndCommands(self.view)
        if filename and self.command in commands:
            remoteCommand(self.view, '%s \"%s\"' % (self.command, filename))
            self.view.run_command("remote_git_st")

class RemoteGitAdd(RemoteGitCommand):
    command = GIT_ADD

class RemoteGitReset(RemoteGitCommand):
    command = GIT_RESET

class RemoteGitCheckout(RemoteGitCommand):
    command = GIT_CHECKOUT

class RemoteGitCommit(WindowCommand):
    def run(self):
        self.window.show_input_panel("Commit message: ", "", self.commit, None, None)

    def commit(self, message):
        view = self.window.active_view()
        remoteCommand(view, GIT_COMMIT + " \"%s\"" % message)
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
