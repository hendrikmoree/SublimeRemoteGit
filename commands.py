GIT_RESET = "git reset HEAD"
GIT_ADD = "git add"
GIT_RM = "git rm"
GIT_STATUS = "git status"
GIT_CHECKOUT = "git checkout --"
GIT_CHECKOUT_BRANCH = "git checkout"
GIT_CHECKOUT_NEW_BRANCH = "git checkout -b"
GIT_MERGE_BRANCH = "git merge"
GIT_COMMIT = "git commit -m"
GIT_DIFF = "git diff"
GIT_PUSH = "git push"
GIT_PULL = "git pull"
GIT_LIST_BRANCH = "git branch -l"
GIT_LOG = "git log"

class GitCommand(object):
    def __init__(self, command, value=None):
        self.command = command
        self.value = value
        self.options = []

    def addOption(self, option):
        self.options.append(option)

    def asList(self):
        args = ['"%s"' % ' '.join([self.command] + self.options)]
        if self.value:
            args.append('"%s"' % self.value)
        return args