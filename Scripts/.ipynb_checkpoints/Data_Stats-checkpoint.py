
import pandas as pd

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
def runStats(datalist, stats, dataOrder):
    for i in range(len(datalist)):
        for index, row in datalist[i].iterrows():
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
            
            for stat in stats:
                if stat[0] == classif:
                    stat[1] += 1
                    if row['TBI (n)'] != "//ERROR//":
                        stat[2] += int(row['TBI (n)'])
                    if row['TBI (n)'] != "//ERROR//" and row['HC (n)'] != "//ERROR//":
                        stat[3] += ( int(row['TBI (n)']) + int(row['HC (n)']) )           


#end runStats() function----------------------------------------------------------------------------------------------------------------------------




#queryStats() function----------------------------------------------------------------------------------------------------------------------------
#queryStats(stats, weight = "UW", query1="", query2="", query3="", query4="", query5="", query6=""): queryStats() allows you to input a stats 2D list 
#(presumably resulting from runStats), as well as 0 to 6 queries (a query is a string matching a possible type of result such as "dmn" for 
#default mode network results, etc.) and outputs a list of [increase decrease null] results, in that order. This function is integral to printStats.
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
        if "dec" in stat[0] and query1 in stat[0] and query2 in stat[0] and query3 in stat[0] \
            and query4 in stat[0] and query5 in stat[0] and query6 in stat[0]:
                if weight == "UW":
                    count_dec += stat[1]
                elif weight == "W-TBI":
                    count_dec += stat[2]
                elif weight == "W-Total":
                    count_dec += stat[3]
        if "null" in stat[0] and query1 in stat[0] and query2 in stat[0] and query3 in stat[0] \
            and query4 in stat[0] and query5 in stat[0] and query6 in stat[0]:
                if weight == "UW":
                    count_null += stat[1]
                elif weight == "W-TBI":
                    count_null += stat[2]
                elif weight == "W-Total":
                    count_null += stat[3]
    return [count_inc, count_dec, count_null]
#end queryStats() function----------------------------------------------------------------------------------------------------------------------------



#easyQueryStats function--------------------------------------------------------------------------------------------------
#easyQueryStats() works exactly like queryStats except it prints out a mini dataframe 
#of your requested statistics, making it easier to use without additional coding.
#As of 08/11/2021, you also have to provide a weighting type for your results as the second parameter.
#"UW"- unweighted results
#"W-TBI" TBI sample size weighted results
#"W-Total" Total sample size weighted results

def easyQueryStats(stats, weight = "UW", query1="", query2="", query3="", query4="", query5="", query6=""):
    queryList = [query1, query2, query3, query4, query5, query6]
    queryList = [query for query in queryList if not query == ""]
    if(any(query not in nets+results+severities+ages+chronicities+types+controls for query in queryList)):
        print("One of more of your queries did not correspond to a valid keyword. Double check your input!")
        return
    
    if weight not in ["UW", "W-TBI", "W-Total"]:
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
