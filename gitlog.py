from .utils import findFilenameAndCommands, remoteCommand, gotoLine, currentLineNo, replaceView, logCommand, projectRoot
from sublime_plugin import WindowCommand, TextCommand
from .constants import LOG_VIEW_NAME
from .classes.commands import GitCommand, GIT_LOG, GIT_SHOW

class RemoteGitLog(TextCommand):
    def run(self, edit, **kwargs):
        args = kwargs
        view = self.view
        filename, commands = findFilenameAndCommands(view)
        if 'filename' in kwargs:
            filename = kwargs['filename']
        elif filename is None:
            filename = view.file_name()
        if filename:
            args['filename'] = filename
            if 'deps.d' in filename:
                root, depsd = filename.rsplit('deps.d', 1)
                view.rootDir = "%sdeps.d/%s" % (root, depsd.split('/')[1])
            else:
                view.rootDir = projectRoot(view)
            if view.rootDir in filename:
                filename = filename.split(view.rootDir)[1][1:]
        logCommand("remote_git_log", args)
        command = GitCommand(GIT_LOG, filename)
        if kwargs.get('patch') == True:
            command.addOption('-p')
        result = remoteCommand(view, command)
        view.run_command("replace_view_content", args=dict(content=result, name=LOG_VIEW_NAME))
        gotoLine(view, getattr(view, "lastloglineno", 0), atTop=True)

class RemoteGitShowCommit(TextCommand):
    def run(self, edit):
        logCommand("remote_git_show_commit")
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

def gotoNextCommit(view, up, currentLine):
    lines = view.find_all('^commit')
    if len(lines) <= 1:
        return
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
