# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 15:43:30 2016

@author: Patrick
"""
#csv is to manipulate csv files and Levenshtein is to calculate Levenshtein distances.
import csv
import random

#the list that will contain the test data.
testbox = []

#Opening the testdata. The path is absolute rather than relative. May have to change this.
testfile = open('C:\\Users\\Patrick\\Desktop\\Iamthinking\\Data\\test.csv', 'r')

#The reader.
testreader = csv.DictReader(testfile)

#Putting the testdata in the list.
for row in testreader:
    testbox.append((row['id'], row['product_uid'], row['search_term']))

#Closing the file
testfile.close

#The list the results will be in with the first line. Somehow needs editing in notepad.
results = [('id', 'relevance')]

#Did this so I could see the progress.
counter = 0

#This was necessary because otherwise it would go through the entire list from the beginning.
#Fortunately all the lists are ordered so we can use that to our advantage.
search_startpoint = 0

random.seed(4815162342)

for i in range(len(testbox)):
    found = False
    counter = counter + 1
    if counter % 1000 == 0:
        print counter / 166693.00

    relevance = random.randrange(1, 4)
        
    results.append((testbox[i][0], relevance))

#Writes the results in a csv file.    
with open('C:\\Users\\Patrick\\Desktop\\Iamthinking\\Data\\resultrandom.csv', 'wb') as result_file:
    finalwrite = csv.writer(result_file, delimiter=',')
    finalwrite.writerows(results)
    
    result_file.close