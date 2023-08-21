import pandas as pd  #used throughout
import re  #for numAuthors function, to match author names
from IPython.display import display
import numpy as np #for holding data in as numpy arrays in sampleDist function, and for checking nan in resultsByAge func
import seaborn as sns #for sampleDist function
from matplotlib import pyplot as plt #for sampleDist function

#Contains runStats(), queryStats(), easyQueryStats(), printStats()

#List of classifications (used in a couple funcs)
#made it so that no string was contained within another string to make for simpler searching when coming up with statistics
nets = ["dmn", "ecn", "limb", "sn", "dan", "van", "vis", "smn"]
results = ["inc", "dec", "null"]
severities = ["mild", "m/mod", "moderate", "mod/sev", "severe", "mix severity", "No Severity"]
ages = ["child", "adolescent", "adult", "mix age", "No Age"]
chronicities = ["Acute", "ac/subac", "subacute", "subac/chron", "chronic", "repsub", "mix cnicity", "No Cnicity"]
types = ["sport", "military", "civilian", "mix Type"]
controls = ["HC", "ISC", "NCC", "TBI+", "Mood", "Other Control"]

#runStats() function----------------------------------------------------------------------------------------------------------------------------
#runStats(datalist, stats): runStats() takes in a list of pandas dataframes (these should be the cleaned ones output from cleanData()) as well 
#as a 2D 'stats' list (a list of size 2 lists, where each size 2 list is a pair: a classification, and a count of how 
#many times that classification shows up in the data (this should start at 0 for all classifications the same way I initially 
#set up my stats object). It outputs a modified 2D 'stats' list with the counts added up for each classification after parsing through the provided datalist.
#Rules: Mostly just be careful to pass a stats 2D list which has counts of 0 for everything if you want an accurate analysis of 
#the dataframes you passed in. Furthermore, generating the stats object is performed immediately about this function definition in my code, 
#and could be altered for an alternate classification system.
#Also note: errors should already be checked! they can be allowed to 
#remain if desired for missing info on severity, age, chronicity. Other rows must be figured out. Data is required.
def runStats(datalist, stats, dataOrder, quartiles):
    for i in range(len(datalist)):
        for index, row in datalist[i].iterrows():
            quartile_score = 0
            
            #determine population size quartile (based on total sample size)
            if ( int(row['TBI (n)']) + int(row['HC (n)']) ) < quartiles[0]:
                quartile_score = 1
            elif ( int(row['TBI (n)']) + int(row['HC (n)']) ) >= quartiles[0] \
                and ( int(row['TBI (n)']) + int(row['HC (n)']) ) < quartiles[1]:
                quartile_score = 2
            elif ( int(row['TBI (n)']) + int(row['HC (n)']) ) >= quartiles[1] \
                and ( int(row['TBI (n)']) + int(row['HC (n)']) ) < quartiles[2]:
                quartile_score = 3
            if ( int(row['TBI (n)']) + int(row['HC (n)']) ) >= quartiles[2]:
                quartile_score = 4
            
            #determine classification
            classif = ""
            classif += dataOrder[i]
            classif += "_" + row['RESULT']            
            
            if row['Severity'] == "//ERROR//":
                classif += "_" + "No Severity"
            else:
                classif += "_" + row['Severity']
                
            if row['Age'] == "//ERROR//":
                classif += "_" + "No Age"
            else:
                classif += "_" + row['Age']
                
            if row['Chronicity'] == "//ERROR//":
                classif += "_" + "No Cnicity"
            else:
                classif += "_" + row['Chronicity']
                
            classif += "_" + row['TBI Class']
            classif += "_" + row['Control Type']
            
            #update UW, TBI weighted, total weighted, and quartile scored counts (in that order) 
            for stat in stats:
                if stat[0] == classif:
                    stat[1] += 1
                    if row['TBI (n)'] != "//ERROR//":
                        stat[2] += int(row['TBI (n)'])
                    if row['TBI (n)'] != "//ERROR//" and row['HC (n)'] != "//ERROR//":
                        stat[3] += ( int(row['TBI (n)']) + int(row['HC (n)']) )  
                    stat[4] += quartile_score


#end runStats() function----------------------------------------------------------------------------------------------------------------------------




#queryStats() function----------------------------------------------------------------------------------------------------------------------------
#queryStats(stats, weight = "UW", query1="", query2="", query3="", query4="", query5="", query6=""): queryStats() allows you to input a stats 2D list 
#(presumably resulting from runStats), as well as 0 to 6 queries (a query is a string matching a possible type of result such as "dmn" for 
#default mode network results, etc.) and outputs a list of [increase decrease null] results, in that order. This function is integral to printStats.
#As of 08/11/2021, you also have to provide a weighting type for your results as the second parameter.
#"UW"- unweighted results
#"W-TBI" TBI sample size weighted results
#"W-Total" Total sample size weighted results
#"Quartiles" Weighted by a simple scoring of sample size quartiles
def queryStats(stats, weight = "UW", query1="", query2="", query3="", query4="", query5="", query6=""):
    count_inc = 0
    count_dec = 0
    count_null = 0
    for stat in stats:
        if "inc" in stat[0] and query1 in stat[0] and query2 in stat[0] and query3 in stat[0] \
            and query4 in stat[0] and query5 in stat[0] and query6 in stat[0]:
                if weight == "UW":
                    count_inc += stat[1]
                elif weight == "W-TBI":
                    count_inc += stat[2]
                elif weight == "W-Total":
                    count_inc += stat[3]
                elif weight == "Quartiles":
                    count_inc += stat[4]
        if "dec" in stat[0] and query1 in stat[0] and query2 in stat[0] and query3 in stat[0] \
            and query4 in stat[0] and query5 in stat[0] and query6 in stat[0]:
                if weight == "UW":
                    count_dec += stat[1]
                elif weight == "W-TBI":
                    count_dec += stat[2]
                elif weight == "W-Total":
                    count_dec += stat[3]
                elif weight == "Quartiles":
                    count_dec += stat[4]    
        if "null" in stat[0] and query1 in stat[0] and query2 in stat[0] and query3 in stat[0] \
            and query4 in stat[0] and query5 in stat[0] and query6 in stat[0]:
                if weight == "UW":
                    count_null += stat[1]
                elif weight == "W-TBI":
                    count_null += stat[2]
                elif weight == "W-Total":
                    count_null += stat[3]
                elif weight == "Quartiles":
                    count_null += stat[4]
    return [count_inc, count_dec, count_null]
#end queryStats() function----------------------------------------------------------------------------------------------------------------------------



#easyQueryStats function--------------------------------------------------------------------------------------------------
#easyQueryStats() works exactly like queryStats except it prints out a mini dataframe 
#of your requested statistics, making it easier to use without additional coding.
#As of 08/11/2021, you also have to provide a weighting type for your results as the second parameter.
#"UW"- unweighted results
#"W-TBI" TBI sample size weighted results
#"W-Total" Total sample size weighted results
#"Quartiles" Weighted by a simple scoring of sample size quartiles

def easyQueryStats(stats, weight = "UW", query1="", query2="", query3="", query4="", query5="", query6=""):
    queryList = [query1, query2, query3, query4, query5, query6]
    queryList = [query for query in queryList if not query == ""]
    if(any(query not in nets+results+severities+ages+chronicities+types+controls for query in queryList)):
        print("One of more of your queries did not correspond to a valid keyword. Double check your input!")
        return
    
    if weight not in ["UW", "W-TBI", "W-Total", "Quartiles"]:
        print("Your providing weighting choice did not match a valid keyword. Double check your input!")
        return
    
    res = queryStats(stats, weight, query1, query2, query3, query4, query5, query6)
    
    print("You asked for all " + weight + " results corresponding to: " + query1 + " " + query2 + " " + query3 + " " + query4 + " " + query5 + " " + query6)
    print("Here are the results...")
    result = {"Increase": res[0], "Decrease": res[1], "Null": res[2]}
    res_Index = [query1 + " " + query2 + " " + query3 + " " + query4 + " " + query5 + " " + query6]
    df = pd.DataFrame(result, index = res_Index)
    display(df)
    return
#end easyQueryStats function--------------------------------------------------------------------------------------------------    






#printStats() function----------------------------------------------------------------------------------------------------------------------------
#printStats(stats): printStats() uses queryStats to generate a bunch of pandas dataframes corresponding to relevant outputs for our literature review,
#making visualization of a ton of different subsections of our results easy and clear.
#A weight must be provided as described for queryStats(), otherwise the default is unweighted results.
def printStats(stats, weight = "UW"):
    print("------------------------------\n")
    print('Starting ' + weight + ' Counts...')
    print('\n')
    
    #network totals:
    
    #dmn
    dmn = queryStats(stats, weight, "dmn")

    #ecn        
    ecn = queryStats(stats, weight, "ecn")
    
    #Limbic
    limb = queryStats(stats, weight, "limb")
    
    #Salience/Ventral
    sn = queryStats(stats, weight, "sn")
    
    van = queryStats(stats, weight, "van")
            
    snvan = [sn[0] + van[0], sn[1] + van[1], sn[2] + van[2]]
    
    
    #DAN
    dan = queryStats(stats, weight, "dan")
    
    #Visual
    vis = queryStats(stats, weight, "vis")
    
    #Sensorimotor
    smn = queryStats(stats, weight, "smn")
    
    total_inc = dmn[0] + ecn[0] + limb[0] + snvan[0] + dan[0] + vis[0] + smn[0]
    total_dec = dmn[1] + ecn[1] + limb[1] + snvan[1] + dan[1] + vis[1] + smn[1]
    total_null = dmn[2] + ecn[2] + limb[2] + snvan[2] + dan[2] + vis[2] + smn[2]
    
    data_totals = {'Increase':[dmn[0], ecn[0], limb[0], snvan[0], dan[0], vis[0], smn[0], total_inc], 
                'Decrease':[dmn[1], ecn[1], limb[1], snvan[1], dan[1], vis[1], smn[1], total_dec], 
                'Null':[dmn[2], ecn[2], limb[2], snvan[2], dan[2], vis[2], smn[2], total_null]}        
    df_totals = pd.DataFrame(data_totals, index = ['DMN', 'ECN', 'Limbic', 'Salience/VAN', 'DAN', 'Visual', 'Sensorimotor', 'Total'])
    
    print("Network Totals (" + weight +  "): ")
    display(df_totals)
    
    #now in detail..
    detailed_index = ['All', 'Mild', 'Mild/Moderate', 'Moderate', 'Moderate/Severe', 
             'Severe', 'Mixed Severity', 'No Severity Stated', 'Child', 'Adolescent', 'Adult', 'Mixed Age', 'No Age Stated', 
             'Acute', 'Acute/Subacute', 'Subacute', 'Subacute/Chronic', 'Chronic', 'Repetitive Subconcussive',
             'Mixed Chronicity', 'No Chronicity Stated', 'Sport', 'Military', 'Civilian', 'Mixed Type', 
             'Healthy Control', 'No Contact Control', 'In Sport Control', 'Other Control']
    
    
    #All networks in Detail-------------------:
    print("All Networks in Detail (" + weight +  "):")

    all = [total_inc, total_dec, total_null]
    all_mild = queryStats(stats, weight, "mild")
    all_mildMod = queryStats(stats, weight, "m/mod")
    all_mod = queryStats(stats, weight, "moderate")
    all_modSev = queryStats(stats, weight, "mod/sev")
    all_sev = queryStats(stats, weight, "severe")
    all_mixSev = queryStats(stats, weight, "mix severity")
    all_noSev = queryStats(stats, weight, "No Severity")
    all_child = queryStats(stats, weight, "child")
    all_adolescent = queryStats(stats, weight, "adolescent")
    all_adult = queryStats(stats, weight, "adult")
    all_mixAge = queryStats(stats, weight, "mix age")
    all_noAge = queryStats(stats, weight, "No Age")
    all_acute = queryStats(stats, weight, "Acute")
    all_acuteSub = queryStats(stats, weight, "ac/subac")
    all_subacute = queryStats(stats, weight, "subacute")
    all_subChron = queryStats(stats, weight, "subac/chron")
    all_chronic = queryStats(stats, weight, "chronic")
    all_repSub = queryStats(stats, weight, "repsub")
    all_mixChron = queryStats(stats, weight, "mix cnicity")
    all_noChron = queryStats(stats, weight, "No Cnicity")
    all_sport = queryStats(stats, weight, "sport")
    all_military = queryStats(stats, weight, "military")
    all_civilian = queryStats(stats, weight, "civilian")
    all_mixType = queryStats(stats, weight, "mix Type")
    all_healthyControl = queryStats(stats, weight, "HC")
    all_noContactControl = queryStats(stats, weight, "NCC")
    all_inSportControl = queryStats(stats, weight, "ISC")
    all_otherControl = queryStats(stats, weight, "Other Control")
    
    all_categories = [all, all_mild, all_mildMod, all_mod, all_modSev, all_sev, 
                  all_mixSev, all_noSev, all_child, all_adolescent, all_adult,
                 all_mixAge, all_noAge, all_acute, all_acuteSub, all_subacute, all_subChron, all_chronic, all_repSub, 
                 all_mixChron, all_noChron, all_sport, all_military, all_civilian, all_mixType, 
                 all_healthyControl, all_noContactControl, all_inSportControl, all_otherControl]
    
    all_incList = []
    all_decList = []
    all_nullList = []
    for cat in all_categories:
        all_incList.append(cat[0])
        all_decList.append(cat[1])
        all_nullList.append(cat[2])
    
    data_all = {'Increase': all_incList, 
                'Decrease': all_decList, 
                'Null': all_nullList}        
    df_all = pd.DataFrame(data_all, index = detailed_index)
    display(df_all)
    
    #BY SEVERITY AND CHRONICITY (ALL)
    print("Results by Severity & Chronicity (" + weight +  ")")
    mildAcute = queryStats(stats, weight, "mild", "Acute")
    mildAcuteSubacute = queryStats(stats, weight, "mild", "ac/subac")
    mildSubacute = queryStats(stats, weight, "mild", "subacute")
    mildSubacuteChronic = queryStats(stats, weight, "mild", "subac/chron")
    mildChronic = queryStats(stats, weight, "mild", "chronic")
    mildMixChron = queryStats(stats, weight, "mild", "mix cnicity")
    mildNoChron = queryStats(stats, weight, "mild", "No Cnicity")
    
    mildModAcute = queryStats(stats, weight, "m/mod", "Acute") 
    mildModAcuteSubacute = queryStats(stats, weight, "m/mod", "ac/subac")
    mildModSubacute = queryStats(stats, weight, "m/mod", "subacute")
    mildModSubacuteChronic = queryStats(stats, weight, "m/mod", "subac/chron")
    mildModChronic = queryStats(stats, weight, "m/mod", "chronic")
    mildModMixChron = queryStats(stats, weight, "m/mod", "mix cnicity")
    mildModNoChron = queryStats(stats, weight, "m/mod", "No Cnicity")
    
    modAcute = queryStats(stats, weight, "moderate", "Acute") 
    modAcuteSubacute = queryStats(stats, weight, "moderate", "ac/subac")
    modSubacute = queryStats(stats, weight, "moderate", "subacute")
    modSubacuteChronic = queryStats(stats, weight, "moderate", "subac/chron")
    modChronic = queryStats(stats, weight, "moderate", "chronic")
    modMixChron = queryStats(stats, weight, "moderate", "mix cnicity")
    modNoChron = queryStats(stats, weight, "moderate", "No Cnicity")
    
    modSevereAcute = queryStats(stats, weight, "mod/sev", "Acute") 
    modSevereAcuteSubacute = queryStats(stats, weight, "mod/sev", "ac/subac")
    modSevereSubacute = queryStats(stats, weight, "mod/sev", "subacute")
    modSevereSubacuteChronic = queryStats(stats, weight, "mod/sev", "subac/chron")
    modSevereChronic = queryStats(stats, weight, "mod/sev", "chronic")
    modSevereMixChron = queryStats(stats, weight, "mod/sev", "mix cnicity")
    modSevereNoChron = queryStats(stats, weight, "mod/sev", "No Cnicity")
    
    severeAcute = queryStats(stats, weight, "severe", "Acute") 
    severeAcuteSubacute = queryStats(stats, weight, "severe", "ac/subac")
    severeSubacute = queryStats(stats, weight, "severe", "subacute")
    severeSubacuteChronic = queryStats(stats, weight, "severe", "subac/chron")
    severeChronic = queryStats(stats, weight, "severe", "chronic")
    severeMixChron = queryStats(stats, weight, "severe", "mix cnicity")
    severeNoChron = queryStats(stats, weight, "severe", "No Cnicity")
    
    mixedSevAcute = queryStats(stats, weight, "mix severity", "Acute") 
    mixedSevAcuteSubacute = queryStats(stats, weight, "mix severity", "ac/subac")
    mixedSevSubacute = queryStats(stats, weight, "mix severity", "subacute")
    mixedSevSubacuteChronic = queryStats(stats, weight, "mix severity", "subac/chron")
    mixedSevChronic = queryStats(stats, weight, "mix severity", "chronic")
    mixedSevMixChron = queryStats(stats, weight, "mix severity", "mix cnicity")
    mixedSevNoChron = queryStats(stats, weight, "mix severity", "No Cnicity")
    
    noSevAcute = queryStats(stats, weight, "No Severity", "Acute") 
    noSevAcuteSubacute = queryStats(stats, weight, "No Severity", "ac/subac")
    noSevSubacute = queryStats(stats, weight, "No Severity", "subacute")
    noSevSubacuteChronic = queryStats(stats, weight, "No Severity", "subac/chron")
    noSevChronic = queryStats(stats, weight, "No Severity", "chronic")
    noSevMixChron = queryStats(stats, weight, "No Severity", "mix cnicity")
    noSevNoChron = queryStats(stats, weight, "No Severity", "No Cnicity")
    
    sevChron_list = [mildAcute, mildAcuteSubacute, mildSubacute, mildSubacuteChronic, mildChronic, mildMixChron,
                    mildNoChron, mildModAcute, mildModAcuteSubacute, mildModSubacute, mildModSubacuteChronic, 
                    mildModChronic, mildModMixChron, mildModNoChron, modAcute, modAcuteSubacute, modSubacute,
                    modSubacuteChronic, modChronic, modMixChron, modNoChron, modSevereAcute, modSevereAcuteSubacute,
                    modSevereSubacute, modSevereSubacuteChronic, modSevereChronic, modSevereMixChron, modSevereNoChron,
                    severeAcute, severeAcuteSubacute, severeSubacute, severeSubacuteChronic, severeChronic, severeMixChron,
                    severeNoChron, mixedSevAcute, mixedSevAcuteSubacute, mixedSevSubacute, mixedSevSubacuteChronic,
                    mixedSevChronic, mixedSevMixChron, mixedSevNoChron, noSevAcute, noSevAcuteSubacute, noSevSubacute, noSevSubacuteChronic,
                    noSevChronic, noSevMixChron, noSevNoChron]
    
    sevChron_incList = []
    sevChron_decList = []
    sevChron_nullList = []
    
    for sevChron in sevChron_list:
        sevChron_incList.append(sevChron[0])
        sevChron_decList.append(sevChron[1])
        sevChron_nullList.append(sevChron[2])
    
    sevChron_index = ["Mild Acute", "Mild Acute/Subacute", "Mild Subacute", "Mild Subacute/Chronic", "Mild Chronic", "Mild Mixed Chronicity", "Mild + No Chronicity Stated", 
                      "Mild/Mod Acute", "Mild/Mod Acute/Subacute", "Mild/Mod Subacute", "Mild/Mod Subacute/Chronic", "Mild/Mod Chronic", "Mild/Mod Mixed Chronicity", "Mild/Mod + No Chronicity Stated", 
                      "Moderate Acute", "Moderate Acute/Subacute", "Moderate Subacute", "Moderate Subacute/Chronic", "Moderate Chronic", "Moderate Mixed Chronicity", "Moderate + No Chronicity Stated",
                      "Mod/Sev Acute", "Mod/Sev Acute/Subacute", "Mod/Sev Subacute", "Mod/Sev Subacute/Chronic", "Mod/Sev Chronic", "Mod/Sev Mixed Chronicity", "Mod/Sev + No Chronicity Stated", 
                      "Severe Acute", "Severe Acute/Subacute", "Severe Subacute", "Severe Subacute/Chronic", "Severe Chronic", "Severe Mixed Chronicity", "Severe + No Chronicity Stated",
                      "Mixed Sev. Acute", "Mixed Sev. Acute/Subacute", "Mixed Sev. Subacute", "Mixed Sev. Subacute/Chronic", "Mixed Sev. Chronic", "Mixed Sev. Mixed Chronicity", "Mixed Sev. + No Chronicity Stated", 
                      "No Sev. Stated Acute", "No Sev. Stated Acute/Subacute", "No Sev. Stated Subacute", "No Sev. Stated Subacute/Chronic", "No Sev. Stated Chronic", "No Sev. Stated Mixed Chronicity", "No Sev. Stated + No Chronicity Stated"] 
    
    data_sevChron = {'Increase': sevChron_incList, 
                'Decrease': sevChron_decList, 
                'Null': sevChron_nullList}        
    
    df_sevChron = pd.DataFrame(data_sevChron, sevChron_index)
    display(df_sevChron)
    
    #DMN------------------------------:
    print("DMN in Detail (" + weight +  "):")
    
    dmn_mild = queryStats(stats, weight, "dmn", "mild")
    dmn_mildMod = queryStats(stats, weight, "dmn", "m/mod")
    dmn_mod = queryStats(stats, weight, "dmn", "moderate")
    dmn_modSev = queryStats(stats, weight, "dmn", "mod/sev")
    dmn_sev = queryStats(stats, weight, "dmn", "severe")
    dmn_mixSev = queryStats(stats, weight, "dmn", "mix severity")
    dmn_noSev = queryStats(stats, weight, "dmn", "No Severity")
    dmn_child = queryStats(stats, weight, "dmn", "child")
    dmn_adolescent = queryStats(stats, weight, "dmn", "adolescent")
    dmn_adult = queryStats(stats, weight, "dmn", "adult")
    dmn_mixAge = queryStats(stats, weight, "dmn", "mix age")
    dmn_noAge = queryStats(stats, weight, "dmn", "No Age")
    dmn_acute = queryStats(stats, weight, "dmn", "Acute")
    dmn_acuteSub = queryStats(stats, weight, "dmn", "ac/subac")
    dmn_subacute = queryStats(stats, weight, "dmn", "subacute")
    dmn_subChron = queryStats(stats, weight, "dmn", "subac/chron")
    dmn_chronic = queryStats(stats, weight, "dmn", "chronic")
    dmn_repSub = queryStats(stats, weight, "dmn", "repsub")
    dmn_mixChron = queryStats(stats, weight, "dmn", "mix cnicity")
    dmn_noChron = queryStats(stats, weight, "dmn", "No Cnicity")
    dmn_sport = queryStats(stats, weight, "dmn", "sport")
    dmn_military = queryStats(stats, weight, "dmn", "military")
    dmn_civilian = queryStats(stats, weight, "dmn", "civilian")
    dmn_mixType = queryStats(stats, weight, "dmn", "mix Type")
    dmn_healthyControl = queryStats(stats, weight, "dmn", "HC")
    dmn_noContactControl = queryStats(stats, weight, "dmn", "NCC")
    dmn_inSportControl = queryStats(stats, weight, "dmn", "ISC")
    dmn_otherControl = queryStats(stats, weight, "dmn", "Other Control")
    
    dmn_categories = [dmn, dmn_mild, dmn_mildMod, dmn_mod, dmn_modSev, dmn_sev, 
                  dmn_mixSev, dmn_noSev, dmn_child, dmn_adolescent, dmn_adult,
                 dmn_mixAge, dmn_noAge, dmn_acute, dmn_acuteSub, dmn_subacute, dmn_subChron, dmn_chronic, dmn_repSub, 
                 dmn_mixChron, dmn_noChron, dmn_sport, dmn_military, dmn_civilian, dmn_mixType, 
                 dmn_healthyControl, dmn_noContactControl, dmn_inSportControl, dmn_otherControl]
    
    dmn_incList = []
    for cat in dmn_categories:
        dmn_incList.append(cat[0])
    dmn_decList = []
    for cat in dmn_categories:
        dmn_decList.append(cat[1])
    dmn_nullList = []
    for cat in dmn_categories:
        dmn_nullList.append(cat[2])
    
    data_dmn = {'Increase': dmn_incList, 
                'Decrease': dmn_decList, 
                'Null': dmn_nullList}        
    df_dmn = pd.DataFrame(data_dmn, index = detailed_index)
    display(df_dmn)
    
    #ECN------------------------------:
    print("ECN in Detail (" + weight +  "):")
    
    ecn_mild = queryStats(stats, weight, "ecn", "mild")
    ecn_mildMod = queryStats(stats, weight, "ecn", "m/mod")
    ecn_mod = queryStats(stats, weight, "ecn", "moderate")
    ecn_modSev = queryStats(stats, weight, "ecn", "mod/sev")
    ecn_sev = queryStats(stats, weight, "ecn", "severe")
    ecn_mixSev = queryStats(stats, weight, "ecn", "mix severity")
    ecn_noSev = queryStats(stats, weight, "ecn", "No Severity")
    ecn_child = queryStats(stats, weight, "ecn", "child")
    ecn_adolescent = queryStats(stats, weight, "ecn", "adolescent")
    ecn_adult = queryStats(stats, weight, "ecn", "adult")
    ecn_mixAge = queryStats(stats, weight, "ecn", "mix age")
    ecn_noAge = queryStats(stats, weight, "ecn", "No Age")
    ecn_acute = queryStats(stats, weight, "ecn", "Acute")
    ecn_acuteSub = queryStats(stats, weight, "ecn", "ac/subac")
    ecn_subacute = queryStats(stats, weight, "ecn", "subacute")
    ecn_subChron = queryStats(stats, weight, "ecn", "subac/chron")
    ecn_chronic = queryStats(stats, weight, "ecn", "chronic")
    ecn_repSub = queryStats(stats, weight, "ecn", "repsub")
    ecn_mixChron = queryStats(stats, weight, "ecn", "mix cnicity")
    ecn_noChron = queryStats(stats, weight, "ecn", "No Cnicity")
    ecn_sport = queryStats(stats, weight, "ecn", "sport")
    ecn_military = queryStats(stats, weight, "ecn", "military")
    ecn_civilian = queryStats(stats, weight, "ecn", "civilian")
    ecn_mixType = queryStats(stats, weight, "ecn", "mix Type")
    ecn_healthyControl = queryStats(stats, weight, "ecn", "HC")
    ecn_noContactControl = queryStats(stats, weight, "ecn", "NCC")
    ecn_inSportControl = queryStats(stats, weight, "ecn", "ISC")
    ecn_otherControl = queryStats(stats, weight, "ecn", "Other Control")
    
    ecn_categories = [ecn, ecn_mild, ecn_mildMod, ecn_mod, ecn_modSev, ecn_sev, 
                  ecn_mixSev, ecn_noSev, ecn_child, ecn_adolescent, ecn_adult,
                 ecn_mixAge, ecn_noAge, ecn_acute, ecn_acuteSub, ecn_subacute, ecn_subChron, ecn_chronic, ecn_repSub, 
                 ecn_mixChron, ecn_noChron, ecn_sport, ecn_military, ecn_civilian, ecn_mixType, 
                 ecn_healthyControl, ecn_noContactControl, ecn_inSportControl, ecn_otherControl]
    
    ecn_incList = []
    for cat in ecn_categories:
        ecn_incList.append(cat[0])
    ecn_decList = []
    for cat in ecn_categories:
        ecn_decList.append(cat[1])
    ecn_nullList = []
    for cat in ecn_categories:
        ecn_nullList.append(cat[2])
    
    data_ecn = {'Increase': ecn_incList, 
                'Decrease': ecn_decList, 
                'Null': ecn_nullList}        
    df_ecn = pd.DataFrame(data_ecn, index = detailed_index)
    display(df_ecn)
    
    #Limbic------------------------------:
    print("Limbic in Detail (" + weight +  "):")
    
    limb_mild = queryStats(stats, weight, "limb", "mild")
    limb_mildMod = queryStats(stats, weight, "limb", "m/mod")
    limb_mod = queryStats(stats, weight, "limb", "moderate")
    limb_modSev = queryStats(stats, weight, "limb", "mod/sev")
    limb_sev = queryStats(stats, weight, "limb", "severe")
    limb_mixSev = queryStats(stats, weight, "limb", "mix severity")
    limb_noSev = queryStats(stats, weight, "limb", "No Severity")
    limb_child = queryStats(stats, weight, "limb", "child")
    limb_adolescent = queryStats(stats, weight, "limb", "adolescent")
    limb_adult = queryStats(stats, weight, "limb", "adult")
    limb_mixAge = queryStats(stats, weight, "limb", "mix age")
    limb_noAge = queryStats(stats, weight, "limb", "No Age")
    limb_acute = queryStats(stats, weight, "limb", "Acute")
    limb_acuteSub = queryStats(stats, weight, "limb", "ac/subac")
    limb_subacute = queryStats(stats, weight, "limb", "subacute")
    limb_subChron = queryStats(stats, weight, "limb", "subac/chron")
    limb_chronic = queryStats(stats, weight, "limb", "chronic")
    limb_repSub = queryStats(stats, weight, "limb", "repsub")
    limb_mixChron = queryStats(stats, weight, "limb", "mix cnicity")
    limb_noChron = queryStats(stats, weight, "limb", "No Cnicity")
    limb_sport = queryStats(stats, weight, "limb", "sport")
    limb_military = queryStats(stats, weight, "limb", "military")
    limb_civilian = queryStats(stats, weight, "limb", "civilian")
    limb_mixType = queryStats(stats, weight, "limb", "mix Type")
    limb_healthyControl = queryStats(stats, weight, "limb", "HC")
    limb_noContactControl = queryStats(stats, weight, "limb", "NCC")
    limb_inSportControl = queryStats(stats, weight, "limb", "ISC")
    limb_otherControl = queryStats(stats, weight, "limb", "Other Control")
    
    limb_categories = [limb, limb_mild, limb_mildMod, limb_mod, limb_modSev, limb_sev, 
                  limb_mixSev, limb_noSev, limb_child, limb_adolescent, limb_adult,
                 limb_mixAge, limb_noAge, limb_acute, limb_acuteSub, limb_subacute, limb_subChron, limb_chronic, limb_repSub, 
                 limb_mixChron, limb_noChron, limb_sport, limb_military, limb_civilian, limb_mixType, 
                 limb_healthyControl, limb_noContactControl, limb_inSportControl, limb_otherControl]
    
    limb_incList = []
    for cat in limb_categories:
        limb_incList.append(cat[0])
    limb_decList = []
    for cat in limb_categories:
        limb_decList.append(cat[1])
    limb_nullList = []
    for cat in limb_categories:
        limb_nullList.append(cat[2])
    
    data_limb = {'Increase': limb_incList, 
                'Decrease': limb_decList, 
                'Null': limb_nullList}        
    df_limb = pd.DataFrame(data_limb, index = detailed_index)
    display(df_limb)
    
    #Salience/VAN------------------------:
    print("Salience/VAN in Detail (" + weight +  "):")
    
    #Salience
    sn_mild = queryStats(stats, weight, "sn", "mild")
    sn_mildMod = queryStats(stats, weight, "sn", "m/mod")
    sn_mod = queryStats(stats, weight, "sn", "moderate")
    sn_modSev = queryStats(stats, weight, "sn", "mod/sev")
    sn_sev = queryStats(stats, weight, "sn", "severe")
    sn_mixSev = queryStats(stats, weight, "sn", "mix severity")
    sn_noSev = queryStats(stats, weight, "sn", "No Severity")
    sn_child = queryStats(stats, weight, "sn", "child")
    sn_adolescent = queryStats(stats, weight, "sn", "adolescent")
    sn_adult = queryStats(stats, weight, "sn", "adult")
    sn_mixAge = queryStats(stats, weight, "sn", "mix age")
    sn_noAge = queryStats(stats, weight, "sn", "No Age")
    sn_acute = queryStats(stats, weight, "sn", "Acute")
    sn_acuteSub = queryStats(stats, weight, "sn", "ac/subac")
    sn_subacute = queryStats(stats, weight, "sn", "subacute")
    sn_subChron = queryStats(stats, weight, "sn", "subac/chron")
    sn_chronic = queryStats(stats, weight, "sn", "chronic")
    sn_repSub = queryStats(stats, weight, "sn", "repsub")
    sn_mixChron = queryStats(stats, weight, "sn", "mix cnicity")
    sn_noChron = queryStats(stats, weight, "sn", "No Cnicity")
    sn_sport = queryStats(stats, weight, "sn", "sport")
    sn_military = queryStats(stats, weight, "sn", "military")
    sn_civilian = queryStats(stats, weight, "sn", "civilian")
    sn_mixType = queryStats(stats, weight, "sn", "mix Type")
    sn_healthyControl = queryStats(stats, weight, "sn", "HC")
    sn_noContactControl = queryStats(stats, weight, "sn", "NCC")
    sn_inSportControl = queryStats(stats, weight, "sn", "ISC")
    sn_otherControl = queryStats(stats, weight, "sn", "Other Control")
    
    sn_categories = [sn, sn_mild, sn_mildMod, sn_mod, sn_modSev, sn_sev, 
                  sn_mixSev, sn_noSev, sn_child, sn_adolescent, sn_adult,
                 sn_mixAge, sn_noAge, sn_acute, sn_acuteSub, sn_subacute, sn_subChron, sn_chronic, sn_repSub, 
                 sn_mixChron, sn_noChron, sn_sport, sn_military, sn_civilian, sn_mixType, 
                 sn_healthyControl, sn_noContactControl, sn_inSportControl, sn_otherControl]
    
    sn_incList = []
    for cat in sn_categories:
        sn_incList.append(cat[0])
    sn_decList = []
    for cat in sn_categories:
        sn_decList.append(cat[1])
    sn_nullList = []
    for cat in sn_categories:
        sn_nullList.append(cat[2])
    
    #VAN
    van_mild = queryStats(stats, weight, "van", "mild")
    van_mildMod = queryStats(stats, weight, "van", "m/mod")
    van_mod = queryStats(stats, weight, "van", "moderate")
    van_modSev = queryStats(stats, weight, "van", "mod/sev")
    van_sev = queryStats(stats, weight, "van", "severe")
    van_mixSev = queryStats(stats, weight, "van", "mix severity")
    van_noSev = queryStats(stats, weight, "van", "No Severity")
    van_child = queryStats(stats, weight, "van", "child")
    van_adolescent = queryStats(stats, weight, "van", "adolescent")
    van_adult = queryStats(stats, weight, "van", "adult")
    van_mixAge = queryStats(stats, weight, "van", "mix age")
    van_noAge = queryStats(stats, weight, "van", "No Age")
    van_acute = queryStats(stats, weight, "van", "Acute")
    van_acuteSub = queryStats(stats, weight, "van", "ac/subac")
    van_subacute = queryStats(stats, weight, "van", "subacute")
    van_subChron = queryStats(stats, weight, "van", "subac/chron")
    van_chronic = queryStats(stats, weight, "van", "chronic")
    van_repSub = queryStats(stats, weight, "van", "repsub")
    van_mixChron = queryStats(stats, weight, "van", "mix cnicity")
    van_noChron = queryStats(stats, weight, "van", "No Cnicity")
    van_sport = queryStats(stats, weight, "van", "sport")
    van_military = queryStats(stats, weight, "van", "military")
    van_civilian = queryStats(stats, weight, "van", "civilian")
    van_mixType = queryStats(stats, weight, "van", "mix Type")
    van_healthyControl = queryStats(stats, weight, "van", "HC")
    van_noContactControl = queryStats(stats, weight, "van", "NCC")
    van_inSportControl = queryStats(stats, weight, "van", "ISC")
    van_otherControl = queryStats(stats, weight, "van", "Other Control")
    
    van_categories = [van, van_mild, van_mildMod, van_mod, van_modSev, van_sev, 
                  van_mixSev, van_noSev, van_child, van_adolescent, van_adult,
                 van_mixAge, van_noAge, van_acute, van_acuteSub, van_subacute, van_subChron, van_chronic, van_repSub, 
                 van_mixChron, van_noChron, van_sport, van_military, van_civilian, van_mixType, 
                 van_healthyControl, van_noContactControl, van_inSportControl, van_otherControl]
    
    van_incList = []
    for cat in van_categories:
        van_incList.append(cat[0])
    van_decList = []
    for cat in van_categories:
        van_decList.append(cat[1])
    van_nullList = []
    for cat in van_categories:
        van_nullList.append(cat[2])
        
    #SN/VAN
    snvan_incList = [a + b for a, b in zip(sn_incList, van_incList)]
    snvan_decList = [a + b for a, b in zip(sn_decList, van_decList)]
    snvan_nullList = [a + b for a, b in zip(sn_nullList, van_nullList)]
    
    data_snvan = {'Increase': snvan_incList, 
                'Decrease': snvan_decList, 
                'Null': snvan_nullList}        
    df_snvan = pd.DataFrame(data_snvan, index = detailed_index)
    display(df_snvan)
    
    #DAN------------------------------:
    print("DAN in Detail (" + weight +  "):")
    
    dan_mild = queryStats(stats, weight, "dan", "mild")
    dan_mildMod = queryStats(stats, weight, "dan", "m/mod")
    dan_mod = queryStats(stats, weight, "dan", "moderate")
    dan_modSev = queryStats(stats, weight, "dan", "mod/sev")
    dan_sev = queryStats(stats, weight, "dan", "severe")
    dan_mixSev = queryStats(stats, weight, "dan", "mix severity")
    dan_noSev = queryStats(stats, weight, "dan", "No Severity")
    dan_child = queryStats(stats, weight, "dan", "child")
    dan_adolescent = queryStats(stats, weight, "dan", "adolescent")
    dan_adult = queryStats(stats, weight, "dan", "adult")
    dan_mixAge = queryStats(stats, weight, "dan", "mix age")
    dan_noAge = queryStats(stats, weight, "dan", "No Age")
    dan_acute = queryStats(stats, weight, "dan", "Acute")
    dan_acuteSub = queryStats(stats, weight, "dan", "ac/subac")
    dan_subacute = queryStats(stats, weight, "dan", "subacute")
    dan_subChron = queryStats(stats, weight, "dan", "subac/chron")
    dan_chronic = queryStats(stats, weight, "dan", "chronic")
    dan_repSub = queryStats(stats, weight, "dan", "repsub")
    dan_mixChron = queryStats(stats, weight, "dan", "mix cnicity")
    dan_noChron = queryStats(stats, weight, "dan", "No Cnicity")
    dan_sport = queryStats(stats, weight, "dan", "sport")
    dan_military = queryStats(stats, weight, "dan", "military")
    dan_civilian = queryStats(stats, weight, "dan", "civilian")
    dan_mixType = queryStats(stats, weight, "dan", "mix Type")
    dan_healthyControl = queryStats(stats, weight, "dan", "HC")
    dan_noContactControl = queryStats(stats, weight, "dan", "NCC")
    dan_inSportControl = queryStats(stats, weight, "dan", "ISC")
    dan_otherControl = queryStats(stats, weight, "dan", "Other Control")
    
    dan_categories = [dan, dan_mild, dan_mildMod, dan_mod, dan_modSev, dan_sev, 
                  dan_mixSev, dan_noSev, dan_child, dan_adolescent, dan_adult,
                 dan_mixAge, dan_noAge, dan_acute, dan_acuteSub, dan_subacute, dan_subChron, dan_chronic, dan_repSub, 
                 dan_mixChron, dan_noChron, dan_sport, dan_military, dan_civilian, dan_mixType, 
                 dan_healthyControl, dan_noContactControl, dan_inSportControl, dan_otherControl]
    
    dan_incList = []
    for cat in dan_categories:
        dan_incList.append(cat[0])
    dan_decList = []
    for cat in dan_categories:
        dan_decList.append(cat[1])
    dan_nullList = []
    for cat in dan_categories:
        dan_nullList.append(cat[2])
    
    data_dan = {'Increase': dan_incList, 
                'Decrease': dan_decList, 
                'Null': dan_nullList}        
    df_dan = pd.DataFrame(data_dan, index = detailed_index)
    display(df_dan)
    
    #Visual------------------------------:
    print("Visual in Detail (" + weight +  "):")
    
    vis_mild = queryStats(stats, weight, "vis", "mild")
    vis_mildMod = queryStats(stats, weight, "vis", "m/mod")
    vis_mod = queryStats(stats, weight, "vis", "moderate")
    vis_modSev = queryStats(stats, weight, "vis", "mod/sev")
    vis_sev = queryStats(stats, weight, "vis", "severe")
    vis_mixSev = queryStats(stats, weight, "vis", "mix severity")
    vis_noSev = queryStats(stats, weight, "vis", "No Severity")
    vis_child = queryStats(stats, weight, "vis", "child")
    vis_adolescent = queryStats(stats, weight, "vis", "adolescent")
    vis_adult = queryStats(stats, weight, "vis", "adult")
    vis_mixAge = queryStats(stats, weight, "vis", "mix age")
    vis_noAge = queryStats(stats, weight, "vis", "No Age")
    vis_acute = queryStats(stats, weight, "vis", "Acute")
    vis_acuteSub = queryStats(stats, weight, "vis", "ac/subac")
    vis_subacute = queryStats(stats, weight, "vis", "subacute")
    vis_subChron = queryStats(stats, weight, "vis", "subac/chron")
    vis_chronic = queryStats(stats, weight, "vis", "chronic")
    vis_repSub = queryStats(stats, weight, "vis", "repsub")
    vis_mixChron = queryStats(stats, weight, "vis", "mix cnicity")
    vis_noChron = queryStats(stats, weight, "vis", "No Cnicity")
    vis_sport = queryStats(stats, weight, "vis", "sport")
    vis_military = queryStats(stats, weight, "vis", "military")
    vis_civilian = queryStats(stats, weight, "vis", "civilian")
    vis_mixType = queryStats(stats, weight, "vis", "mix Type")
    vis_healthyControl = queryStats(stats, weight, "vis", "HC")
    vis_noContactControl = queryStats(stats, weight, "vis", "NCC")
    vis_inSportControl = queryStats(stats, weight, "vis", "ISC")
    vis_otherControl = queryStats(stats, weight, "vis", "Other Control")
    
    vis_categories = [vis, vis_mild, vis_mildMod, vis_mod, vis_modSev, vis_sev, 
                  vis_mixSev, vis_noSev, vis_child, vis_adolescent, vis_adult,
                 vis_mixAge, vis_noAge, vis_acute, vis_acuteSub, vis_subacute, vis_subChron, vis_chronic, vis_repSub, 
                 vis_mixChron, vis_noChron, vis_sport, vis_military, vis_civilian, vis_mixType, 
                 vis_healthyControl, vis_noContactControl, vis_inSportControl, vis_otherControl]
    
    vis_incList = []
    for cat in vis_categories:
        vis_incList.append(cat[0])
    vis_decList = []
    for cat in vis_categories:
        vis_decList.append(cat[1])
    vis_nullList = []
    for cat in vis_categories:
        vis_nullList.append(cat[2])
    
    data_vis = {'Increase': vis_incList, 
                'Decrease': vis_decList, 
                'Null': vis_nullList}        
    df_vis = pd.DataFrame(data_vis, index = detailed_index)
    display(df_vis)
    
    #SMN------------------------------:
    print("SMN in Detail (" + weight +  "):")
    
    smn_mild = queryStats(stats, weight, "smn", "mild")
    smn_mildMod = queryStats(stats, weight, "smn", "m/mod")
    smn_mod = queryStats(stats, weight, "smn", "moderate")
    smn_modSev = queryStats(stats, weight, "smn", "mod/sev")
    smn_sev = queryStats(stats, weight, "smn", "severe")
    smn_mixSev = queryStats(stats, weight, "smn", "mix severity")
    smn_noSev = queryStats(stats, weight, "smn", "No Severity")
    smn_child = queryStats(stats, weight, "smn", "child") 
    smn_adolescent = queryStats(stats, weight, "smn", "adolescent")
    smn_adult = queryStats(stats, weight, "smn", "adult")
    smn_mixAge = queryStats(stats, weight, "smn", "mix age")
    smn_noAge = queryStats(stats, weight, "smn", "No Age")
    smn_acute = queryStats(stats, weight, "smn", "Acute")
    smn_acuteSub = queryStats(stats, weight, "smn", "ac/subac")
    smn_subacute = queryStats(stats, weight, "smn", "subacute")
    smn_subChron = queryStats(stats, weight, "smn", "subac/chron")
    smn_chronic = queryStats(stats, weight, "smn", "chronic")
    smn_repSub = queryStats(stats, weight, "smn", "repsub")
    smn_mixChron = queryStats(stats, weight, "smn", "mix cnicity")
    smn_noChron = queryStats(stats, weight, "smn", "No Cnicity")
    smn_sport = queryStats(stats, weight, "smn", "sport")
    smn_military = queryStats(stats, weight, "smn", "military")
    smn_civilian = queryStats(stats, weight, "smn", "civilian")
    smn_mixType = queryStats(stats, weight, "smn", "mix Type")
    smn_healthyControl = queryStats(stats, weight, "smn", "HC")
    smn_noContactControl = queryStats(stats, weight, "smn", "NCC")
    smn_inSportControl = queryStats(stats, weight, "smn", "ISC")
    smn_otherControl = queryStats(stats, weight, "smn", "Other Control")
    
    smn_categories = [smn, smn_mild, smn_mildMod, smn_mod, smn_modSev, smn_sev, 
                  smn_mixSev, smn_noSev, smn_child, smn_adolescent, smn_adult,
                 smn_mixAge, smn_noAge, smn_acute, smn_acuteSub, smn_subacute, smn_subChron, smn_chronic, smn_repSub, 
                 smn_mixChron, smn_noChron, smn_sport, smn_military, smn_civilian, smn_mixType, 
                 smn_healthyControl, smn_noContactControl, smn_inSportControl, smn_otherControl]
    
    smn_incList = []
    for cat in smn_categories:
        smn_incList.append(cat[0])
    smn_decList = []
    for cat in smn_categories:
        smn_decList.append(cat[1])
    smn_nullList = []

    for cat in smn_categories:
        smn_nullList.append(cat[2])
    
    data_smn = {'Increase': smn_incList, 
                'Decrease': smn_decList, 
                'Null': smn_nullList}        
    df_smn = pd.DataFrame(data_smn, index = detailed_index)
    display(df_smn)    
    print("------------------------------\n------------------------------\n------------------------------")
#--end printStats function-----------------------------------------------------------


#sampleDist function
#produces a distribution of TBI and Total Sample Sizes on a per-paper basis (each paper gets one entry), using a cleaned spreadsheet output
#also displays age distribution
def sampleDist(datalist, agesFrame):
    papers_already_counted = []
    TBI_sample_sizes = []
    Total_sample_sizes = []
    ages = []
    
    for index, row in agesFrame.iterrows():
        if np.isnan(row['AGE']):
            continue
        else:
            ages.append(float(row['AGE']))
    
    
    #find sample sizes once for each paper
    for i in range(len(datalist)):
        for index, row in datalist[i].iterrows():
            if not row['WITHIN NETWORK FINDINGS'].isspace() and not row['WITHIN NETWORK FINDINGS'] == "" \
            and not row['WITHIN NETWORK FINDINGS'] in papers_already_counted:
                papers_already_counted.append(row['WITHIN NETWORK FINDINGS'])
                TBI_sample_sizes.append(int(row['TBI (n)']))
                total_sample_size = int(row['TBI (n)']) + int(row['HC (n)'])
                Total_sample_sizes.append(total_sample_size)
    
    print('Found ' + str(len(TBI_sample_sizes)) + " TBI sample sizes reported in the given data:")
    print(str(TBI_sample_sizes) + '\n')
    print('Found ' + str(len(Total_sample_sizes)) + " Total sample sizes reported in the given data:")
    print(str(Total_sample_sizes) + '\n')
    print('Found ' + str(len(ages)) + " average age statistics reported in the given data:")
    print(str(ages) + '\n')
    
    plt.rcParams["figure.figsize"] = [10.00, 5.00]
    plt.rcParams["figure.autolayout"] = True
    fig, axes = plt.subplots(1, 3)
    
    sns.histplot(np.array(TBI_sample_sizes), bins = 20, kde = True, ax=axes[0]).set(title = 'TBI Sample Size Distribution')
    sns.histplot(np.array(Total_sample_sizes), bins = 20, kde = True, ax=axes[1]).set(title = 'Total Sample Size Distribution')
    sns.histplot(np.array(ages), bins = 20, kde = True, ax=axes[2]).set(title = 'Average Age Distribution')
    axes[0].set_xlabel('TBI Group Size (n)')
    axes[1].set_xlabel('Total Sample Size (n)')
    axes[2].set_xlabel('Average/Median Age (yrs)')
    plt.show()
    
    #OUTPUTS FOR QUARTILES
    #Calculate quartiles for scoring cutoffs

    #TBI
    print('TBI percentiles:')
    print(np.percentile(TBI_sample_sizes, 25))
    print(np.percentile(TBI_sample_sizes, 50))
    print(np.percentile(TBI_sample_sizes, 75))
    print('\n')

    #Total
    print('Total percentiles:')
    print(np.percentile(Total_sample_sizes, 25))
    print(np.percentile(Total_sample_sizes, 50))
    print(np.percentile(Total_sample_sizes, 75))
    print('\n')

    #calculate age quartiles
    print('Age Quartiles:')
    print(np.percentile(ages, 25))
    print(np.percentile(ages, 50))
    print(np.percentile(ages, 75))
    print('\n')
          
    return [TBI_sample_sizes, Total_sample_sizes, ages]
#end sampleDist function----------------------------------------------------------------------------------------------------


#numAuthors function---------------------------------------------------------------------------------
#prints the number of unique authors in a dataframe
#requires that author names are followed by either a 1, 2, (, or #
def numAuthors(data):
    
    authorList = []
    
    for index, row in data.iterrows():
        #get only the other name portion
        
        alpha_only = re.compile('[A-zÀ-ú\s]*')
        author = alpha_only.match( row['Study'] )
        
        #strip whitespace off of ends, only allowed within author names (ie: van der Horn)
        authorOnly = author.group(0).strip()
        
        #search for author and add if not found already
        if authorOnly in authorList:
            continue
        else:
            authorList.append(authorOnly)
        
    authorList.sort(key = str.lower)
    print("There were " + str(len(authorList)) + " many unique author names in the dataframe passed.")
    print("Authors found: " + '\n' + str(authorList))
    
    return
#end numAuthors function------------------------------------------------------------------------------------

#investigate results by age
#note that NOT ALL STUDIES reported age so this won't add up to the totals expected!
def resultsByAge(datalist, ageFrame, age_quartiles, age_percentiles):
    print('Note that not all studies reported age, so totals will be < than expected.')
    print('')
    
    #combine all data into one table
    singleTableList = []
    for i in range(len(datalist)):
        singleTableList.append( datalist[i].filter(["WITHIN NETWORK FINDINGS", 'RESULT'], axis = 1) )
    
    singleTable = pd.concat(singleTableList)
    singleTable.reset_index(drop = True, inplace = True)
    singleTable['AGE'] = np.nan
    
    #make a tuple list of all papers and ages from the ageFrame
    age_papers = []
    
    for index, row in ageFrame.iterrows():
        ageFrame.at[index, 'WITHIN NETWORK FINDINGS'] = row['WITHIN NETWORK FINDINGS'].strip()
        if row['AGE'] == "n/a":
            continue
        else:
            age_papers.append((ageFrame.at[index, 'WITHIN NETWORK FINDINGS'], row['AGE']))

    #fill age info in for each paper in the concatenated table
    #and generate list of tuples of results and ages
    
    results_ages = []
    
    for index, row in singleTable.iterrows():
        singleTable.at[index, 'WITHIN NETWORK FINDINGS'] = row['WITHIN NETWORK FINDINGS'].strip()
        
        #fill paper names downward
        if row['WITHIN NETWORK FINDINGS'] == "" and index -1 >= 0:
            singleTable.at[index, 'WITHIN NETWORK FINDINGS'] = singleTable.at[index-1, 'WITHIN NETWORK FINDINGS']
            
        for paper, age in age_papers:
            if singleTable.at[index, 'WITHIN NETWORK FINDINGS'] == paper:
                singleTable.at[index, 'AGE'] = age
                
        if not np.isnan(singleTable.at[index, 'AGE']):
            results_ages.append((row['RESULT'], float(singleTable.at[index, 'AGE'])))
    
    #used for double checking outputs
    #display(singleTable)
    #print(results_ages)    
    
    age_stats = [[1, 0, 0, 0], [2, 0, 0, 0], [3, 0, 0, 0], [4, 0, 0 , 0]]
    age_pstats = [[1, 0, 0, 0], [2, 0, 0, 0], [3, 0, 0, 0], [4, 0, 0 , 0], [5, 0, 0, 0], [6, 0, 0, 0], [7, 0, 0, 0], [8, 0, 0 , 0], [9, 0, 0, 0], [10, 0, 0, 0]]
    
    #now generate a count of increases, decreases, and nulls by age quartile
    for result, age in results_ages:
        #determine quartile score
        quartile_score = 0
        if age < age_quartiles[0]:
            quartile_score = 1
        elif age >= age_quartiles[0] and age < age_quartiles[1]:
            quartile_score = 2
        elif age >= age_quartiles[1] and age < age_quartiles[2]:
            quartile_score = 3
        elif age >= age_quartiles[2]:
            quartile_score = 4
        else:
            print(f'Error!{age}')
            
        #determine percentile score
        percentile_score = 0
        if age < age_percentiles[0]:
            percentile_score = 1
        elif age >= age_percentiles[0] and age < age_percentiles[1]:
            percentile_score = 2
        elif age >= age_percentiles[1] and age < age_percentiles[2]:
            percentile_score = 3
        elif age >= age_percentiles[2] and age < age_percentiles[3]:
            percentile_score = 4
        elif age >= age_percentiles[3] and age < age_percentiles[4]:
            percentile_score = 5
        elif age >= age_percentiles[4] and age < age_percentiles[5]:
            percentile_score = 6
        elif age >= age_percentiles[5] and age < age_percentiles[6]:
            percentile_score = 7
        elif age >= age_percentiles[6] and age < age_percentiles[7]:
            percentile_score = 8
        elif age >= age_percentiles[7] and age < age_percentiles[8]:
            percentile_score = 9
        elif age >= age_percentiles[8]:
            percentile_score = 10
        
        #count up quartile stats
        for ageStat in age_stats:
            if ageStat[0] == quartile_score:
                if result == 'inc':
                    ageStat[1] += 1
                if result == 'dec':
                    ageStat[2] += 1
                if result == 'null':
                    ageStat[3] += 1
                    
        #count up percentile stats
        for agePStat in age_pstats:
            if agePStat[0] == percentile_score:
                if result == 'inc':
                    agePStat[1] += 1
                if result == 'dec':
                    agePStat[2] += 1
                if result == 'null':
                    agePStat[3] += 1
    
    #dataframe of quartile stats
    age_totals = {'Increase': [ageStat[1] for ageStat in age_stats], 
                'Decrease': [ageStat[2] for ageStat in age_stats], 
                'Null': [ageStat[3] for ageStat in age_stats]}        
    df_totals = pd.DataFrame(age_totals, index = ['TBI Age: 1st Quartile', 'TBI Age: 2nd Quartile', 'TBI Age: 3rd Quartile', 'TBI Age: 4th Quartile'])
    
    #dataframe of percentile stats
    age_ptotals = {'Increase': [agePStat[1] for agePStat in age_pstats], 
                'Decrease': [agePStat[2] for agePStat in age_pstats], 
                'Null': [agePStat[3] for agePStat in age_pstats]}        
    df_ptotals = pd.DataFrame(age_ptotals, index = [('TBI Age: Decile ' + str(agePStat[0])) for agePStat in age_pstats])
    
    #display percentile stats
    display(df_ptotals)
    
    return df_totals
        

def averageVolumes(vol):
    return_val = vol
    if isinstance(vol, str) and vol.strip() == 'unfound':
        return_val = 'unfound'
    elif isinstance(vol, str):
        vols_range = vol.strip().split('-')
        vols_range = list(map(float, vols_range))
        return_val =  np.mean(vols_range)
    return return_val

#investigate results by methods!
#NOTE: if eye stats aren't reported as 'open', 'closed', 'fixated', or 'unfound' they won't be recorded by this function
#NOTE: if regressions aren't reported as 'yes', 'no', 'unfound' they won't be recorded
def resultsByMethod(datalist):
    
    #combine all data into one table for simpler iteration
    singleTableList = []
    for i in range(len(datalist)):
        singleTableList.append( datalist[i] )
    
    singleTable = pd.concat(singleTableList)
    singleTable.reset_index(drop = True, inplace = True)
    
    #cleaning
    for index, row in singleTable.iterrows():
        #strip methods and results cells
        singleTable.at[index, 'RESULT'] = row['RESULT'].strip()
        singleTable.at[index, 'Eyes Open/Closed/Fixated'] = row['Eyes Open/Closed/Fixated'].strip()
        singleTable.at[index, 'Preprocessing Software'] = row['Preprocessing Software'].strip()
        singleTable.at[index, 'Global signal regression'] = row['Global signal regression'].strip()
        singleTable.at[index, 'Motion regression'] = row['Motion regression'].strip()
        singleTable.at[index, 'White matter regression'] = row['White matter regression'].strip()
        singleTable.at[index, 'CSF regression'] = row['CSF regression'].strip()
        
        #fill method info from previous line
        if row['Eyes Open/Closed/Fixated'] == "" and index - 1 >= 0:
            singleTable.at[index, 'Eyes Open/Closed/Fixated'] = singleTable.at[index-1, 'Eyes Open/Closed/Fixated']
        if row['# of volumes'] == "" and index - 1 >= 0:
            singleTable.at[index, '# of volumes'] = singleTable.at[index-1, '# of volumes']
        if row['Preprocessing Software'] == "" and index - 1 >= 0:
            singleTable.at[index, 'Preprocessing Software'] = singleTable.at[index-1, 'Preprocessing Software']
        if row['Global signal regression'] == "" and index - 1 >= 0:
            singleTable.at[index, 'Global signal regression'] = singleTable.at[index-1, 'Global signal regression']
        if row['Motion regression'] == "" and index - 1 >= 0:
            singleTable.at[index, 'Motion regression'] = singleTable.at[index-1, 'Motion regression']
        if row['White matter regression'] == "" and index - 1 >= 0:
            singleTable.at[index, 'White matter regression'] = singleTable.at[index-1, 'White matter regression']
        if row['CSF regression'] == "" and index - 1 >= 0:
            singleTable.at[index, 'CSF regression'] = singleTable.at[index-1, 'CSF regression']
    
    #can't do this if there are empty strings so wait until fill
    singleTable['# of volumes'] = singleTable['# of volumes'].map(averageVolumes)
    
   #for debugggin: display(singleTable[singleTable['# of volumes'] == 'unfound'])
    #display(singleTable['# of volumes'])
    
    
    #set up data collection for methods
    
    #eyes
    eye_stats = [['open', 0, 0, 0], ['closed', 0, 0, 0], ['fixated', 0, 0, 0], ['unfound', 0, 0, 0]]
    
    #number of volumes
    vol_stats = [['<200', 0, 0, 0], ['[200-300)', 0, 0, 0], ['[300-400)', 0, 0, 0], ['[400-500)', 0, 0, 0], ['[500+', 0, 0, 0], ['unfound', 0, 0, 0]]
    
    #preprocessing
    prep_stats = [['Mixed (Includes Custom or Generic MATLAB)', 0, 0, 0], ['AFNI', 0, 0, 0], ['FSL', 0, 0, 0],  ['SPM12', 0, 0, 0], ['DPARSF', 0, 0, 0], ['SPM8', 0, 0, 0], ['CONN', 0, 0, 0], ['FMRIB', 0, 0, 0], ['SPM5', 0, 0, 0], ['RSL', 0, 0, 0], ['unfound', 0, 0, 0]]
    
    #global regression
    greg_stats = [['yes', 0, 0, 0], ['no', 0, 0, 0], ['unfound', 0, 0, 0]]
    
    #motion regression
    mreg_stats = [['yes', 0, 0, 0], ['no', 0, 0, 0], ['unfound', 0, 0, 0]]
    
    #white matter regression
    wreg_stats = [['yes', 0, 0, 0], ['no', 0, 0, 0], ['unfound', 0, 0, 0]]
    
    #CSF regression
    csfreg_stats = [['yes', 0, 0, 0], ['no', 0, 0, 0], ['unfound', 0, 0, 0]]
        
    #counting
    for index, row in singleTable.iterrows():
        result = row['RESULT']
        
        #count up volume stats
        vol_label = ''
        
        if row['# of volumes'] == 'unfound':
            vol_label = 'unfound'
        elif float(row['# of volumes']) < 200.0:
            vol_label = '<200'
        elif float(row['# of volumes']) >= 200.0 and float(row['# of volumes']) < 300.0:
            vol_label = '[200-300)'
        elif float(row['# of volumes']) >= 300.0 and float(row['# of volumes']) < 400.0:
            vol_label = '[300-400)'
        elif float(row['# of volumes']) >= 400.0 and float(row['# of volumes']) < 500.0:
            vol_label = '[400-500)'
        elif float(row['# of volumes']) >= 500.0:
            vol_label = '[500+'
        
            
        for volStat in vol_stats:
            if volStat[0] == vol_label: 
                if result == 'inc':
                    volStat[1] += 1
                if result == 'dec':
                    volStat[2] += 1
                if result == 'null':
                    volStat[3] += 1
                    
        #count up prep stats
        found_prep = False
        for prepStat in prep_stats:
            if prepStat[0] == str(row['Preprocessing Software']):
                found_prep = True
                if result == 'inc':
                    prepStat[1] += 1
                if result == 'dec':
                    prepStat[2] += 1
                if result == 'null':
                    prepStat[3] += 1
        if found_prep == False:
            if result == 'inc':
                prep_stats[0][1] += 1
            if result == 'dec':
                prep_stats[0][2] += 1
            if result == 'null':
                prep_stats[0][3] += 1
        
        #count up eye stats
            
        for eyeStat in eye_stats:
            if eyeStat[0] == str(row['Eyes Open/Closed/Fixated']):
                if result == 'inc':
                    eyeStat[1] += 1
                if result == 'dec':
                    eyeStat[2] += 1
                if result == 'null':
                    eyeStat[3] += 1
                    
        #global reg stats
        for gregStat in greg_stats:
            if gregStat[0] == str(row['Global signal regression']):
                if result == 'inc':
                    gregStat[1] += 1
                if result == 'dec':
                    gregStat[2] += 1
                if result == 'null':
                    gregStat[3] += 1
        #motion reg stats
        for mregStat in mreg_stats:
            if mregStat[0] == str(row['Motion regression']):
                if result == 'inc':
                    mregStat[1] += 1
                if result == 'dec':
                    mregStat[2] += 1
                if result == 'null':
                    mregStat[3] += 1
                        
        #white matter reg stats
        for wregStat in wreg_stats:
            if wregStat[0] == str(row['White matter regression']):
                if result == 'inc':
                    wregStat[1] += 1
                if result == 'dec':
                    wregStat[2] += 1
                if result == 'null':
                    wregStat[3] += 1
                        
        #csf reg stats
        for csfregStat in csfreg_stats:
            if csfregStat[0] == str(row['CSF regression']):
                if result == 'inc':
                    csfregStat[1] += 1
                if result == 'dec':
                    csfregStat[2] += 1
                if result == 'null':
                    csfregStat[3] += 1
                    
    #MAKE ALL THE DATAFRAMES

    #eye
    eye_totals = {'Increase': [eyeStat[1] for eyeStat in eye_stats], 
            'Decrease': [eyeStat[2] for eyeStat in eye_stats], 
            'Null': [eyeStat[3] for eyeStat in eye_stats]}        
    df_eyetotals = pd.DataFrame(eye_totals, index = [eyeStat[0] for eyeStat in eye_stats])
    print("Eye Method Breakdown:")
    display(df_eyetotals)
    print('\n')
    
    #volumes
    vol_totals = {'Increase': [volStat[1] for volStat in vol_stats], 
            'Decrease': [volStat[2] for volStat in vol_stats], 
            'Null': [volStat[3] for volStat in vol_stats]}        
    df_voltotals = pd.DataFrame(vol_totals, index = [volStat[0] for volStat in vol_stats])
    print("# of Volumes Breakdown:")
    display(df_voltotals)
    print('\n')
    
    #preprocessing software
    prep_totals = {'Increase': [prepStat[1] for prepStat in prep_stats], 
            'Decrease': [prepStat[2] for prepStat in prep_stats], 
            'Null': [prepStat[3] for prepStat in prep_stats]}        
    df_preptotals = pd.DataFrame(prep_totals, index = [prepStat[0] for prepStat in prep_stats])
    print("Preprocessing Software Breakdown:")
    display(df_preptotals)
    print('\n')
    
    #global reg
    greg_totals = {'Increase': [gregStat[1] for gregStat in greg_stats], 
            'Decrease': [gregStat[2] for gregStat in greg_stats], 
            'Null': [gregStat[3] for gregStat in greg_stats]}        
    df_gregtotals = pd.DataFrame(greg_totals, index = [gregStat[0] for gregStat in greg_stats])
    print("Global Regression Breakdown:")
    display(df_gregtotals)
    print('\n')
    
    #motion reg
    mreg_totals = {'Increase': [mregStat[1] for mregStat in mreg_stats], 
            'Decrease': [mregStat[2] for mregStat in mreg_stats], 
            'Null': [mregStat[3] for mregStat in mreg_stats]}        
    df_mregtotals = pd.DataFrame(mreg_totals, index = [mregStat[0] for mregStat in mreg_stats])
    print("Motion Regression Breakdown:")
    display(df_mregtotals)
    print('\n')
    
    #white matter reg
    wreg_totals = {'Increase': [wregStat[1] for wregStat in wreg_stats], 
            'Decrease': [wregStat[2] for wregStat in wreg_stats], 
            'Null': [wregStat[3] for wregStat in wreg_stats]}        
    df_wregtotals = pd.DataFrame(wreg_totals, index = [wregStat[0] for wregStat in wreg_stats])
    print("White Matter Regression Breakdown:")
    display(df_wregtotals)
    print('\n')
    
    #csf reg
    csfreg_totals = {'Increase': [csfregStat[1] for csfregStat in csfreg_stats], 
            'Decrease': [csfregStat[2] for csfregStat in csfreg_stats], 
            'Null': [csfregStat[3] for csfregStat in csfreg_stats]}        
    df_csfregtotals = pd.DataFrame(csfreg_totals, index = [csfregStat[0] for csfregStat in csfreg_stats])
    print("CSF Regression Breakdown:")
    display(df_csfregtotals)
    print('\n')
    
    
    #MAKE DURATION DATAFRAME-------- tried some fancy sh- (ahem) stuff here from my Data Science class
    data_single = pd.concat(datalist)
    data_single = data_single.loc[:, ['RESULT', 'WITHIN NETWORK FINDINGS', 'Duration of scan (s)']]
    #replace whitespace with nan so i can forward fill (ffill)
    data_single = data_single.replace(r'^\s*$', np.NaN, regex=True)
    data_single['WITHIN NETWORK FINDINGS'] = data_single['WITHIN NETWORK FINDINGS'].ffill()
    data_single['Duration of scan (s)'] = data_single['Duration of scan (s)'].ffill()
    
    #grab unfound stuff to deal with separately
    data_unfound = data_single[data_single['Duration of scan (s)'] == "unfound"]
    
    data_single = data_single[data_single['Duration of scan (s)'] != "unfound"]
    data_single = data_single.astype({'Duration of scan (s)': 'int64'})
    data_single = data_single.loc[:, ['RESULT', 'Duration of scan (s)']].sort_values(by = ['Duration of scan (s)'])
    
    #form a dictionary of inc, dec, null results for each scanning duration
    res_dict = {}
    for name, group in data_single.groupby('Duration of scan (s)'):
        #display(group)
        if 'inc' in group['RESULT'].values:
            res_dict[str(name) + '_inc'] = group['RESULT'].value_counts()['inc']
        else:
            res_dict[str(name) + '_inc'] = 0
        if 'dec' in group['RESULT'].values:
            res_dict[str(name) + '_dec'] = group['RESULT'].value_counts()['dec']
        else:
            res_dict[str(name) + '_dec'] = 0
        if 'null' in group['RESULT'].values:
            res_dict[str(name) + '_null'] = group['RESULT'].value_counts()['null']
        else: 
            res_dict[str(name) + '_null'] = 0

    #full groupby output for checking:
    #for name, group in data_single.groupby('Duration of scan (s)'):
        #print(name)
        #print(group)
        #print ('\nStatistics: ')
        #print(group['RESULT'].value_counts())
        #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

    #Passed check!!

    inc_dur_list = []
    dec_dur_list = []
    null_dur_list = []

    for key,value in res_dict.items():
        if 'inc' in key:
            inc_dur_list.append(value)
        elif 'dec' in key:
            dec_dur_list.append(value)
        elif 'null' in key:
            null_dur_list.append(value)

    #append 'unfound' categorical results
    inc_dur_list.append(data_unfound['RESULT'].value_counts()['inc'])
    dec_dur_list.append(data_unfound['RESULT'].value_counts()['dec'])
    null_dur_list.append(data_unfound['RESULT'].value_counts()['null'])
    
    #Make results by duration dataframe:
    res_duration = {"Increase": inc_dur_list,
                   'Decrease': dec_dur_list,
                   "Null": null_dur_list}

    index_dur = [name for name, group in data_single.groupby('Duration of scan (s)')]
    index_dur.append('unfound')
    
    data_duration = pd.DataFrame(res_duration, index = index_dur)
    print('Scan Duration (Seconds) Breakdown: ')
    display(data_duration)
    print('\n')
    
    return
#end resultsByMethod() function--------------------------------------------------------------------------------


#investigate results by methods using quartiles where applicable!
def resultsByMethodQuartiles(datalist):
    
    #combine all data into one table for simpler iteration
    singleTableList = []
    for i in range(len(datalist)):
        singleTableList.append( datalist[i] )
    
    singleTable = pd.concat(singleTableList)
    singleTable.reset_index(drop = True, inplace = True)
    
    #cleaning
    for index, row in singleTable.iterrows():
        #strip methods and results cells
        singleTable.at[index, 'RESULT'] = row['RESULT'].strip()
        
        #fill method info from previous line
        if row['# of volumes'] == "" and index - 1 >= 0:
            singleTable.at[index, '# of volumes'] = singleTable.at[index-1, '# of volumes']
    
    #can't do this if there are empty strings so wait until fill
    singleTable['# of volumes'] = singleTable['# of volumes'].map(averageVolumes)
    
    #data collection
    #set up with quartiles
    
    vols = singleTable['# of volumes'].tolist()
    valueToBeRemoved = 'unfound'

    filt = filter(lambda val: val !=  valueToBeRemoved, vols) 
    vols = list(filt)
    
    #unhash to check all the volumes in the data
    #print(vols)
    
    quartile_1 = np.percentile(vols, 25)
    quartile_2 = np.percentile(vols, 50)
    quartile_3 = np.percentile(vols, 75)
    
    #number of volumes
    vol_stats = [[f"Quartile 1: 0-{quartile_1}]", 0, 0, 0], [f"Quartile 2: {quartile_1}-{quartile_2}]", 0, 0, 0], [f"Quartile 3: {quartile_2}-{quartile_3}]", 0, 0, 0], [f"Quartile 4: {quartile_3}+", 0, 0, 0], ['unfound', 0, 0, 0]]
        
    #counting
    for index, row in singleTable.iterrows():
        result = row['RESULT']
        
        #count up volume stats
        vol_label = ''
        
        if row['# of volumes'] == 'unfound':
            vol_label = 'unfound'
        elif float(row['# of volumes']) <= quartile_1:
            vol_label = f"Quartile 1: 0-{quartile_1}]"
        elif float(row['# of volumes']) > quartile_1 and float(row['# of volumes']) <= quartile_2:
            vol_label = f"Quartile 2: {quartile_1}-{quartile_2}]"
        elif float(row['# of volumes']) > quartile_2 and float(row['# of volumes']) <= quartile_3:
            vol_label = f"Quartile 3: {quartile_2}-{quartile_3}]"
        elif float(row['# of volumes']) > quartile_3:
            vol_label = f"Quartile 4: {quartile_3}+"
        
            
        for volStat in vol_stats:
            if volStat[0] == vol_label: 
                if result == 'inc':
                    volStat[1] += 1
                if result == 'dec':
                    volStat[2] += 1
                if result == 'null':
                    volStat[3] += 1
                    
    #MAKE DATAFRAMME
    #volumes
    vol_totals = {'Increase': [volStat[1] for volStat in vol_stats], 
            'Decrease': [volStat[2] for volStat in vol_stats], 
            'Null': [volStat[3] for volStat in vol_stats]}        
    df_voltotals = pd.DataFrame(vol_totals, index = [volStat[0] for volStat in vol_stats])
    print("# of Volumes Breakdown (Quartiles):")
    display(df_voltotals)
    print('\n')
    
    
    #MAKE DURATION DATAFRAME-------- tried some fancy groupby sh- (ahem) stuff here from my Data Science class
    data_single = pd.concat(datalist)
    data_single = data_single.loc[:, ['RESULT', 'WITHIN NETWORK FINDINGS', 'Duration of scan (s)']]
    #replace whitespace with nan so i can forward fill (ffill)
    data_single = data_single.replace(r'^\s*$', np.NaN, regex=True)
    data_single['WITHIN NETWORK FINDINGS'] = data_single['WITHIN NETWORK FINDINGS'].ffill()
    data_single['Duration of scan (s)'] = data_single['Duration of scan (s)'].ffill()
    
    #grab unfound stuff to deal with separately
    #data_unfound = data_single[data_single['Duration of scan (s)'] == "unfound"]
    data_single_num = data_single[data_single['Duration of scan (s)'] != "unfound"]
    data_single_num = data_single_num.astype({'Duration of scan (s)': 'int64'})
    data_single_num = data_single_num.loc[:, ['RESULT', 'Duration of scan (s)']].sort_values(by = ['Duration of scan (s)'])
    
    durations = data_single_num['Duration of scan (s)'].tolist()
    quartile_1 = np.percentile(durations, 25)
    quartile_2 = np.percentile(durations, 50)
    quartile_3 = np.percentile(durations, 75)
    
    #duration stat counting
    dur_stats = [[f"Quartile 1: 0-{quartile_1}]", 0, 0, 0], [f"Quartile 2: {quartile_1}-{quartile_2}]", 0, 0, 0], [f"Quartile 3: {quartile_2}-{quartile_3}]", 0, 0, 0], [f"Quartile 4: {quartile_3}+", 0, 0, 0], ['unfound', 0, 0, 0]]
    
    #counting
    for index, row in data_single.iterrows():
        result = row['RESULT']
        
        #count up duration stats
        dur_label = ''
        
        if row['Duration of scan (s)'] == 'unfound':
            dur_label = 'unfound'
        elif float(row['Duration of scan (s)']) <= quartile_1:
            dur_label = f"Quartile 1: 0-{quartile_1}]"
        elif float(row['Duration of scan (s)']) > quartile_1 and float(row['Duration of scan (s)']) <= quartile_2:
            dur_label = f"Quartile 2: {quartile_1}-{quartile_2}]"
        elif float(row['Duration of scan (s)']) > quartile_2 and float(row['Duration of scan (s)']) <= quartile_3:
            dur_label = f"Quartile 3: {quartile_2}-{quartile_3}]"
        elif float(row['Duration of scan (s)']) > quartile_3:
            dur_label = f"Quartile 4: {quartile_3}+"
        
            
        for durStat in dur_stats:
            if durStat[0] == dur_label: 
                if result == 'inc':
                    durStat[1] += 1
                if result == 'dec':
                    durStat[2] += 1
                if result == 'null':
                    durStat[3] += 1
                    
    #MAKE DATAFRAMME
    dur_totals = {'Increase': [durStat[1] for durStat in dur_stats], 
            'Decrease': [durStat[2] for durStat in dur_stats], 
            'Null': [durStat[3] for durStat in dur_stats]}        
    df_durtotals = pd.DataFrame(dur_totals, index = [durStat[0] for durStat in dur_stats])
    print("Scan Duration (s) Breakdown (Quartiles):")
    display(df_durtotals)
    print('\n')
    
    
    
    return
#end resultsByMethodQuartiles() function--------------------------------------------------------------------------------