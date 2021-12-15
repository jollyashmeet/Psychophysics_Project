#adapted from demo scripts used in class

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
from os import listdir
from statistics import mean
from statsmodels.stats.anova import AnovaRM

#d' function
def dPrime(hitRate, FArate):
    stat = norm.ppf(hitRate) - norm.ppf(FArate)

    return stat

#criterion function
def criterion(hitRate, FArate):
    stat = -.5*(norm.ppf(hitRate) + norm.ppf(FArate))

    return stat

#Data fram for meanSDTs
meanSDTs = pd.DataFrame({"participant" : [], 'conditions' : [], 'hits': [], 'misses': [], 'FA': [], 'CR': [], 'dPrime':[],'crt':[]})


#import the raw data from the csv file
dataPath = "data_group/"
fileList = listdir(dataPath)

counter = 0 #initialize counter with 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)


    #create new data framw
    #import raw data from specified columns
    expData = pd.DataFrame(rawData, columns = ["cond", "correct_resp", "key_resp.keys", "key_resp.rt"])

    #rename specified columns
    expData = expData.rename(columns = {"cond" : "condition", "correct_resp" : "task",
                "key_resp.keys" : "resp", "key_resp.rt" : "RT"})


    #the data frame we'll be using
    accuracy = pd.DataFrame({"condition" : ["1", "2"], "hits" : [0,0], "misses" : [0,0],
                        "CRs" : [0,0], "FAs" : [0,0]})


    #updating the data frame for each entry
    for index, row in expData.iterrows():
        #condition: 1
        if row["condition"] == 1.0:
            rowInd = 0
            #Hit
            if row["task"] == "right" and row["resp"] == "right":
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["task"] == "right" and row['resp'] == "left":
                accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["task"] == "left" and row["resp"] == "left":
                accuracy.loc[rowInd,"CRs"] += 1
            #False alarm
            elif row["task"] == "left" and row["resp"] == "right":
                accuracy.loc[rowInd,"FAs"] += 1
    
        #condition: 2
        elif row["condition"] == 2.0:
            rowInd = 1
            #Hit
            if row["task"] == "right" and row["resp"] == "right":
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["task"] == "right" and row["resp"] == "left":
                accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["task"] == "left" and row["resp"] == "left":
                accuracy.loc[rowInd,"CRs"] += 1
            #False alarm
            elif row["task"] == "left" and row["resp"] == "right":
                accuracy.loc[rowInd,"FAs"] += 1
    
    #Calculate rates for each condition from response counts
    hitRate1 = accuracy.loc[0,"hits"]/15
    FArate1 = accuracy.loc[0,"FAs"]/15

    hitRate2 = accuracy.loc[1,"hits"]/15
    FArate2 = (accuracy.loc[1,"FAs"])/15

    
    #Data Lists
    pNumList = [pNum, pNum]
    condList = ["1", "2"]
    hitList = [accuracy.loc[0,"hits"],accuracy.loc[1,"hits"]]
    FAList = [accuracy.loc[0,'FAs'], accuracy.loc[1,'FAs']]
    missList = [accuracy.loc[0,'misses'],accuracy.loc[1,'misses']]
    CRList = [accuracy.loc[0,'CRs'],accuracy.loc[1,'CRs']]
    
    dPrimeList = [dPrime(hitRate1, FArate1), dPrime(hitRate2, FArate2)]
    criterionList = [criterion(hitRate1, FArate1),criterion(hitRate2, FArate2)]
    #new data --> data frame
    newLines = pd.DataFrame({'participant' : pNumList, 'conditions' : condList, 'hits': hitList, 'misses': missList, 'FA': FAList, 'CR': CRList, 'dPrime': dPrimeList,'crt': criterionList})
    #append newLines to meanSDTs
    meanSDTs = meanSDTs.append(newLines, ignore_index=True)

print(meanSDTs.to_string())

#average of dPrime and criterion for both conditions
print('The average d'' for both conditions:', mean(dPrimeList))
print('The average criterion for both conditions:', mean(criterionList))



#bargraph representing average of dPrime and criterion
fig, ax = plt.subplots()
bars = ax.bar([.5,1],[mean(dPrimeList),mean(criterionList)], width = .4)
ax.set_title('Average dPrime and Criterion')
ax.set_ylabel("Trials")
ax.set_xticklabels(["dPrime",'criterion'])
ax.set_xticks([.5,1])
plt.show()

# condition bargraph
cond_1 = [accuracy.loc[0,'hits'],accuracy.loc[0,'misses'],accuracy.loc[0,'CRs'],accuracy.loc[0,'FAs']] #condition 1 accuracy
cond_2 = [accuracy.loc[1,'hits'],accuracy.loc[1,'misses'],accuracy.loc[1,'CRs'],accuracy.loc[1,'FAs']] #condition 2 accuracy
xLabels = ['hits', 'misses','CRs','FAs']
x = np.arange(len(xLabels))
width = 0.35

fig, ax = plt.subplots()
bar1 = ax.bar(x-width/2,cond_1,width,label = '1.0')
bar2 = ax.bar(x+width/2,cond_2,width,label = '2.0')
ax.set_ylabel('Trials')
ax.set_title('Mean response by Duration of Stimuli for each condition')
ax.set_xticks(x)
ax.set_xticklabels(xLabels)
ax.legend((bar1, bar2), ('1.0','2.0'))
plt.show()

#repeated measures anova for d'
model = AnovaRM(data = meanSDTs, depvar = 'dPrime', subject = "participant", within = ['conditions']).fit()
print(model)
#repeated measures anova for criterion
model2 = AnovaRM(data = meanSDTs, depvar = 'crt', subject = "participant", within = ['conditions']).fit()
print(model2)
