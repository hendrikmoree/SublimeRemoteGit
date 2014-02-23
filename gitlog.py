from .utils import findFilenameAndCommands, remoteCommand, lastCommand, gotoLine, currentLineNo, replaceView
from sublime_plugin import WindowCommand, TextCommand
from .constants import LOG_VIEW_NAME
from .commands import GitCommand, GIT_LOG, GIT_SHOW

class RemoteGitLog(TextCommand):
    def run(self, edit, **kwargs):
        view = self.view
        print ('goto line ', getattr(view, "lastloglineno", 1))
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
        gotoLine(view, getattr(view, "lastloglineno", 1))

class RemoteGitShowCommit(TextCommand):
    def run(self, edit):
        currentLine = self.view.substr(self.view.line(self.view.sel()[0]))
        commit = currentLine.split()[1]
        result = remoteCommand(self.view, GitCommand(GIT_SHOW, commit))
        replaceView(self.view, edit, result, name=LOG_VIEW_NAME)

class RemoteGitLogChangeLine(TextCommand):
    def run(self, edit, up=False):
        if self.view.name() != LOG_VIEW_NAME:
            return
        gotoNextCommit(self.view, up=up, currentLine=currentLineNo(self.view))
        self.view.lastloglineno = currentLineNo(self.view)
        print('set lastloglineno', self.view.lastloglineno)

def gotoNextCommit(view, up, currentLine):
    lines = view.find_all('^commit')
    lineNos = [view.rowcol(l.a)[0] for l in lines]
    for index, lineNo in enumerate(lineNos):
        if lineNo > currentLine:
            if up:
                index = index - 2
            break
    else:
        index = -2 if up else 0
    gotoLine(view, lineNos[index], atTop=True)

class RemoteGitLogHelp(WindowCommand):
    def run(self):
        items = ['p (patch of this log)']
        self.window.show_quick_panel(items, lambda x: None)
