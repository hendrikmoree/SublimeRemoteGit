from .utils import findFilenameAndCommands, remoteCommand, lastCommand
from sublime_plugin import WindowCommand
from .constants import LOG_VIEW_NAME
from .commands import GitCommand, GIT_LOG

class RemoteGitLog(WindowCommand):
    def run(self, **kwargs):
        view = self.window.active_view()
        filename, commands = findFilenameAndCommands(view)
        if view.name() == LOG_VIEW_NAME:
            filename = lastCommand().value
        elif filename is None:
            filename = view.file_name()
        command = GitCommand(GIT_LOG, filename)
        if kwargs.get('patch') == True:
            command.addOption('-p')
        result = remoteCommand(view, command)
        view.run_command("replace_view_content", args=dict(content=result, name=LOG_VIEW_NAME))
