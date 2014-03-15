from unittest import TestCase
from SublimeRemoteGit.classes.commands import GitCommand, GIT_STATUS, GIT_PULL, GIT_LOG, GIT_LIST_TAGS

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
        self.assertEqual(['"git log --decorate=short --graph -p"', '"a file"'], command.asList())
        self.assertEqual('"git log --decorate=short --graph -p" "a file"', command.asString())

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

    def testParseResult(self):
        command = GitCommand(command=GIT_LOG)
        result = command.parseResult("a result")
        self.assertEqual("a result", result)

    def testSortListTags(self):
        command = GitCommand(command=GIT_LIST_TAGS)
        result = command.parseResult("0.1 Tag 1\n0.2 Tag 2")
        self.assertEqual("0.2 Tag 2\n0.1 Tag 1", result)