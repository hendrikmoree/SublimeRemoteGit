
from sublime_plugin import TextCommand, WindowCommand
from sublime import Region

from .classes.gitstatus import GitStatus
from .commands import GIT_STATUS, GIT_ADD, GIT_RESET, GIT_CHECKOUT, GIT_COMMIT, GIT_DIFF, GIT_PUSH, GIT_RM, GIT_PULL, GIT_CHECKOUT_BRANCH, GIT_CHECKOUT_NEW_BRANCH, GIT_MERGE_BRANCH, GIT_LIST_BRANCH
from .utils import remoteCommand, currentLineNo, gotoLine, findFilenameAndCommands, replaceView, createView
from .constants import ST_VIEW_NAME, VIEW_PREFIX

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
        if self.choose:
            branches = [b.strip() for b in remoteCommand(self.view, GIT_LIST_BRANCH).strip().split('\n') if not b.startswith('*')]
            self.view.window().show_quick_panel(branches, lambda x: self.checkout(branches[x]) if x != -1 else None)
        else:
            self.view.window().show_input_panel("Branch name: ", "", self.checkout, None, None)

    def checkout(self, name):
        remoteCommand(self.view, self.command, name)
        self.view.run_command("remote_git_st")

class RemoteGitCheckoutBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_BRANCH
    choose = True

class RemoteGitCheckoutNewBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_NEW_BRANCH
    choose = False

class RemoteGitMergeBranch(_RemoteGitBranchCommand):
    command = GIT_MERGE_BRANCH
    choose = True

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
