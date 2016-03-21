from nltk.corpus import conll2002 
from custom_chunker import ConsecutiveNPChunker
from nltk.chunk.util import conlltags2tree, tree2conlltags
from nltk import Tree  # Import the type so we can check for it
import chunkfeatures
from chunkfeatures import chunkfeatures_1
corpus = conll2002 # Save us some typing with this alias
import cPickle as pickle
import time
import winsound
now = time.time()
print (time.strftime("%d/%m/%Y %H:%M:%S") + ": started")
training = corpus.chunked_sents("ned.train")
simple_nl_NER = ConsecutiveNPChunker(chunkfeatures_1, training)
pickle.dump(simple_nl_NER,open('best.pickle','w'))
print (time.strftime("%d/%m/$Y %H:%M:%S") + ": done")