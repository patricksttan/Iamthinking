# FILE: custom_chunker.py

# Natural Language Toolkit: code_classifier_chunker
# Based on code from
#   http://www.nltk.org/book/ch07.html#code-classifier-chunker
#
# Revisions:
# Not using megam; the feature builder is a constructor parameter;
# fixed bug of absent nltk.conlltags2tree
#
# Alexis Dimitriadis

import nltk
from nltk.chunk.util import conlltags2tree, tree2conlltags

algorithm = None
# In NLTK book example: algorithm='megam'


# If numpy is absent, the nltk fails with a very confusing error.
# We avoid problems by checking directly
try:
    import numpy
except ImportError:
    print "You need to download and install numpy!!!"
    raise


class ConsecutiveNPChunker(nltk.ChunkParserI):
    """
    Train a classifier on chunked data in Tree format.
    Arguments for the constructor:

    featuremap   The function that will compute features for each word
        in a sentence. See the NLTK book (and the assignment)
        for the arguments it must accept.

    train_sents  A list of sentences in chunked (Tree) format.
    """
    def __init__(self, featuremap, train_sents):
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = _ConsecutiveNPChunkTagger(featuremap, tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return conlltags2tree(conlltags)

    chunk = parse  # A synonym for the absent-minded


class _ConsecutiveNPChunkTagger(nltk.TaggerI):
    """This class is not meant to be
    used directly: Use ConsecutiveNPChunker instead."""

    def __init__(self, featuremap, train_sents):
        
        self._featuremap = featuremap
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = self._featuremap(untagged_sent, i, history) 
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = self._featuremap(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)
