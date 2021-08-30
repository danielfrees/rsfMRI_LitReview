![Literature Review Toolkit rsfMRI in TBI](https://user-images.githubusercontent.com/72712014/131385098-8b9abcac-c958-4ae3-a35b-5946b7cdfdf3.png)

![GitHub last commit](https://img.shields.io/github/last-commit/danielfrees/rsfMRI_LitReview?style=plastic)

## Purpose

These scripts were written by Daniel Frees, an undergraduate in the UCLA BrainSPORT Lab, for the analysis of resting state functional MRI literature on traumatic brain injury patients. A number of scripts are included for cleaning raw data, and others for performing statistical analysis.

## Important Setup

Data_Investigation_LR.ipynb has the correct workflow set up. Directories to CSV files must be stated in the Directory() object, and order of uploads (which upload was which network) must be stated as well. Then the workflow is:

1) run data through cleanData() function
2) run sampleDist() to determine sample size info
3) Calculate quartiles of sample size data 
4) set up classifications and stats array
5) use runStats() to count up all the data for each specific classification
6) use printStats() with desired weightings to auto-query for a ton of subpopulations of data
7) use easyQueryStats() or queryStats() as desired to investigate other more specific subpopulations of data for any weighting desired


## Cleaning Functions

```python
cleanData(datalist)
```
cleanData() takes in a list of pandas dataframes (these are generated in my code shortly below the directory inputs), and outputs clean dataframes for the columns relevant to our analysis. I used natural language processing (NLP) to determine what our final verdict for each result/classification was, and then edited the output list of dataframes accordingly. 

•Rules: the final determined Result (for increase, decrease or null connectivity) must be written leftmost in its cell in the input dataframe. Results and Chronicities must be listed for each finding, but other classifications will autofill down wherever they have not been filled in (as we typically only wrote these out for the first finding of a given paper). Certain mispellings and miscapitalizations are allowed, but I did not write a full Trie or other spellchecker, so try to avoid typos as much as possible. I made sure through multiple iterations that this was catching all of our most common mispellings/ miscaps.

```python
smallTable(datalist)
```
smallTable() takes in cleaned data (run through cleanData() first), and then outputs a dataframe detailing the most important information for each paper, summarized across all comparisons that any given paper may have made. 

## Stat Functions

```python
runStats(datalist, stats, dataOrder, quartiles)
```
runStats() takes in a list of pandas dataframes (these should be the cleaned ones output from cleanData()) as well as a 2D 'stats' list (a list of size 2 lists, where each size 2 list is a pair: a classification, and a count of how many times that classification shows up in the data (this should start at 0 for all classifications the same way I initially set up my stats object). It outputs a modified 2D 'stats' list with the counts added up for each classification after parsing through the provided datalist.

-Must input the order of data in datalist (ie: which network is which)

-Must also input quartiles so that quartile weighted results can be run

•Rules: Mostly just be careful to pass a stats 2D list which has counts of 0 for everything if you want an accurate analysis of the dataframes you passed in. Furthermore, generating the stats object is performed immediately about this function definition in my code, and could be altered for an alternate classification system. 

```python
queryStats(stats, weight = "UW", query1="", query2="", query3="", query4="", query5="", query6="")
```
queryStats() allows you to input a stats 2D list (presumably resulting from runStats), as well as 0 or more queries (a query is a string matching a possible type of result such as "dmn" for default mode network results, etc.) and outputs a list of [increase decrease null] results, in that order. This function is integral to printStats.

The only additional thing you need to do compared to the pre-08/11/2021 code is provide a weighting option as your second parameter:
"UW" - uses unweighted results;
"W-TBI" - uses TBI sample size weighted results;
"W-Total" - uses Total sample size weighted results
"Quartiles" - uses Quartile scored weighted results

```python
printStats(stats)
```
printStats() uses queryStats to generate a bunch of pandas dataframes corresponding to relevant outputs for our literature review, making visualization of a ton of different subsections of our results easy and clear.

```python
easyQueryStats(stats, weight = "UW", query1="", query2="", query3="", query4="", query5="", query6="")
```
easyQueryStats() works almost exactly like queryStats except it prints out a mini dataframe of your requested statistics, making it easier to use without additional coding. 
Weights:
"UW" - uses unweighted results;
"W-TBI" - uses TBI sample size weighted results;
"W-Total" - uses Total sample size weighted results
"Quartiles" - uses Quartile scored weighted results

•**This is the function to use if you want to investigate the data in the easiest way possible.** Simply go into a new cell and call the function away. An example has been provided in the bottom-most codeblock in this notebook

•Note that if you hop on the notebook and only want to use this function you will still need to run each of the preceding code blocks in order, so that the necessary stats object will be created for you.

Classifications which can be used as query keywords: 

nets = ["dmn", "ecn", "limb", "sn", "dan", "van", "vis", "smn"]

results = ["inc", "dec", "null"]

severities = ["mild", "m/mod", "moderate", "mod/sev", "severe", "mix severity", "No Severity"]

ages = ["child", "adolescent", "adult", "mix age", "No Age"]

chronicities = ["Acute", "ac/subac", "subacute", "subac/chron", "chronic", "repsub", "mix cnicity", "No Cnicity"]

types = ["sport", "military", "civilian", "mix Type"]

controls = ["HC", "ISC", "NCC", "TBI+", "Mood", "Other Control"]

```python
sampleDist(datalist)
```
The sampleDist function produces a distribution of TBI and Total Sample Sizes on a per-paper basis (each paper gets one entry), using a cleaned spreadsheet input. Input should ideally come from data which has gone through cleanData().

```python
numAuthors(data)
```
- intended for use on the output of smallTable()
- prints the number of unique authors in a dataframe
- requires that author names are followed by either a 1, 2, (, or #

## Questions/ Alternate Usage

If you wish to use or modify this code for a similar project, email danielfreess@g.ucla.edu with any questions. 
