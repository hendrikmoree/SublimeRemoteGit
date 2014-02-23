from unittest import TestCase
from SublimeRemoteGit.commands import GitCommand, GIT_STATUS, GIT_PULL, GIT_LOG

class CommandsTest(TestCase):
    def testCommand(self):
        command = GitCommand(command=GIT_PULL)
        self.assertEquals(['"%s"' % GIT_PULL], command.asList())

    def testWithFilename(self):
        command = GitCommand(command=GIT_STATUS, value="a file")
        self.assertEquals(['"%s"' % GIT_STATUS, '"a file"'], command.asList())

    def testWithOption(self):
        command = GitCommand(command=GIT_LOG, value="a file")
        command.addOption('-p')
        self.assertEquals(['"%s -p"' % GIT_LOG, '"a file"'], command.asList())
