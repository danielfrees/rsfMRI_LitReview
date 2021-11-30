import pandas as pd
import csv
import re

#list of words used for decrease, increase, etc. 
decList = ["DECREASE", 'decrease', 'Decrease', 'Dec', 'dec', 'hypo', 'Hypo', 'HYPO', 'Reduce', 'reduce']
incList = ["INCREASE", 'increase', 'Increase', 'Inc', 'inc', 'hyper', 'Hyper', 'HYPER']
nullList = ["NULL", "NO", "No", "no", 'null', 'Null', 'No diff', 'no diff', 'No Diff', 'No sig', 'no sig', 'No Sig', 'NO SIG']
resultWords = decList + incList + nullList


#severity words
mildTerms = ["MILD", "mild", "Mild"]
modTerms = ["MOD", "mod", "Mod"]
sevTerms = ["SEV", "sev", "Sev"]
mixTerms = ["MIX", "mix", "Mix", "all", "All", "ALL"]

#age words
adultList = ["ADULT", "adult", 'Adult']
adolescentList = ["ADOL", "adolescent", "Adolescent"]
childList = ["CHILD, ""child", "Child"]
mixList = ["MIX", "mix", "Mix"]

#chronicity words
acuteList = ["ACUTE", "acute", "Acute"]
subacuteList = ["SUBACUTE", "subacute", "Subacute"]
chronicList = ["CHRONIC", "chronic", "Chronic"]
mixedList = ["MIX", "mix", "Mix"]
repSubList = ["REP", "SUBCON", "repetitive", "Repetitive", "subconcussive", "Subconcussive"]

#control words
healthyList = ["HC", "healthy", "Healthy", "HEALTHY"]
inSportList = ["ISC", "In-sport", "in-sport", "IN-SPORT", "IN SPORT"]
nonContactList = ["NCC", "Non-contact", "non-contact", "NON-CONTACT", "non-contact", "Non-Contact", "NON CONTACT"]
tbiPlusMoodList = ["TBI+", "tbi+", "Tbi+", "TBI plus", "tbi plus", "Tbi plus", "tbi +", "Tbi +", "TBI PLUS"]
moodList = ["mood", "Mood", "anxiety", "Anxiety", "MOOD", "ANXIETY"]
otherList =  ["other", "Other", "Orthopedic", "orthopedic", "military", "Military", "OTHER", "ORTHO", "MILIT"]
    

#cleanData function ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
#cleanData(datalist): cleanData() takes in a list of pandas dataframes (these are generated in my code shortly below the directory inputs), and outputs 
#clean dataframes for the columns relevant to our analysis. I used natural language processing (NLP) to determine what our final verdict for 
#each result/classification was, and then edited the output list of dataframes accordingly.
#Rules: the final determined Result must be written leftmost in its cell so the correct keyword can be identified. 
#Results and Chronicities must be listed for each finding, but other classifications will autofill down wherever they 
#have not been filled in (as we typically only wrote these out for the first finding of a given paper). Certain mispellings 
#and miscapitalizations are allowed, but I did not write a full Trie or other spellchecker, so try to avoid typos as much as possible. 
#I made sure through multiple iterations that this was catching all of our most common mispellings/ miscaps.
def cleanData(datalist):
    for i in range(len(datalist)):
        datalist[i] = datalist[i].fillna('')
    
    for i in range(len(datalist)):
        for index, row in datalist[i].iterrows():
            #CLEAN RESULTS SECTION
            #NOTE: First occurence is counted, because that was how we reported our main findings (always came first). Sometimes the other key words will appear describing a finding which 
            #did not survive due to ANCOVA etc. 
            
            #strip all leading and ending whitespace for the columns to be cleaned (important so that I can check for empty cases vs. error cases). Could've also used isspace() instead but this was better
            row['RESULT'].strip()
            row['TBI Class'].strip()
            row['Severity'].strip()
            row['Age'].strip()
            row['Chronicity'].strip()
            row['Control Type'].strip()   
            
            keyPositions = ((row['RESULT'].find(resWord), resWord) for resWord in resultWords)
            keyPositions = [key for key in keyPositions if key[0] != -1]  #don't want to consider keywords which didn't show up (pos -1)
            try:
                leftmost = min(keyPositions, key = lambda t: t[1]) #anonymous func! yay!
                if leftmost[1] in decList:
                    datalist[i].at[index, 'RESULT'] = "dec"
                elif leftmost[1] in incList:
                    datalist[i].at[index, 'RESULT'] = "inc"
                elif leftmost[1] in nullList:
                    datalist[i].at[index, 'RESULT'] = "null"
            except ValueError as e:
                datalist[i].at[i, 'RESULT'] = "//ERROR//"
            
            
            
            #Clean TBI Class Section
            #allows filling down since we wrote this info only once per paper
            if any(civ in row['TBI Class'] for civ in ["Civilian", "civilian", "civ", "Civ", "CIVILIAN"]):
                datalist[i].at[index, 'TBI Class'] = "civilian"
            elif any(sport in row['TBI Class'] for sport in ["sport", "Sport", "Athlete", "athlete", "ATHLETE", "SPORT"]):
                datalist[i].at[index, 'TBI Class'] = "sport"
            elif any(mil in row['TBI Class'] for mil in ["Military", "military", "blast", "Blast", "MILITARY", "BLAST"]):
                datalist[i].at[index, 'TBI Class'] = "military"
            elif any(mix in row['TBI Class'] for mix in ["mix", "Mix", "MIX"]):
                datalist[i].at[index, 'TBI Class'] = "mix Type"    
            elif index-1 >= 0 and datalist[i].at[index, 'TBI Class'] == "":  #fill down
                datalist[i].at[index, 'TBI Class'] = datalist[i].at[index -1, 'TBI Class']
            else: 
                datalist[i].at[index, 'TBI Class'] = "//ERROR//"
            
                
            #Clean Severity Section
            #allows filling down since we wrote this info only once per paper
            hasMild = False
            hasMod = False
            hasSev = False
            hasMix = False
            if any(mild in row['Severity'] for mild in mildTerms):
                hasMild = True
            if any(mod in row['Severity'] for mod in modTerms):  #we sometimes used shortenings for moderate/severe
                hasMod = True
            if any(sev in row['Severity'] for sev in sevTerms):
                hasSev = True
            if any(mix in row['Severity'] for mix in mixTerms):
                hasMix = True
                
            if row['Severity'] == "" and index-1 >= 0:   #fill down
                datalist[i].at[index, 'Severity'] = datalist[i].at[index -1, 'Severity'] #fill down
            elif not row['Severity'] == "" and not any(keyw in row['Severity'] for keyw in mildTerms + modTerms + sevTerms + mixTerms):  #check for errors
                datalist[i].at[index, 'Severity'] = "//ERROR//"
            elif hasMild and hasMod and not hasSev:
                datalist[i].at[index, 'Severity'] = "m/mod"
            elif not hasMild and hasMod and hasSev:
                datalist[i].at[index, 'Severity'] = "mod/sev"
            elif hasMild and not hasMod and not hasSev:
                datalist[i].at[index, 'Severity'] = "mild"
            elif not hasMild and hasMod and not hasSev:
                datalist[i].at[index, 'Severity'] = "moderate"
            elif not hasMild and not hasMod and hasSev:
                datalist[i].at[index, 'Severity'] = "severe"
            elif hasMix:
                datalist[i].at[index, 'Severity'] = "mix severity"
            elif not row['Severity'] == "":
                datalist[i].at[index, 'Severity'] = "mix severity"
            
            
            #clean Age section
            #allows filling down since we wrote this info only once per paper
            if any(mix in row['Age'] for mix in mixList) or (any(adult in row['Age'] for adult in adultList) and (any(adolescent in row['Age'] for adolescent in adolescentList) or any(child in row['Age'] for child in childList))) or (any(adolescent in row['Age'] for adolescent in adolescentList) and any(child in row['Age'] for child in childList)):
                datalist[i].at[index, 'Age'] = "mix age"
            elif any(adult in row['Age'] for adult in adultList):
                datalist[i].at[index, 'Age'] = 'adult'
            elif any(adolescent in row['Age'] for adolescent in adolescentList):
                datalist[i].at[index, 'Age'] = "adolescent"
            elif any(child in row['Age'] for child in childList):
                datalist[i].at[index, 'Age'] = "child"
            elif row['Age'] == "" and index-1 >= 0:  #fill down
                datalist[i].at[index, 'Age'] = datalist[i].at[index -1, 'Age'] #fill down
            else:
                datalist[i].at[index, 'Age'] = "//ERROR//"

            #clean Chronicity Section 
            #note: no filling, each finding must have its own chronicity
            hasAcute = False
            hasSubacute = False
            hasChronic = False
            hasMix = False
            hasRepSub = False
            
            #dealing with the fact that acute exists within subacute
            numAcutes = 0
            for acute in acuteList:
                numAcutes += row['Chronicity'].count(acute) 
            
            #if acute and not subacute we have an actual acute, if acute shows up multiple places we should have acute
            #in the form acute/subacute
            if numAcutes == 1 and not any (sub in row['Chronicity'] for sub in subacuteList) or numAcutes > 1:
                hasAcute = True
                
            if any (sub in row['Chronicity'] for sub in subacuteList):
                hasSubacute = True
            if any (chron in row['Chronicity'] for chron in chronicList):
                hasChronic = True
            if any (mix in row['Chronicity'] for mix in mixedList):
                hasMix = True
            if any (repSub in row['Chronicity'] for repSub in repSubList):
                hasRepSub = True
            if hasRepSub:
                datalist[i].at[index, 'Chronicity'] = "repsub"
            elif hasMix or (hasAcute and hasChronic):
                datalist[i].at[index, 'Chronicity'] = "mix cnicity"
            elif hasAcute and hasSubacute and not hasChronic:
                datalist[i].at[index, 'Chronicity'] = "ac/subac"
            elif not hasAcute and hasSubacute and hasChronic:
                datalist[i].at[index, 'Chronicity'] = "subac/chron"
            elif not hasAcute and not hasSubacute and hasChronic:
                datalist[i].at[index, 'Chronicity'] = "chronic"
            elif hasAcute and not hasSubacute and not hasChronic:
                datalist[i].at[index, 'Chronicity'] = "Acute"
            elif not hasAcute and hasSubacute and not hasChronic:
                datalist[i].at[index, 'Chronicity'] = "subacute"   
            else:
                datalist[i].at[index, 'Chronicity'] = "//ERROR//"
                
            #clean Control Section
            #allows filling down since we wrote this info only once per paper
            if row['Control Type'] == "" and index-1 >= 0:   #fill down
                datalist[i].at[index, 'Control Type'] = datalist[i].at[index -1, 'Control Type']
            elif any(healthy in row['Control Type'] for healthy in healthyList):
                datalist[i].at[index, 'Control Type'] = "HC"
            elif any(inSport in row['Control Type'] for inSport in inSportList):
                datalist[i].at[index, 'Control Type'] = "ISC"
            elif any(nonCon in row['Control Type'] for nonCon in nonContactList):
                datalist[i].at[index, 'Control Type'] = "NCC"    
            elif any(tbiPlus in row['Control Type'] for tbiPlus in tbiPlusMoodList):
                datalist[i].at[index, 'Control Type'] = "TBI+"
            elif any(mood in row['Control Type'] for mood in moodList):
                datalist[i].at[index, 'Control Type'] = "Mood"
            elif any(other in row['Control Type'] for other in otherList):
                datalist[i].at[index, 'Control Type'] = "Other Control"    
            else: 
                datalist[i].at[index, 'Control Type'] = "//ERROR//"
                
            #clean up sample sizes (fill down), and put errors for missing info
            if row['TBI (n)'] == "" and index-1 >= 0:   #fill down
                datalist[i].at[index, 'TBI (n)'] = datalist[i].at[index-1, 'TBI (n)']
            elif row['TBI (n)'] == "X": 
                datalist[i].at[index, 'TBI (n)'] = "//ERROR//"
            
            if row['HC (n)'] == "" and index-1 >= 0:   #fill down
                datalist[i].at[index, 'HC (n)'] = datalist[i].at[index-1, 'HC (n)']
            elif row['HC (n)'] == "X": 
                datalist[i].at[index, 'HC (n)'] = "//ERROR//"
                
    return datalist      
##end cleanData function ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----


#smallTable function ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
#this function takes in cleaned dataframes (some output from cleanData), and returns dataframes which #contain only info salient to the actual paper (purpose: for inclusion in certain journals in which table of the papers may be published)
#identifies unique paper titles, collects all relevant info that may differ across observations for this paper, cleans and outputs
#a small pretty dataframe

def smallTable(datalist, ageFrame):
    
    smallTableList = []
    papers = []
    paper_chron = []
    drop_indices = []
    
    for i in range(len(datalist)):
        smallTableList.append( datalist[i].filter(["WITHIN NETWORK FINDINGS", 'TBI Class', 'Severity', 'Age', 'Chronicity', 'Control Type', 'TBI (n)', 'HC (n)'], axis = 1) )
    
    smallTable =  pd.concat(smallTableList)
    
    smallTable.reset_index(drop = True, inplace = True)
    
    #first pass: fill papers
    for index, row, in smallTable.iterrows():
        #fill papers downward, need to add all necessary chronicity info which is found by paper
        if row['WITHIN NETWORK FINDINGS'] == "" and index -1 >= 0:
            smallTable.at[index, 'WITHIN NETWORK FINDINGS'] = smallTable.at[index-1, 'WITHIN NETWORK FINDINGS']

#second pass: gather all chron info
    for index, row, in smallTable.iterrows():
        
        #add chronicity information in rows where a paper is reported again, then schedule to delete 
        #this redundant paper row
        if row['WITHIN NETWORK FINDINGS'] in papers: 
            for pchron in paper_chron:
                if row['WITHIN NETWORK FINDINGS'] == pchron[0] and not row['Chronicity'] in pchron[1]:
                    pchron[1] += (' + ' + row['Chronicity'])
            drop_indices.append(index)
        #if encountering a new paper, add to the tracker lists
        else: 
            papers.append(row['WITHIN NETWORK FINDINGS'])
            paper_chron.append([row['WITHIN NETWORK FINDINGS'], row['Chronicity']])
            
    
    smallTable.drop(drop_indices, inplace = True)
    smallTable.reset_index(drop = True, inplace = True)
    
    #third pass: update the chronicities now that the entire table has been searched and all chronicity info has been added for a given paper
    for index, row, in smallTable.iterrows():
        for pchron in paper_chron:
            if row['WITHIN NETWORK FINDINGS'] == pchron[0]:
                row['Chronicity'] = pchron[1]
                
    #MAKE PRETTY: 11/30/21 UPDATE
    
    
    #MERGE IN AGE INFO (Future update? Not working quite right yet on manning and one other)
    #ageFrame['WITHIN NETWORK FINDINGS'].str.strip()
    #smallTable = smallTable.merge(ageFrame, how = 'left', left_on = 'WITHIN NETWORK FINDINGS', right_on = 'WITHIN NETWORK FINDINGS')
    
    smallTable.rename(columns = {'WITHIN NETWORK FINDINGS': 'Study', 'AGE': 'Average TBI Age'}, inplace=True)
    smallTable['Study'] = smallTable['Study'].map(study_title_cleaner)
    smallTable['TBI Class'] = smallTable['TBI Class'].map(tbi_class_cleaner)
    smallTable['Severity'] = smallTable['Severity'].map(severity_cleaner)
    smallTable['Age'] = smallTable['Age'].map(age_cleaner)
    smallTable['Chronicity'] = smallTable['Chronicity'].map(chronicity_cleaner)
    
    smallTable.drop(axis = 1, labels = 'Control Type', inplace=True)
    
    smallTable['TBI (n)'] = smallTable['TBI (n)'].astype('int64')
    smallTable['HC (n)'] = smallTable['HC (n)'].astype('int64')
    
    #not working yet
    #rounding ages bc not super accurate to begin with, some studies did median some did mean, some had exact vals which seemed rounded
    #smallTable['Average TBI Age'] = smallTable['Average TBI Age'].fillna('Not Reported')
    #smallTable['Average TBI Age'] = smallTable['Average TBI Age'].astype('str')
    
    #smallTable['Average TBI Age'] = smallTable['Average TBI Age'].map(tbi_age_cleaner)
    
    smallTable.sort_values(axis=0, by=['Study'], inplace=True)
    smallTable.reset_index(drop=True, inplace=True)
                                 
    smallTable.index += 1
    
    #MANUAL(CHANGE IF ABOVE CODE CHANGED)
    #A couple manual fixes for weird entries we had (we had paper B in many cases as a remnant where the other paper of same
    #title was already removed from the study)
    smallTable.loc[22, 'Study'] = smallTable.loc[22, 'Study'].replace(' B', '')
    smallTable.loc[28, 'Study'] = smallTable.loc[28, 'Study'].replace(' B', '')
    smallTable.loc[38, 'Study'] = smallTable.loc[38, 'Study'].replace(' B', '')
    smallTable.loc[42, 'Study'] = smallTable.loc[42, 'Study'].replace(' B', '')
    smallTable.loc[49, 'Study'] = smallTable.loc[49, 'Study'].replace(' B', '')
    
    return smallTable


##end smallTable function ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

def militaryOnly(datalist):
    for i in range(len(datalist)):
        drop_indices = []
        for index, row in datalist[i].iterrows():
            if not row['TBI Class'] == 'military':
                drop_indices.append(index)
                
        datalist[i].drop(drop_indices, inplace = True)
    
    return datalist





#------- helper functions
def study_title_cleaner(title):
    
    #deal with years which aren't encapsulated in parens
    pattern = re.compile('\d{4}')
    if pattern.search(title):
        match = pattern.search(title)
        yearStart = match.span()[0]
        if title[yearStart-1] != '(':
            title = title[:yearStart] + '(' + title[yearStart:yearStart + 4] + ')' + title[yearStart+4:]
    
    #name second paper with B instead of #2
    title = title.replace('#2', 'B')
    
    #strip locations
    strip_after = max(title.find('B'), title.find(')'))
    title = title[:strip_after+1]
    
    #don't care about B's when they are before parens, usually a mistake/remnant actually
    if title.find('B') < title.find(')'):
        title = title.replace('B', '')
        
    #one particular case for Li-- this is me being lazy :P
    title.replace('(2020b)', '(2020) B')
            
    return title


def tbi_class_cleaner(tbi):
    tbi = tbi.replace('civilian', 'Civilian')
    tbi = tbi.replace('military', 'Military')
    tbi = tbi.replace('sport', 'Sport')
    return tbi
    
def severity_cleaner(sev):
    sev = sev.replace('mild', 'Mild')
    sev = sev.replace('mix severity', 'Mixed')
    sev = sev.replace('m/mod', 'Mild/Moderate')
    sev = sev.replace('mod/sev', 'Moderate/Severe')
    sev = sev.replace('severe', 'Severe')
    return sev

def age_cleaner(age):
    age = age.replace('child', 'Child')
    age = age.replace('adult', 'Adult')
    age = age.replace('mix age', 'Mixed')
    age = age.replace('adolescent', 'Adolescent')
    return age

def chronicity_cleaner(chron):
    chron = chron.replace('ac/subac', 'Acute/Subacute')
    chron = chron.replace('chronic', 'Chronic')
    chron = chron.replace('subac/chron', 'Subacute/Chronic')
    chron = chron.replace('+', '&')
    chron = chron.replace('//ERROR//', 'Not Stated')
    chron = chron.replace('subacute', 'Subacute')
    return chron

def tbi_age_cleaner(age):
    decimal = age.find('.')
    if (decimal != -1):
        age = age[:decimal]
    return age