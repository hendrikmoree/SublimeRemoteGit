from sublime import ENCODED_POSITION
from sublime_plugin import TextCommand

from .utils import remoteCommand, projectRoot
from .sublime_utils import currentLineText
from .classes.commands import GitCommand, GIT_GREP
from .constants import GREP_VIEW_NAME

class RemoteGitGrep(TextCommand):

    def run(self, edit):
        self.view.window().show_input_panel("Grep: ", "", lambda s: self.grep(edit, s), None, None)

    def grep(self, edit, aString):
        command = GitCommand(GIT_GREP, aString)
        result = remoteCommand(self.view, command)
        self.view.run_command("replace_view_content", args=dict(content=result, name=GREP_VIEW_NAME))

class RemoteGitOpenGreppedLine(TextCommand):

    def run(self, edit):
        currentLine = currentLineText(self.view)
        filename, lineno, _ = currentLine.split(":", 2)
        filepath = "{0}/{1}:{2}".format(projectRoot(self.view), filename, lineno)
        self.view.window().open_file(filepath, ENCODED_POSITION)
