from sublime_plugin import TextCommand
from .utils import remoteCommand, logCommand
from .sublime_utils import findFilenameAndCommands, replaceView
from .classes.commands import GitCommand, GIT_ADD, GIT_ADD_ALL, GIT_RM, GIT_RESET, GIT_CHECKOUT, GIT_DIFF, GIT_PUSH, GIT_PULL, GIT_COMMIT, GIT_STATUS, GIT_LAST_COMMIT_MESSAGE
from .constants import ST_VIEW_NAME
from sublime import message_dialog

class _RemoteGitCommand(TextCommand):
    viewName = ST_VIEW_NAME
    showOuput = False
    addFilename = True

    def run(self, edit, **kwargs):
        view = self.view
        filename, commands = findFilenameAndCommands(view)
        command = None
        if self.addFilename and filename is None:
            filename = view.file_name()
            command = self.commands[0]
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
                logCommand(view, self.__class__.__name__)
                view.run_command("replace_view_content", args=dict(content=result, name=self.viewName))

class RemoteGitStage(_RemoteGitCommand):
    commands = [GIT_ADD, GIT_RM]

class RemoteGitStageAll(_RemoteGitCommand):
    addFilename = False
    commands = [GIT_ADD_ALL]

class RemoteGitReset(_RemoteGitCommand):
    commands = [GIT_RESET]

class RemoteGitCheckout(_RemoteGitCommand):
    commands = [GIT_CHECKOUT]

class RemoteGitDiff(_RemoteGitCommand):
    commands = [GIT_DIFF]
    showOuput = True

class RemoteGitPush(_RemoteGitCommand):
    commands = [GIT_PUSH]
    showOuput = True
    addFilename = False

class RemoteGitPull(_RemoteGitCommand):
    commands = [GIT_PULL]
    showOuput = True
    addFilename = False

class RemoteGitCommit(TextCommand):
    options = []

    def run(self, edit, presetMessage=""):
        result = remoteCommand(self.view, GitCommand(GIT_STATUS))
        command = GitCommand(GIT_DIFF)
        command.addOption("--staged")
        stagedDiff = remoteCommand(self.view, command)
        if not stagedDiff.strip():
            message_dialog("You have nothing staged for commit")
            return
        result += "\n" + stagedDiff
        replaceView(self.view, edit, result)
        self.view.window().show_input_panel("Commit message: ", presetMessage, self.commit, None, None)

    def commit(self, message):
        command = GitCommand(GIT_COMMIT, message)
        for o in self.options:
            command.addOption(o)
        command.addOption("-m")
        remoteCommand(self.view, command)
        self.view.run_command("remote_git_st")

class RemoteGitCommitAmend(RemoteGitCommit):
    options = ['--amend']

    def run(self, edit):
        presetMessage = remoteCommand(self.view, GitCommand(GIT_LAST_COMMIT_MESSAGE))
        super(RemoteGitCommitAmend, self).run(edit, presetMessage)

class RemoteGitCommitStageAll(RemoteGitCommit):
    def run(self, edit):
        self.view.run_command("remote_git_stage_all")
        super(RemoteGitCommitStageAll, self).run(edit)