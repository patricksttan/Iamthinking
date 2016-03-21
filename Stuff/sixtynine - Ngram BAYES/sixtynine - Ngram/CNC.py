##Character N-gram checker.

from collections import defaultdict
from nltk.chunk.util import conlltags2tree, tree2conlltags

class CharacterNgramChecker(object):
    def __init__(self, depth, train_sents):
        global maxDepth
        maxDepth = depth
        self.dicTree = DefDict(1)
        for s in train_sents:
            for (w,p,c) in tree2conlltags(s):
                if c == "O":
                    self.train(w)

    def train(self,w):
        w = "^"+w+"$"
        while w != "":
            self.dicTree.add(w[:maxDepth])
            w = w[1:]

    def check(self,w):
        w = "^"+w+"$"
        record = maxDepth+1
        while w != "":
            check = self.dicTree.check(w[:maxDepth])
            if check < record:
                record = check
            w = w[1:]
        return record

class DefDict(object):
    
    def __init__(self, depth):
        self.dic = defaultdict(lambda: End(depth))
        self.dic[""] = End(maxDepth+1)
        self.depth = depth
        
    def add(self,substring):
        char = substring[:1]
        if not self.dic[char].add(substring[1:]):
            if char != "":
                if self.depth != maxDepth:
                    self.dic[char] = DefDict(self.depth+1)
                    self.dic[char].add(substring)
        return True

    def check(self, substring):
        return self.dic[substring[:1]].check(substring[1:])

class End(object):
    def __init__(self, depth):
        self.depth = depth
    def check(self,substring):
        return self.depth
    def add(self,substring):
        return False
