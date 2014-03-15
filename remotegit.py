from .utils import projectRoot, lastCommand
from .sublime_utils import createView, replaceView
from sublime_plugin import TextCommand, WindowCommand
from .constants import VIEW_PREFIX
from os import listdir
from os.path import join, isdir, basename
from re import compile as regexCompile

class RemoteGitSetRootDir(TextCommand):
    def run(self, edit, rootDir):
        self.view.rootDir = rootDir
        self.view.run_command("remote_git_st")

class RemoteGit(WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view.name().startswith(VIEW_PREFIX):
            view = createView(view.window())
        items = [basename(projectRoot(view))]
        depsdDir = join(projectRoot(view), 'deps.d')
        if not isdir(depsdDir):
            self._changeDir(items[0], view)
            return
        for f in listdir(depsdDir):
            items.append(f)
        if len(items) == 1:
            self._changeDir(items[0], view)
            return
        self.window.show_quick_panel(items, lambda x: self._changeDir(items[x], view) if x != -1 else None)

    def _changeDir(self, name, view):
        rootDir = projectRoot(view)
        if name == basename(rootDir):
            directory = rootDir
        else:
            directory = join(rootDir, 'deps.d', name)
        view.run_command('remote_git_set_root_dir', args=dict(rootDir=directory))

class ReplaceViewContent(TextCommand):
    def run(self, edit, content, **arguments):
        name = arguments.get('name', VIEW_PREFIX)
        replaceView(self.view, edit, content, name=name)

p = regexCompile('([A-Z])')
class RemoteGitBack(TextCommand):
    def run(self, edit):
        command, args = lastCommand(2)
        command = p.sub(r'_\1', command)[1:].lower()
        self.view.run_command(command, args=args)
