
from unittest import TestCase
from SublimeRemoteGit.classes.gitstatus import GitStatus


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
#   new file:   test/alltest.sh
#
# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#
#   test/alltest.py
""")
        self.assertEqual([(4, "setup.py")], gitStatus.staged)
        self.assertEqual([(10, "setup.py"), (11, "test/alltest.sh")], gitStatus.changed)
        self.assertEqual([(16, "test/alltest.py")], gitStatus.untracked)

        filename, commands = gitStatus.fileAndCommandsForLine(4)
        self.assertEqual("setup.py", filename)
        filename, commands = gitStatus.fileAndCommandsForLine(10)
        self.assertEqual("setup.py", filename)
        filename, commands = gitStatus.fileAndCommandsForLine(11)
        self.assertEqual("test/alltest.sh", filename)
        filename, commands = gitStatus.fileAndCommandsForLine(16)
        self.assertEqual("test/alltest.py", filename)
        self.assertEqual(None, gitStatus.fileAndCommandsForLine(12))

        self.assertEqual(4, gitStatus.firstlineno())
        self.assertEqual(10, gitStatus.nextlineno(4))
        self.assertEqual(11, gitStatus.nextlineno(10))
        self.assertEqual(16, gitStatus.nextlineno(11))
        self.assertEqual(4, gitStatus.nextlineno(16))

        self.assertEqual(11, gitStatus.nextlineno(16, True))
        self.assertEqual(10, gitStatus.nextlineno(11, True))
        self.assertEqual(4, gitStatus.nextlineno(10, True))
        self.assertEqual(16, gitStatus.nextlineno(4, True))
        self.assertEqual(4, gitStatus.nextlineno(0, True))
        self.assertEqual(4, gitStatus.nextlineno(1, True))
        self.assertEqual(10, gitStatus.nextlineno(8, True))
