
from sublime_plugin import TextCommand, WindowCommand
from sublime import Region

from .classes.gitstatus import GitStatus
from .commands import GIT_STATUS, GIT_ADD, GIT_RESET, GIT_CHECKOUT, GIT_COMMIT, GIT_DIFF, GIT_PUSH, GIT_RM, GIT_PULL, GIT_CHECKOUT_BRANCH, GIT_CHECKOUT_NEW_BRANCH, GIT_MERGE_BRANCH
from .utils import remoteCommand

VIEW_PREFIX = "RemoteGit"
ST_VIEW_NAME = "%sSt" % VIEW_PREFIX

class RemoteGitSt(TextCommand):
    def run(self, edit):
        result = remoteCommand(self.view, GIT_STATUS)
        # result += remoteCommand(self.view, GIT_DIFF)

        if self.view.name().startswith(VIEW_PREFIX):
            replaceView(self.view, edit, result)
            view = self.view
        else:
            view = createView(self.view.window())
            replaceView(view, edit, result)
        gitStatus = GitStatus.fromMessage(view.substr(Region(0, view.size())))
        toLine = getattr(self.view, "lastlineno", gitStatus.firstlineno())
        gotoLine(view, gitStatus.closestLineNo(toLine))

def createView(window, name=ST_VIEW_NAME):
    view = window.new_file()
    view.set_name(name)
    view.set_scratch(True)
    view.settings().set('line_numbers', False)
    view.set_read_only(True)
    view.set_syntax_file('Packages/SublimeRemoteGit/RemoteGitSt.tmLanguage')
    return view

def replaceView(view, edit, content, name=ST_VIEW_NAME):
    if not view.name().startswith(VIEW_PREFIX):
        view = createView(view.window(), name=name)
    view.set_name(name)
    view.set_read_only(False)
    view.erase(edit, Region(0, view.size()))
    view.insert(edit, 0, content)
    view.set_read_only(True)

class ReplaceViewContent(TextCommand):
    def run(self, edit, content):
        replaceView(self.view, edit, content, name=VIEW_PREFIX)

class RemoteGitCommand(WindowCommand):
    def run(self):
        view = self.window.active_view()
        filename, commands = findFilenameAndCommands(view)
        command = None
        for c in commands:
            if c in self.commands:
                command = c
                break
        if command:
            if self.addFilename and filename:
                result = remoteCommand(view, command, filename)
            else:
                result = remoteCommand(view, command)
            if not self.showOuput:
                view.run_command("remote_git_st")
            else:
                view.run_command("replace_view_content", args=dict(content=result))

class RemoteGitStage(RemoteGitCommand):
    commands = [GIT_ADD, GIT_RM]
    showOuput = False
    addFilename = True

class RemoteGitReset(RemoteGitCommand):
    commands = [GIT_RESET]
    showOuput = False
    addFilename = True

class RemoteGitCheckout(RemoteGitCommand):
    commands = [GIT_CHECKOUT]
    showOuput = False
    addFilename = True

class RemoteGitDiff(RemoteGitCommand):
    commands = [GIT_DIFF]
    showOuput = True
    addFilename = True

class RemoteGitPush(RemoteGitCommand):
    commands = [GIT_PUSH]
    showOuput = True
    addFilename = False

class RemoteGitPull(RemoteGitCommand):
    commands = [GIT_PULL]
    showOuput = True
    addFilename = False

class RemoteGitCommit(TextCommand):
    def run(self, edit):
        result = remoteCommand(self.view, GIT_STATUS)
        result += remoteCommand(self.view, GIT_DIFF, "--staged")
        replaceView(self.view, edit, result)
        self.view.window().show_input_panel("Commit message: ", "", self.commit, None, None)

    def commit(self, message):
        remoteCommand(self.view, GIT_COMMIT, message)
        self.view.run_command("remote_git_st")

class _RemoteGitBranchCommand(TextCommand):
    def run(self, edit):
        self.view.window().show_input_panel("Branch name: ", "", self.checkout, None, None)

    def checkout(self, name):
        remoteCommand(self.view, self.command, name)

class RemoteGitCheckoutBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_BRANCH

class RemoteGitCheckoutNewBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_NEW_BRANCH

class RemoteGitMergeBranch(_RemoteGitBranchCommand):
    command = GIT_MERGE_BRANCH

class RemoteGitChangeLine(TextCommand):
    def run(self, edit, up=False):
        if self.view.name() != ST_VIEW_NAME:
            return
        gitStatus = GitStatus.fromMessage(self.view.substr(Region(0, self.view.size())))
        gotoLine(self.view, gitStatus.nextlineno(currentLineNo(self.view), up))
        self.view.lastlineno = currentLineNo(self.view)

class RemoteGitHelp(WindowCommand):
    def run(self):
        items = ['a (git add or git rm if deleted)', 'r (git reset HEAD)', 'c (git checkout)', 'm (git commit)', 'p (git push)', 'l (git pull)', 'd (git diff)']
        self.window.show_quick_panel(items, lambda x: None)

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
