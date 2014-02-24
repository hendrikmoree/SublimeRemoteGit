
from unittest import TestCase
from SublimeRemoteGit.classes.gitstatus import GitStatus, DEFAULT_COMMANDS
from SublimeRemoteGit.commands import GIT_RESET, GIT_ADD, GIT_CHECKOUT, GIT_DIFF, GIT_RM

class GitStatusTest(TestCase):

    def testParseMessage(self):
        gitStatus = GitStatus.fromMessage(message="""# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#   modified:   setup.py
#
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#   modified:   setup.py
#   deleted:    testsetup.py
#   new file:   test/alltest.sh
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#   test/alltest.py
""")
        self.assertEqual([(4, "setup.py", "modified")], gitStatus.staged)
        self.assertEqual([(10, "setup.py", "modified"), (11, "testsetup.py", "deleted"), (12, "test/alltest.sh", "modified")], gitStatus.changed)
        self.assertEqual([(17, "test/alltest.py", "modified")], gitStatus.untracked)

        filename, commands = gitStatus.fileAndCommandsForLine(4)
        self.assertEqual("setup.py", filename)
        self.assertEqual([GIT_RESET] + DEFAULT_COMMANDS, commands)
        filename, commands = gitStatus.fileAndCommandsForLine(10)
        self.assertEqual("setup.py", filename)
        self.assertEqual([GIT_CHECKOUT, GIT_DIFF, GIT_ADD] + DEFAULT_COMMANDS, commands)
        filename, commands = gitStatus.fileAndCommandsForLine(11)
        self.assertEqual("testsetup.py", filename)
        self.assertEqual([GIT_CHECKOUT, GIT_DIFF, GIT_RM] + DEFAULT_COMMANDS, commands)
        filename, commands = gitStatus.fileAndCommandsForLine(12)
        self.assertEqual("test/alltest.sh", filename)
        self.assertEqual([GIT_CHECKOUT, GIT_DIFF, GIT_ADD] + DEFAULT_COMMANDS, commands)
        filename, commands = gitStatus.fileAndCommandsForLine(17)
        self.assertEqual("test/alltest.py", filename)
        self.assertEqual([GIT_ADD] + DEFAULT_COMMANDS, commands)
        filename, commands = gitStatus.fileAndCommandsForLine(13)
        self.assertEqual(None, filename)
        self.assertEqual(DEFAULT_COMMANDS, commands)

        self.assertEqual(4, gitStatus.firstlineno())
        self.assertEqual(10, gitStatus.nextlineno(4))
        self.assertEqual(11, gitStatus.nextlineno(10))
        self.assertEqual(12, gitStatus.nextlineno(11))
        self.assertEqual(17, gitStatus.nextlineno(12))
        self.assertEqual(4, gitStatus.nextlineno(17))

        self.assertEqual(12, gitStatus.nextlineno(17, True))
        self.assertEqual(11, gitStatus.nextlineno(12, True))
        self.assertEqual(10, gitStatus.nextlineno(11, True))
        self.assertEqual(4, gitStatus.nextlineno(10, True))
        self.assertEqual(17, gitStatus.nextlineno(4, True))
        self.assertEqual(4, gitStatus.nextlineno(0, True))
        self.assertEqual(4, gitStatus.nextlineno(1, True))
        self.assertEqual(10, gitStatus.nextlineno(8, True))

    def testParseAllClean(self):
        gitStatus = GitStatus.fromMessage("""# On branch master
nothing to commit, working directory clean""")
        self.assertEquals([], gitStatus.staged)
        self.assertEquals([], gitStatus.changed)
        self.assertEquals([], gitStatus.untracked)
        self.assertEquals(None, gitStatus.firstlineno())