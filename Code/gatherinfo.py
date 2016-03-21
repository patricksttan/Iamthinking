# -*- coding: utf-8 -*-
"""
~Blame Marc if code is crappy~
Input: attribues.csv, product_descriptions.csv
Output: dictionary with {Productuid: {Informationthings:theirvalues}}
"""

#import stuff
import pandas as panda
import time
import pickle

#initialize variables
t0 = time.clock()
datadir = "../Data/"
product = {}

attributes = panda.read_csv(datadir+"attributes.csv")
product_descriptions = panda.read_csv(datadir + 'product_descriptions.csv')

attributes.to_pickle('attributes.pkl')
product_descriptions.to_pickle('product_descriptions.pkl')

#basically convert product_descriptions to a dictionary.
for index, row in product_descriptions.iterrows():
    product[row['product_uid']] = {'Description':row['product_description']}
        
#add the information from attributes to the dictionary of products.
for index, row in attributes.iterrows():
    if not row['product_uid'] in product:
        print index
        print row
    else:
    product[row['product_uid']][row['name']] = row['value']    

print product

t1 = time.clock()
print t1 - t0

#uncomment to save.
#attributes.to_pickle('attributes.pkl')
#product_descriptions.to_pickle('product_descriptions.pkl')
pickle.dump(product,open('products.p','wb'))
