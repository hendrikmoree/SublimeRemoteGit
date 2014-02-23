
from copy import copy
from ..commands import GIT_ADD, GIT_RESET, GIT_CHECKOUT, GIT_DIFF, GIT_PUSH, GIT_RM, GIT_PULL, GIT_LOG

STAGED = [GIT_RESET]
CHANGED = [GIT_CHECKOUT, GIT_DIFF]
UNTRACKED = [GIT_ADD]
DEFAULT_COMMANDS = [GIT_PUSH, GIT_PULL, GIT_LOG]

class GitStatus(object):

    def __init__(self, staged, changed, untracked):
        self.staged = staged
        self.changed = changed
        self.untracked = untracked
        self._linenos = [n for n, _, _ in self.staged + self.changed + self.untracked]

    def fileAndCommandsForLine(self, lineno):
        for commands, lines in [(STAGED, self.staged), (CHANGED, self.changed), (UNTRACKED, self.untracked)]:
            for n, filename, status in lines:
                if lineno == n:
                    retCommands = copy(commands)
                    if commands == CHANGED:
                        if status == 'modified':
                            retCommands.append(GIT_ADD)
                        else:
                            retCommands.append(GIT_RM)
                    return filename, retCommands + DEFAULT_COMMANDS
        return None, DEFAULT_COMMANDS

    def firstlineno(self):
        return self._linenos[0]

    def nextlineno(self, currentLineNo, up=False):
        change = -1 if up else +1
        try:
            return self._linenos[self._linenos.index(currentLineNo) + change]
        except IndexError:
            return self._linenos[0]
        except ValueError:
            return self.closestLineNo(currentLineNo)

    def closestLineNo(self, currentLineNo):
        return min(self._linenos, key=lambda x: abs(x - currentLineNo))

    @classmethod
    def fromMessage(cls, message):
        staged = []
        changed = []
        untracked = []
        appendTo = None
        for lineno, line in enumerate(message.split("\n")):
            if line == "# Changes to be committed:":
                appendTo = staged
            elif line == "# Changes not staged for commit:" or line == "# Changed but not updated:":
                appendTo = changed
            elif line == "# Untracked files:":
                appendTo = untracked
            if line.startswith("#   ") and not line.startswith("#   ("):
                filename = line[4:].split(":   ", 1)[-1].strip()
                status = "deleted" if "deleted:" in line else "modified"
                appendTo.append((lineno, filename, status))
        return cls(staged, changed, untracked)