from .utils import remoteCommand
from sublime_plugin import TextCommand
from .commands import GitCommand, GIT_CHECKOUT_BRANCH, GIT_CHECKOUT_NEW_BRANCH, GIT_MERGE_BRANCH, GIT_LIST_BRANCH, GIT_REMOVE_BRANCH, GIT_LIST_TAGS

class _RemoteGitBranchCommand(TextCommand):
    choose = True
    show = False

    def run(self, edit):
        if self.choose or self.show:
            branches = [
                b.strip() for b in
                remoteCommand(self.view, GitCommand(self.listcommand)).strip().split('\n')
                if self.show or (self.choose and not b.startswith('*'))
            ]
            self.view.window().show_quick_panel(branches, lambda x: self.checkout(branches[x]) if x != -1 and self.choose else None)
        else:
            self.view.window().show_input_panel("Branch name: ", "", self.checkout, None, None)

    def checkout(self, name):
        remoteCommand(self.view, GitCommand(self.command, name))
        self.view.run_command("remote_git_st")

class RemoteGitCheckoutBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_BRANCH
    listcommand = GIT_LIST_BRANCH

class RemoteGitCheckoutNewBranch(_RemoteGitBranchCommand):
    command = GIT_CHECKOUT_NEW_BRANCH
    choose = False

class RemoteGitMergeBranch(_RemoteGitBranchCommand):
    command = GIT_MERGE_BRANCH
    listcommand = GIT_LIST_BRANCH

class RemoteGitRemoveBranch(_RemoteGitBranchCommand):
    command = GIT_REMOVE_BRANCH
    listcommand = GIT_LIST_BRANCH

class RemoteGitListBranch(_RemoteGitBranchCommand):
    listcommand = GIT_LIST_BRANCH
    show = True
    choose = False

class RemoteGitListTags(_RemoteGitBranchCommand):
    listcommand = GIT_LIST_TAGS
    show = True
    choose = False
