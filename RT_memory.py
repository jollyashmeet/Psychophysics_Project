#adapted from demo scripts used in class

from statsmodels.stats.anova import AnovaRM
import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean
from os import listdir

##import raw data
dataPath = "data_group/"
fileList = listdir(dataPath)

#data frame for mean RTs
meanRTs = pd.DataFrame({"participant" : [], "meanRT" : [], 'conditions' : []})

counter = 0 #initialize counter with 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)
    
    #create new data frame
    #import raw data from specified columns
    expData = pd.DataFrame(rawData, columns = ['cond','correct_resp',"key_resp.rt", "key_resp.keys"])
    #rename specified columns 
    expData = expData.rename(columns = {"key_resp.rt" : "RT", "key_resp.keys" : "response"})

    #only include trials with a response
    expData = expData[expData.RT.notnull()]

    #only include trials with correct test responses for RT analysis
    rtData = expData[((expData.correct_resp == "right") & (expData.response == "right")) | ((expData.correct_resp == "left") & (expData.response == "left"))] #attributions and rejections

    print(rtData.to_string())

    #data frame for RTs for each condition
    cond1RTs = rtData[(rtData.cond == 1.0)].RT


    cond2RTs = rtData[(rtData.cond == 2.0)].RT
    


    #Data Lists
    pNumList = [pNum, pNum]
    condList = ["1", "2"]
    RTList = [mean(cond1RTs), mean(cond2RTs)]


    #new data --> data frame
    newLines = pd.DataFrame({"participant" : pNumList, "meanRT" : RTList,'conditions': condList})

    #append newLines to meanRTs
    meanRTs = meanRTs.append(newLines, ignore_index=True) #don't want index duplicates

print(meanRTs.to_string())

#group means for each condition
cond1Means = meanRTs[(meanRTs.conditions == '1')]["meanRT"]
cond2Means = meanRTs[(meanRTs.conditions == '2')]["meanRT"]

print('The mean RT for condition 1:', mean(cond1Means))
print('The mean RT for condition 2:', mean(cond2Means))

# #vizualizing with a boxplot


fig, ax = plt.subplots()

box = ax.boxplot([cond1Means, cond2Means])
ax.set_title('Mean Reaction Time by Duration of Stimuli')
ax.set_ylabel("RT (s)")
ax.set_xticklabels(["1.0 (0.5s)","2.0 (1.0s)"])

plt.show()


#repeated measures anova
model = AnovaRM(data = meanRTs, depvar = "meanRT", subject = "participant", within = ['conditions']).fit()
print(model)

