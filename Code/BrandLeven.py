# -*- coding: utf-8 -*-
"""
~Blame Marc if code is crappy~
Input: attributes.csv, product_descriptions.csv, test.csv
Output: (corrected) Levenstein Distance for brand.
"""

#import stuff
import pandas as panda
import time
import pickle
import Levenshtein

#initializing variables
t0 = time.clock()
datadir = "../Data/"

#loading files
products = pickle.load( open( "products.p", "rb" ) )
training = panda.read_csv(datadir+"train_small.csv")

brand = products[training["product_uid"][12]]["MFG Brand Name"] 
search_term = training["search_term"][12]

print search_term
print brand
print Levenshtein.distance(search_term, brand) - (len(search_term) - len(brand))