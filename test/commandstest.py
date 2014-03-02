from unittest import TestCase
from SublimeRemoteGit.classes.commands import GitCommand, GIT_STATUS, GIT_PULL, GIT_LOG

class CommandsTest(TestCase):
    def testCommand(self):
        command = GitCommand(command=GIT_PULL)
        self.assertEqual(['"git pull"'], command.asList())
        self.assertEqual('"git pull"', command.asString())

    def testWithFilename(self):
        command = GitCommand(command=GIT_STATUS, value="a file")
        self.assertEqual(['"git status"', '"a file"'], command.asList())
        self.assertEqual('"git status" "a file"', command.asString())

    def testWithOption(self):
        command = GitCommand(command=GIT_LOG, value="a file")
        command.addOption('-p')
        self.assertEqual(['"git log -p"', '"a file"'], command.asList())
        self.assertEqual('"git log -p" "a file"', command.asString())

    def testCommandFromString(self):
        command = GitCommand.fromString('"git log"')
        self.assertEqual("git log", command.command)
        self.assertEqual([], command.options)
        self.assertEqual(None, command.value)

    def testCommandFromStringWithFilename(self):
        command = GitCommand.fromString('"git log" "a file"')
        self.assertEqual("git log", command.command)
        self.assertEqual([], command.options)
        self.assertEqual("a file", command.value)

    def testCommandFromStringWithOption(self):
        command = GitCommand.fromString('"git log -p" "a file"')
        self.assertEqual("git log", command.command)
        self.assertEqual(["-p"], command.options)
        self.assertEqual("a file", command.value)