
from sublime_plugin import TextCommand, WindowCommand
from sublime import Region

from .classes.gitstatus import GitStatus
from .commands import GIT_STATUS, GitCommand
from .utils import remoteCommand, currentLineNo, gotoLine, replaceView, createView
from .constants import ST_VIEW_NAME, VIEW_PREFIX

class RemoteGitSt(TextCommand):
    def run(self, edit):
        result = remoteCommand(self.view, GitCommand(GIT_STATUS))
        if self.view.name().startswith(VIEW_PREFIX):
            replaceView(self.view, edit, result)
            view = self.view
        else:
            view = createView(self.view.window())
            replaceView(view, edit, result)
        gitStatus = GitStatus.fromMessage(view.substr(Region(0, view.size())))
        toLine = getattr(self.view, "laststatuslineno", gitStatus.firstlineno())
        gotoLine(view, gitStatus.closestLineNo(toLine))

class RemoteGitStatusChangeLine(TextCommand):
    def run(self, edit, up=False):
        if self.view.name() != ST_VIEW_NAME:
            return
        gitStatus = GitStatus.fromMessage(self.view.substr(Region(0, self.view.size())))
        gotoLine(self.view, gitStatus.nextlineno(currentLineNo(self.view), up))
        self.view.laststatuslineno = currentLineNo(self.view)

class RemoteGitStatusHelp(WindowCommand):
    def run(self):
        items = ['a (git add or git rm if deleted)', 'r (git reset HEAD)', 'c (git checkout)', 'm (git commit)', 'p (git push)', 'd (git diff)', 'l (git log)']
        self.window.show_quick_panel(items, lambda x: None)

class RemoteGitBack(WindowCommand):
    def run(self):
        for i in range(-1, -10, -1):
            command, args, _ = self.window.active_view().command_history(i)
            if 'change_line' not in command and 'replace_view_content' not in command:
                print (command, args)
                self.window.run_command(command, args=args)
                break
