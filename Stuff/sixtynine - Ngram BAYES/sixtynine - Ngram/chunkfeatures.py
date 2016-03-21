# Read in our names from a CSV file
from CNC import CharacterNgramChecker
import csv
from nltk.corpus import conll2002
corpus = conll2002 # Save us some typing with this alias

fp = open("namen.csv", "rb")
reader = csv.reader(fp)
rows = [ row for row in reader ]
fp.close()

for row in rows:
    row[0] = unicode(row[0], "utf-8")

namen = list(rows)

training = corpus.chunked_sents("ned.train")
NgramChecker = CharacterNgramChecker(4,training)
print "NgramChecker trained."

def chunkfeatures_1(sentence, i, history):
    """Simplest chunker features: Just the POS tag of the word"""
    word, pos = sentence[i]
    capital = "Dit is niets."
    if(i == 0):
        capital = "Begin zin"
        prevword, prevpos = "<START>","<START>"
        hist = "<START>"
    else:
        if word.istitle():
            capital = "Naam of land"
        prevword, prevpos = sentence[i-1]
        hist = history[i-1]

    if(i == len(sentence) - 1):
        nextword, nextpos = "<END>","<END>" 
    else:
        nextword, nextpos = sentence[i+1]

    if(word.istitle()):
        if(word in namen):
            isNaam = "Ja, ik denk het wel."
        else:
            isNaam = "Misschien is het een locatie!"
    else:
        isNaam = "Ik kan hier niks mee."
    
    caps = word.isupper()
    
    
    return {
            "Capital": capital,
            "CAPS": caps,
            "word": word,
            "nextword": nextword,
            "prevword": prevword,
            "Nextpos": nextpos,
            "prevpos+pos": "%s+%s" % (prevpos, pos),
            "Streepje": '-' in word,
            "History": hist,
            "isNaam": isNaam,
            "NGram": NgramChecker.check(word)
            }
