from unittest import TestCase

from SublimeRemoteGit.utils import sortTags

class UtilsTest(TestCase):

    def testSortTags(self):
        tags = ['0.1  Tag 1', '0.10 Tag 10', '0.2  Tag 2']
        self.assertEquals(['0.10 Tag 10', '0.2  Tag 2', '0.1  Tag 1'], sortTags(tags))
