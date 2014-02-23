from .utils import remoteCommand
from sublime_plugin import TextCommand
from .commands import GitCommand, GIT_CHECKOUT_BRANCH, GIT_CHECKOUT_NEW_BRANCH, GIT_MERGE_BRANCH, GIT_LIST_BRANCH, GIT_REMOVE_BRANCH

class _RemoteGitBranchCommand(TextCommand):
    def run(self, edit):
        if self.choose:
            branches = [b.strip() for b in remoteCommand(self.view, GitCommand(GIT_LIST_BRANCH)).strip().split('\n') if not b.startswith('*')]
            self.view.window().show_quick_panel(branches, lambda x: self.checkout(branches[x]) if x != -1 else None)
        else:
            self.view.window().show_input_panel("Branch name: ", "", self.checkout, None, None)

    def checkout(self, name):
        remoteCommand(self.view, GitCommand(self.command, name))
        self.view.run_command("remote_git_st")

class RemoteGitCheckoutBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_BRANCH
    choose = True

class RemoteGitCheckoutNewBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_NEW_BRANCH
    choose = False

class RemoteGitMergeBranch(_RemoteGitBranchCommand):
    command = GIT_MERGE_BRANCH
    choose = True

class RemoteGitRemoveBranch(_RemoteGitBranchCommand):
    command = GIT_REMOVE_BRANCH
    choose = True
