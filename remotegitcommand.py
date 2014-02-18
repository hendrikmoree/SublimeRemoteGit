from sublime_plugin import WindowCommand
from .utils import remoteCommand, findFilenameAndCommands
from .commands import GIT_ADD, GIT_RM, GIT_RESET, GIT_CHECKOUT, GIT_DIFF, GIT_PUSH, GIT_PULL

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
