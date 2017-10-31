import sys
import io
from collections import defaultdict
from numpy import median

# Opening the file and parsing and splitting the data ------------------------------------------------------------------
with io.open(sys.argv[1], 'r', encoding='latin-1') as infile:
    # We don't have to infile.close() using 'with'
    # Need to use encoding = latin-1, otherwise file will be opened with our OS dependent system default codec
    # Common ones are Latin-1 and UTF-8

    noOfRows = 0  # Just for counting
    noOfRowsForZip = -1  # To prevent index out of bound for the last entry
    noOfRowsForDate = -1

    # Opening files to write
    my_file_zip = open(sys.argv[2], "w")
    my_file_date = open(sys.argv[3], "w")

    # Declare lists for Zip purpose
    list_of_CMTE_ID = []
    list_of_ZIP_CODE = []
    list_of_TRANSACTION_DT = []
    list_of_TRANSACTION_AMT = []

    # Declare lists for Date purpose
    list_of_CMTE_ID_date = []
    list_of_ZIP_CODE_date = []
    list_of_TRANSACTION_DT_date = []
    list_of_TRANSACTION_AMT_date = []

    # Declare  dictionaries for Zip purpose
    dictOfZipTotalNoOfTransaction = {}
    dictOfZipTotalAmountOfTransaction = {}
    dictOfZipForTransactionAmountRunningMedian = defaultdict(list)  # we need to append more members to a dict

    # Declare  dictionaries for date purpose
    dictOfDateTotalNoOfTransaction = {}
    dictOfDateTotalAmountOfTransaction = {}
    dictOfDateForTransactionAmountMedian = defaultdict(list)

    for line in infile:    # looping through the lines
        noOfRows += 1   # keeping track of no of entries
        line = line.strip()    # remove all the leading and trailing spaces

        # Splitting the line into required data members
        splittedForm = line.split('|')
        CMTE_ID = splittedForm[0]  # recipient of this contribution
        ZIP_CODE = splittedForm[10]  # this Zip code may have more than 5 chars (9 chars). We will deal with it later
        TRANSACTION_DT = splittedForm[13]
        TRANSACTION_AMT = splittedForm[14]
        OTHER_ID = splittedForm[15]

        if OTHER_ID == '' and CMTE_ID != '' and TRANSACTION_AMT != '':

            # Running Median by Zip ====================================================================================
            if len(ZIP_CODE) >= 5:  # invalid if empty or less than 5 char
                ZIP_CODE = ZIP_CODE[:5]  # we only want the first five digits
                noOfRowsForZip += 1

                # Appending the relevant data members in the list
                list_of_CMTE_ID.append(CMTE_ID)
                list_of_ZIP_CODE.append(ZIP_CODE)
                list_of_TRANSACTION_DT.append(TRANSACTION_DT)
                list_of_TRANSACTION_AMT.append(TRANSACTION_AMT)

                # Total number of transactions to a dictionary
                try:
                    dictOfZipTotalNoOfTransaction[list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]] += 1
                except KeyError:
                    dictOfZipTotalNoOfTransaction[list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]] = 1

                # Transaction total amount to a dictionary
                # Also appending amounts for the running median
                try:
                    dictOfZipTotalAmountOfTransaction[list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]] += int(list_of_TRANSACTION_AMT[noOfRowsForZip])
                    dictOfZipForTransactionAmountRunningMedian[
                        list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]].append(int(
                        list_of_TRANSACTION_AMT[noOfRowsForZip]))

                except KeyError:
                    dictOfZipTotalAmountOfTransaction[list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]] = int(list_of_TRANSACTION_AMT[noOfRowsForZip])
                    dictOfZipForTransactionAmountRunningMedian[
                        list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]].append(int(
                        list_of_TRANSACTION_AMT[noOfRowsForZip]))

                #  Running median to a dictionary
                # int will truncate '.0' of 2.0
                runningMedian = int(round(median(dictOfZipForTransactionAmountRunningMedian[list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]])))
                # print runningMedian

                # Printing to Check
                # print list_of_CMTE_ID[noOfRowsForZip] + '|' + list_of_ZIP_CODE[noOfRowsForZip] + '|' + \
                #       str(runningMedian) + '|' + \
                #       str(dictOfZipTotalNoOfTransaction[list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]]) + '|' + \
                #       str(dictOfZipTotalAmountOfTransaction[list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]])

                # Writing the results to the text file for medianvals_by_zip.txt
                my_file_zip.write(list_of_CMTE_ID[noOfRowsForZip] + '|' + list_of_ZIP_CODE[noOfRowsForZip] + '|' + \
                      str(runningMedian) + '|' + \
                      str(dictOfZipTotalNoOfTransaction[
                              list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]]) + '|' + \
                      str(dictOfZipTotalAmountOfTransaction[
                              list_of_CMTE_ID[noOfRowsForZip], list_of_ZIP_CODE[noOfRowsForZip]]) +'\n')
                # Done with Running Median by Zip ======================================================================

                # Median by Date =======================================================================================
                if len(TRANSACTION_DT) == 8:  # should not be empty and malformed
                    noOfRowsForDate += 1

                    # To yyyymmdd format from original mmddyyyy so that alphabetical sorting becomes easy
                    TRANSACTION_DT = TRANSACTION_DT[4:8] + TRANSACTION_DT[0:2] + TRANSACTION_DT[2:4]

                    # Appending the relevant data members in the list
                    list_of_CMTE_ID_date.append(CMTE_ID)
                    list_of_ZIP_CODE_date.append(ZIP_CODE)
                    list_of_TRANSACTION_DT_date.append(TRANSACTION_DT)
                    list_of_TRANSACTION_AMT_date.append(TRANSACTION_AMT)

                    # Total number of transactions to a dictionary
                    try:
                        dictOfDateTotalNoOfTransaction[
                            list_of_CMTE_ID_date[noOfRowsForDate], list_of_TRANSACTION_DT_date[noOfRowsForDate]] += 1
                    except KeyError:
                        dictOfDateTotalNoOfTransaction[
                            list_of_CMTE_ID_date[noOfRowsForDate], list_of_TRANSACTION_DT_date[noOfRowsForDate]] = 1

                    # Transaction total amount to a dictionary
                    # Also appending amounts for the  median
                    try:
                        dictOfDateTotalAmountOfTransaction[
                            list_of_CMTE_ID_date[noOfRowsForDate], list_of_TRANSACTION_DT_date[noOfRowsForDate]] += int(
                            list_of_TRANSACTION_AMT_date[noOfRowsForDate])
                        dictOfDateForTransactionAmountMedian[
                            list_of_CMTE_ID_date[noOfRowsForDate], list_of_TRANSACTION_DT_date[noOfRowsForDate]].append(int(
                            list_of_TRANSACTION_AMT_date[noOfRowsForDate]))

                    except KeyError:
                        dictOfDateTotalAmountOfTransaction[
                            list_of_CMTE_ID_date[noOfRowsForDate], list_of_TRANSACTION_DT_date[noOfRowsForDate]] = int(
                            list_of_TRANSACTION_AMT_date[noOfRowsForDate])
                        dictOfDateForTransactionAmountMedian[
                            list_of_CMTE_ID_date[noOfRowsForDate], list_of_TRANSACTION_DT_date[noOfRowsForDate]].append(int(
                            list_of_TRANSACTION_AMT_date[noOfRowsForDate]))

    # Sorting, post processing, printing to check and writing to the file
    # (k[0][0], k[0][1]) = recipient ID and date respectively, two keys of our dictionary
    # k[1] = value of our dictionary
    for key, value in sorted(dictOfDateTotalAmountOfTransaction.iteritems(), key=lambda k: (k[0][0], k[0][1])):
        medianByDate = int(round(median(dictOfDateForTransactionAmountMedian[key])))
        # Back to mmddyyyy  format from yyyymmdd which was done for sorting
        date = key[1]  # since we cannot slice the tuple member
        date = date[4:6] + date[6:8] + date[0:4]
        #print key[0] + '|' + date + '|' + '|' + str(medianByDate) + '|' + str(dictOfDateTotalNoOfTransaction[key]) + '|' + str(value)

        # Writing the results to the text file for medianvals_by_date.txt
        my_file_date.write(key[0] + '|' + date + '|' + str(medianByDate) + '|' + str(dictOfDateTotalNoOfTransaction[key]) + '|' + str(value) + '\n')
        # Done with Running Median by Date =============================================================================
    print ('Done')



































