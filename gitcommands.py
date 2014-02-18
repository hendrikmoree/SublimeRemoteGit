from sublime_plugin import WindowCommand, TextCommand
from .utils import remoteCommand, findFilenameAndCommands, replaceView
from .commands import GIT_ADD, GIT_RM, GIT_RESET, GIT_CHECKOUT, GIT_DIFF, GIT_PUSH, GIT_PULL, GIT_COMMIT, GIT_STATUS

class _RemoteGitCommand(WindowCommand):
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

class RemoteGitStage(_RemoteGitCommand):
    commands = [GIT_ADD, GIT_RM]
    showOuput = False
    addFilename = True

class RemoteGitReset(_RemoteGitCommand):
    commands = [GIT_RESET]
    showOuput = False
    addFilename = True

class RemoteGitCheckout(_RemoteGitCommand):
    commands = [GIT_CHECKOUT]
    showOuput = False
    addFilename = True

class RemoteGitDiff(_RemoteGitCommand):
    commands = [GIT_DIFF]
    showOuput = True
    addFilename = True

class RemoteGitPush(_RemoteGitCommand):
    commands = [GIT_PUSH]
    showOuput = True
    addFilename = False

class RemoteGitPull(_RemoteGitCommand):
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
