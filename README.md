# Find Political Donors # 
https://github.com/InsightDataScience/find-political-donors </br>
This program simulates a real-time platform that identifies and analyzes possible donors for upcoming election campaign. 
# Data Structure # 
The data structure used are lists and dictionaries. Key of our dictionary is a tuple - unique combination of CMTE_ID & ZIP_CODE and CMTE_ID & TRANSACTION_DATE. Value of our dictionary are running median/median, total dollar amount and total number of contributions.
# Algorithm # 
It reads input file, parses through each line and reads relevant fields CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT and OTHER_ID. </br>
In the orginal loop, it calculates running median, total dollar amount and total number of contributions by recipient and zip code. This is continuosly being logged in medianvals_by_zip.txt file. </br>
In the same loop, it calculates total dollar amount and total number of contributions by recipient and date. Corresponding amount is being appended as a list. Since we have to calcualte just a median and not the running median in second case, after we are done with this loop, median is calcualted by recipient and date. This is logged in medianvals_by_date.txt file.</br>
# Requires Python 2.7 and following dependencies: # 
import sys <br />
import io <br />
from collections import defaultdict <br />
from numpy import median <br /> 
# Test cases : # 
Multiple test cases were made and tested against the manually verified results.
1. OTHER_ID not empty <br />
2. Malformed and/or empty TRANSACTION_DT with good ZIP_CODE <br />
3. Fewer than 5 digits and/or empty ZIP_CODE with good TRANSACTION_DT <br />
4. CMTE_ID empty <br />
5. TRANSACTION_AMT empty </br>
6. Various combinations of above test cases
