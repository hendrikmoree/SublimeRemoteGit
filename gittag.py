from .classes.commands import GitCommand, GIT_TAG, GIT_LIST_TAGS, GIT_REMOVE_TAG, GIT_PUSH
from sublime_plugin import TextCommand
from .utils import remoteCommand
from .sublime_utils import replaceView
from .gitbranchcommands import _RemoteGitBranchCommand
from sublime import message_dialog

class RemoteGitCreateTag(TextCommand):
    def run(self, edit):
        self.window = self.view.window()
        command = GitCommand(GIT_LIST_TAGS)
        result = '\n'.join(reversed(remoteCommand(self.view, command).strip().split('\n')))
        replaceView(self.view, edit, result)
        self.window.show_input_panel("Tag version:", "", self.message, None, None)

    def message(self, version):
        self.window.show_input_panel("Tag message:", "", lambda m: self.tag(version, m), None, None)

    def tag(self, version, message):
        command = GitCommand(GIT_TAG, message)
        command.addOption(version)
        command.addOption("-a")
        command.addOption("-m")
        result = remoteCommand(self.view, command)
        if result.strip():
            message_dialog(result.strip())
        else:
            pushCommand = GitCommand(GIT_PUSH)
            pushCommand.addOption("--tags")
            remoteCommand(self.view, pushCommand)
            message_dialog("Tag '%s' created and pushed" % version)


class RemoteGitListTags(_RemoteGitBranchCommand):
    listcommand = GIT_LIST_TAGS
    show = True
    choose = False

class RemoteGitRemoveTag(_RemoteGitBranchCommand):
    command = GIT_REMOVE_TAG
    listcommand = GIT_LIST_TAGS
