from .utils import remoteCommand
from sublime_plugin import TextCommand
from .classes.commands import GitCommand, GIT_GREP
from .constants import GREP_VIEW_NAME

class RemoteGitGrep(TextCommand):

    def run(self, edit):
        self.view.window().show_input_panel("Grep: ", "", lambda s: self.grep(edit, s), None, None)

    def grep(self, edit, aString):
        command = GitCommand(GIT_GREP, aString)
        result = remoteCommand(self.view, command)
        self.view.run_command("replace_view_content", args=dict(content=result, name=GREP_VIEW_NAME))
