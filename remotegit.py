from .utils import projectRoot, createView, replaceView
from sublime_plugin import TextCommand, WindowCommand
from .constants import VIEW_PREFIX
from os import listdir
from os.path import join, isdir, basename

class RemoteGit(TextCommand):
    def run(self, edit):
        view = self.view
        if not view.name().startswith(VIEW_PREFIX):
            view = createView(self.view.window())
        view.run_command('remote_git_set_root_dir', args=dict(rootDir=projectRoot(self.view)))

class RemoteGitSetRootDir(TextCommand):
    def run(self, edit, rootDir):
        self.view.rootDir = rootDir
        self.view.run_command("remote_git_st")

class RemoteGitChooseRootDir(WindowCommand):
    def run(self):
        view = self.window.active_view()
        items = [basename(projectRoot(view))]
        depsdDir = join(projectRoot(view), 'deps.d')
        if not isdir(depsdDir):
            return
        for f in listdir(depsdDir):
            items.append(f)
        self.window.show_quick_panel(items, lambda x: self._changeDir(items[x], view))

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
