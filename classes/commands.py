from ..utils import sortTags

GIT_RESET = "git reset HEAD"
GIT_ADD = "git add"
GIT_ADD_ALL = "git add ."
GIT_RM = "git rm"
GIT_STATUS = "git status"
GIT_CHECKOUT = "git checkout --"
GIT_CHECKOUT_BRANCH = "git checkout"
GIT_CHECKOUT_NEW_BRANCH = "git checkout -b"
GIT_REMOVE_BRANCH = "git branch -d"
GIT_MERGE_BRANCH = "git merge"
GIT_REBASE_BRANCH = "git rebase"
GIT_COMMIT = "git commit -m"
GIT_DIFF = "git diff"
GIT_PUSH = "git push"
GIT_PULL = "git pull"
GIT_LIST_BRANCH = "git branch -l"
GIT_LOG = "git log --decorate=short --graph"
GIT_SHOW = "git show"
GIT_LIST_TAGS = "git tag -l -n"
GIT_TAG = "git tag"
GIT_REMOVE_TAG = "git tag -d"
GIT_GREP = "git grep"

functions = {
    GIT_LIST_TAGS: sortTags
}

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

    def asString(self):
        return ' '.join(self.asList())

    @classmethod
    def fromString(cls, string):
        splitted = string[1:-1].split('" "')
        command = splitted[0]
        value = None
        if len(splitted) == 2:
            value = splitted[1]
        splitted = command.split(' ', 2)
        gitcommand = splitted[0] + " " + splitted[1]
        command = cls(gitcommand, value=value)
        if len(splitted) == 3:
            for option in splitted[2].split():
                command.addOption(option)
        return command

    def parseResult(self, result):
        function = functions.get(self.command)
        if function is None:
            return result.strip()
        return '\n'.join(function(result.strip().split('\n')))