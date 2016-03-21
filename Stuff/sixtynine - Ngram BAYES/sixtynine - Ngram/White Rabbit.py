from nltk.corpus import conll2002 
from custom_chunker import ConsecutiveNPChunker
from nltk.chunk.util import conlltags2tree, tree2conlltags
from nltk import Tree  # Import the type so we can check for it
from chunkfeatures import chunkfeatures_1
corpus = conll2002 # Save us some typing with this alias
import cPickle as pickle
testing = corpus.chunked_sents("ned.testa")
import winsound

simple_nl_NER = pickle.load(open('best.pickle','r'))
print simple_nl_NER.evaluate(testing)
winsound.Beep(220,250)
winsound.Beep(440,250)
winsound.Beep(880,250)
