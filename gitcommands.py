from sublime_plugin import TextCommand, EventListener
from .utils import remoteCommand, logCommand
from .sublime_utils import findFilenameAndCommands, replaceView
from .classes.commands import GitCommand, GIT_ADD, GIT_ADD_ALL, GIT_RM, GIT_RESET, GIT_CHECKOUT, GIT_DIFF, GIT_PUSH, GIT_PULL, GIT_COMMIT, GIT_STATUS, GIT_LAST_COMMIT_MESSAGE
from .constants import ST_VIEW_NAME, COMMIT_EDITMSG_VIEW_NAME
from sublime import message_dialog, Region, load_settings
from SublimeUtils.sublimeutils import projectRoot
from os import environ
from os.path import join

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

GIT_COMMIT_OPTIONS = {}
class RemoteGitCommit(TextCommand):
    options = []

    def run(self, edit, presetMessage=""):
        GIT_COMMIT_OPTIONS['options'] = self.options
        remoteCommand(self.view, GitCommand("git commit"))
        rootDir = self.view.rootDir if hasattr(self.view, 'rootDir') else projectRoot(self.view)
        GIT_COMMIT_OPTIONS['rootDir'] = rootDir
        result = open(join(rootDir, '.git', 'COMMIT_EDITMSG')).read().rstrip()
        command = GitCommand(GIT_DIFF)
        command.addOption("--staged")
        stagedDiff = remoteCommand(self.view, command)
        if not stagedDiff.strip():
            message_dialog("You have nothing staged for commit")
            return
        commitRegion = Region(len(presetMessage), len(result))
        result += "\n" + stagedDiff.strip()
        view = replaceView(self.view, edit, presetMessage + result, name=COMMIT_EDITMSG_VIEW_NAME)
        view.sel().clear()
        view.sel().add(Region(0, 0))
        view.set_read_only(False)
        view.add_regions(COMMIT_EDITMSG_VIEW_NAME, [commitRegion])

class RemoteGitCommitClose(EventListener):
    def on_pre_close(self, view):
        if view.name() != COMMIT_EDITMSG_VIEW_NAME:
            return
        commitRegion = view.get_regions(COMMIT_EDITMSG_VIEW_NAME)[0]
        if commitRegion.a > 0:
            data = view.substr(Region(0, commitRegion.b))
            open(join(GIT_COMMIT_OPTIONS['rootDir'], '.git', 'COMMIT_EDITMSG'), 'w').write(data)
            self.commit(view)

    def commit(self, view):
        view.rootDir = GIT_COMMIT_OPTIONS['rootDir']
        command = GitCommand(GIT_COMMIT)
        for o in GIT_COMMIT_OPTIONS['options']:
            command.addOption(o)
        command.addOption("--file .git/COMMIT_EDITMSG --cleanup strip")
        settings = load_settings('SublimeRemoteGit.sublime-settings')
        if settings.get('git_author_email') and settings.get('git_author_name'):
            command.addOption("--author '{0} <{1}>'".format(settings.get('git_author_name'), settings.get('git_author_email')))
        remoteCommand(view, command)
        views = view.window().views()
        preView = views[views.index(view) - 1]
        preView.run_command("remote_git_st")

class RemoteGitCommitAmend(RemoteGitCommit):
    options = ['--amend']

    def run(self, edit):
        presetMessage = remoteCommand(self.view, GitCommand(GIT_LAST_COMMIT_MESSAGE))
        super(RemoteGitCommitAmend, self).run(edit, presetMessage)

class RemoteGitCommitStageAll(RemoteGitCommit):
    def run(self, edit):
        self.view.run_command("remote_git_stage_all")
        super(RemoteGitCommitStageAll, self).run(edit)
