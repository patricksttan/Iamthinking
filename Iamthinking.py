# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 15:43:30 2016

@author: Patrick
"""
#csv is to manipulate csv files and Levenshtein is to calculate Levenshtein distances.
import csv
import Levenshtein

#Where we will store the pertinent info from the traindata for now.
toolbox = []

#Opening the traindata
trainfile = open('C:\\Users\\Patrick\\Desktop\\Iamthinking\\Data\\train.csv', 'r')

#The reader that will access the file.
trainreader = csv.DictReader(trainfile)

#puts the pertinent training data in a list. In this case only 3 features were used.
for row in trainreader:
    toolbox.append((row['product_uid'], row['search_term'], row['relevance']))

#closes the file
trainfile.close

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

#Loops through the testdata. If it finds a match it will calculate the Levenshtein distance
#After it has found a match it will try the next training data point untill a match is not found.
#Then the loop will be broken and it will carry on with the next test datapoint.
#Also, it will change the search_startpoint. The result will be put in the result list.
#The values are not rounded. I did that manually in an editor.
for i in range(len(testbox)):
    found = False
    counter = counter + 1
    if counter % 1000 == 0:
        print counter / 166693.00
    distance = 1000
    relevance = 1
    for j in range(search_startpoint, len(toolbox)):
        if testbox[i][1] == toolbox[j][0]:
            found = True
            search_startpoint = j
            if Levenshtein.distance(testbox[i][2], toolbox[j][1]) < distance:
                distance = Levenshtein.distance(testbox[i][2], toolbox[j][1])
                relevance = toolbox[j][2]
        elif testbox[i][1] != toolbox[j][0] and found == True:
            break
        
    results.append((testbox[i][0], relevance))

#Writes the results in a csv file.    
with open('C:\\Users\\Patrick\\Desktop\\Iamthinking\\Data\\result.csv', 'wb') as result_file:
    finalwrite = csv.writer(result_file, delimiter=',')
    finalwrite.writerows(results)
    
    result_file.close