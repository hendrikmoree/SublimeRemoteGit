from sublime_plugin import WindowCommand, TextCommand
from .utils import remoteCommand, findFilenameAndCommands, replaceView
from .commands import GitCommand, GIT_ADD, GIT_RM, GIT_RESET, GIT_CHECKOUT, GIT_DIFF, GIT_PUSH, GIT_PULL, GIT_COMMIT, GIT_STATUS, GIT_LOG
from .constants import ST_VIEW_NAME, LOG_VIEW_NAME

class _RemoteGitCommand(WindowCommand):
    viewName = ST_VIEW_NAME

    def run(self, **kwargs):
        view = self.window.active_view()
        filename, commands = findFilenameAndCommands(view)
        if self.addFilename and filename is None:
            filename = view.file_name()
        command = None
        for c in commands:
            if c in self.commands:
                command = c
                break
        if command:
            command = GitCommand(command, filename if self.addFilename else None)
            for k, v in kwargs.items():
                if k in self.kwargs:
                    command.addOption(self.kwargs[k])
            result = remoteCommand(view, command)
            if not self.showOuput:
                view.run_command("remote_git_st")
            else:
                view.run_command("replace_view_content", args=dict(content=result, name=self.viewName))

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

class RemoteGitLog(_RemoteGitCommand):
    commands = [GIT_LOG]
    showOuput = True
    addFilename = True
    kwargs = {'patch': '-p'}
    viewName = LOG_VIEW_NAME

class RemoteGitCommit(TextCommand):
    def run(self, edit):
        result = remoteCommand(self.view, GitCommand(GIT_STATUS))
        command = GitCommand(GIT_DIFF)
        command.addOption("--staged")
        result += remoteCommand(self.view, command)
        replaceView(self.view, edit, result)
        self.view.window().show_input_panel("Commit message: ", "", self.commit, None, None)

    def commit(self, message):
        remoteCommand(self.view, GitCommand(GIT_COMMIT, message))
        self.view.run_command("remote_git_st")
