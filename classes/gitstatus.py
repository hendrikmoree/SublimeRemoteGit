
from ..commands import GIT_ADD, GIT_RESET, GIT_CHECKOUT

STAGED = [GIT_RESET]
CHANGED = [GIT_ADD, GIT_CHECKOUT]
UNTRACKED = [GIT_ADD]

class GitStatus(object):

    def __init__(self, staged, changed, untracked):
        self.staged = staged
        self.changed = changed
        self.untracked = untracked
        self._linenos = [n for n, _ in self.staged + self.changed + self.untracked]

    def fileAndCommandsForLine(self, lineno):
        for commands, lines in [(STAGED, self.staged), (CHANGED, self.changed), (UNTRACKED, self.untracked)]:
            for n, filename in lines:
                if lineno == n:
                    return filename, commands

    def firstlineno(self):
        return self._linenos[0]

    def nextlineno(self, currentLineNo, up=False):
        change = -1 if up else +1
        try:
            return self._linenos[self._linenos.index(currentLineNo) + change]
        except IndexError:
            return self._linenos[0]
        except ValueError:
            return self._closestLineNo(currentLineNo)

    def _closestLineNo(self, currentLineNo):
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
            elif line == "# Changes not staged for commit:":
                appendTo = changed
            elif line == "# Untracked files:":
                appendTo = untracked
            if line.startswith("#   ") and not line.startswith("#   ("):
                filename = line[4:].split(":   ", 1)[-1]
                appendTo.append((lineno, filename))
        return cls(staged, changed, untracked)