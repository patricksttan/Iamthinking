# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\Patrick\.spyder2\.temp.py
"""

import csv
import Levenshtein

toolbox = []

class TrainTool(object):
    search_term_relevance_list = []     

    def __init__(self, product_uid, search_term, relevance):
        self.product_uid = product_uid
        self.add_search_term_relevance(search_term, relevance, self.search_term_relevance_list)
        
    def add_search_term_relevance(self, search_term, relevance, search_term_relevance_list):
        exec("s" + str(len(search_term_relevance_list)) + " = search_term_relevance('" + search_term + "'," + str(relevance) + ")")
        

    def check_search_terms(self, search_term):
        global search_term_relevance_list        
        distance = 1000
        relevance = 1
        for terms in search_term_relevance_list:
            if Levenshtein.distance(search_term, terms.search_term) < distance:
                distance = Levenshtein.distance(search_term, terms.search_term)
                relevance = terms.relevance
        
        return relevance

class search_term_relevance(object):
    def __init__(self, search_term, relevance):
        self.search_term = search_term
        self.relevance = relevance

            
trainfile = open('C:\\Users\\Patrick\\Desktop\\Iamthinking\\Data\\train.csv', 'r')

trainreader = csv.DictReader(trainfile)

for row in trainreader:
    target = 't' + str(row['product_uid'])
    term = row['search_term'].translate(None, "'")
    
    if target in toolbox:
        exec(str(target) + ".add_search_term_relevance(" + "'" + term + "'" + ", " + str(row['relevance']) + ", " + str(target) + ".search_term_relevance_list" +")")
    else:
        exec(str(target) + " = TrainTool(" + row['product_uid'] + ", " + "'" + term + "'" + ", " + row['relevance'] + ")")
        toolbox.append(str(target))

trainfile.close

testfile = open('C:\\Users\\Patrick\\Desktop\\Iamthinking\\Data\\test.csv', 'r')

testreader = csv.DictReader(testfile)

resultslist = [['id', '"relevance"']]

for row in testreader:
    target = 't' + str(row['product_uid'])
    term = row['search_term'].translate(None, "'")
    if target in toolbox:
        relevance = target.check_search_terms(row['search_term'])
        resultslist.append([row['id'], relevance])
    else:
        resultslist.append([row['id'], 1])

testfile.close
"""        
with open('test.csv', 'wb') as ding:
    dong = csv.writer(ding, delimiter=',')
    dong.writerows(testlist)
"""