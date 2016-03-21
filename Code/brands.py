# -*- coding: utf-8 -*-
"""
~Blame Marc if code is crappy~
Input: attributes.csv
Output: dictionary with {'Brand Name': [list of product_uids]}
"""
#importing stuff.
import pandas as panda
import time
import pickle

#initializing variables
t0 = time.clock()
datadir = "../Data/"
brands = {}

#loading attributes.
print "Loading attributes.csv"
attributes = panda.read_csv(datadir+"attributes.csv")

#iterate over all entries in attributes
#if the attribute is brand name and the Brand Name is in the dictionary, append the produt.
#If the Brand Name is not in the dictionary, start a new entry.
for index, row in attributes.iterrows():
    if(row['name'] == 'MFG Brand Name'):
       if(row['value'] in brands):
           brands[row['value']].append(row['product_uid'])
       else:
           brands[row['value']] = [row['product_uid']]

t1 = time.clock()

print brands
print t1 - t0

#uncomment to save.
#pickle.dump(brands,open('brands.p','wb'))
