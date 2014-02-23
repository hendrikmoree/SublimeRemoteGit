from unittest import TestCase
from SublimeRemoteGit.commands import GitCommand, GIT_STATUS, GIT_PULL, GIT_LOG

class CommandsTest(TestCase):
    def testCommand(self):
        command = GitCommand(command=GIT_PULL)
        self.assertEquals(['"git pull"'], command.asList())
        self.assertEquals('"git pull"', command.asString())

    def testWithFilename(self):
        command = GitCommand(command=GIT_STATUS, value="a file")
        self.assertEquals(['"git status"', '"a file"'], command.asList())
        self.assertEquals('"git status" "a file"', command.asString())

    def testWithOption(self):
        command = GitCommand(command=GIT_LOG, value="a file")
        command.addOption('-p')
        self.assertEquals(['"git log -p"', '"a file"'], command.asList())
        self.assertEquals('"git log -p" "a file"', command.asString())

    def testCommandFromString(self):
        command = GitCommand.fromString('"git log"')
        self.assertEquals("git log", command.command)
        self.assertEquals([], command.options)
        self.assertEquals(None, command.value)

    def testCommandFromStringWithFilename(self):
        command = GitCommand.fromString('"git log" "a file"')
        self.assertEquals("git log", command.command)
        self.assertEquals([], command.options)
        self.assertEquals("a file", command.value)

    def testCommandFromStringWithOption(self):
        command = GitCommand.fromString('"git log -p" "a file"')
        self.assertEquals("git log", command.command)
        self.assertEquals(["-p"], command.options)
        self.assertEquals("a file", command.value)