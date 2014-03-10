from .classes.commands import GitCommand, GIT_TAG, GIT_LIST_TAGS, GIT_REMOVE_TAG
from sublime_plugin import TextCommand
from .utils import remoteCommand
from .gitbranchcommands import _RemoteGitBranchCommand

class RemoteGitCreateTag(TextCommand):
    def run(self, edit):
        self.view.window().show_input_panel("Tag name:", "", self.message, None, None)

    def message(self, tagName):
        self.view.window().show_input_panel("Tag message:", "", lambda m: self.tag(tagName, m), None, None)

    def tag(self, tagName, message):
        command = GitCommand(GIT_TAG, message)
        command.addOption(tagName)
        command.addOption("-a")
        command.addOption("-m")
        remoteCommand(self.view, command)


class RemoteGitListTags(_RemoteGitBranchCommand):
    listcommand = GIT_LIST_TAGS
    show = True
    choose = False

class RemoteGitRemoveTag(_RemoteGitBranchCommand):
    command = GIT_REMOVE_TAG
    listcommand = GIT_LIST_TAGS
