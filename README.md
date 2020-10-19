# Insight Coding Challenge - Data Engineering - Oct 2020

## Problem Statement

In this problem, population information is provided at the tract level which are “small areas that average 4,000 inhabitants”. The goal of this program is to provide a rolled up view of the population information at the core area level which is defined as “a set of communities, often with a population center and shared economic and social ties” and are essentially larger areas comprising of several tracts. 

## Solution

To solve the problem of rolling up population information at the core area level two classes are used in the _population_rollup.py_ script and this arrangement is used for scalability of the solution.  The first class **Core_Area** tracks population information at the core area level such as the area’s population in 2000 and 2010, the number of tracts in the area and the average population percent change between 2000 and 2010. The second class **Core_Area_Process** processes the population information input file at the tract level and rollups the information to provide a view at the core area level. 

It does this:

1. by tracking the core area information in a dictionary data structure with the core area code and core area title pair serving as the unique identifier.

2.	reading the input file line by line to bypass any memory issues arising from larger files and separating the fields into their respective variables and checking for missing values. 

3. checking if the unique identifier is present in the core area dictionary keys. If it does, then the core areas tract count is incremented by one and the populations for 2000 and 2010 and the tracts population percent change is appended to the respective lists of their attributes, else a core are object is instantiated with the derived information. 

4. feeding the core area dictionary into the method of the processing class to save as a csv file. 

## Running the Program

To run the program type 
```
./run.sh
```
And to run the test program type, and compare report.csv with report2.csv
```
./run_test.sh
```
## Output

The output file which presents the rolled up view at the core area level contains the following fields:

1.	Core area code

2.	Core area title

3.	Number of tracts in the core area

4.	Total 2000 population of the core area

5.	Total 2010 population of the core area

6.	Average population change for the core area between 2000 and 2010


