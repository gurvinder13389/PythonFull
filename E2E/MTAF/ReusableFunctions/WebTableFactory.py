from MTAF.ReusableFunctions import globalVar, reportFact, selenium_driver
from selenium.webdriver import ActionChains
import time

class WebTableFactory:
    # Function will return n rows
    def get_row_count(self, weTable):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                return len(weTable.find_elements_by_tag_name("tr"))
            except Exception as ex:
                print('Row count for web table ' + weTable + ' cannot be fetched. ' + str(ex))
                reportFact.AddSteps(
                    'Row count for web table ' + weTable + ' should be fetched. ',
                    'Row count for web table ' + weTable + ' cannot be fetched. ',
                    strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    # Function will return n columns
    def get_column_count(self, weTable):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                return len(weTable.find_elements_by_xpath("//tr[2]/td"))
            except Exception as ex:
                print('Column count for web table ' + weTable + ' cannot be fetched. ' + str(ex))
                reportFact.AddSteps(
                    'Column count for web table ' + weTable + ' should be fetched. ',
                    'Column count for web table ' + weTable + ' cannot be fetched. ',
                    strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    # User should pass column number(1 onwards) and row number (iStartRow)(1 onwards) along with data to compare
    # and function will return the matched row number. It will return 0 if data not found.
    def getRowNumOnColumnDataCompare(self, weTable, iColumnNumber, strDataToCompare, searchFormat='ascending', iStartRow=0):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                iRowCount = self.get_row_count(weTable)

                lstRows = weTable.find_elements_by_tag_name("tr")
                iRowFound = 0
                if iStartRow > 0:
                    iStartRow = iStartRow - 1

                if searchFormat == 'ascending':
                    start = iStartRow
                    stop = iRowCount
                    step = 1
                else:
                    start = iRowCount
                    stop = iStartRow
                    step = -1

                for iRow in range(start, stop, step):
                    weRow = lstRows[iRow]
                    if (len(weRow.find_elements_by_tag_name("td")) > 0):
                        strActualData = weRow.find_elements_by_tag_name("td")[int(iColumnNumber) - 1].text
                        if strDataToCompare == strActualData:
                            iRowFound = iRow + 1
                            break
                return iRowFound
            except Exception as ex:
                print(
                    'Row number for web table ' + weTable + ' cannot be fetched for column data compare at column ' + iColumnNumber + '. ' + str(
                        ex))
                reportFact.AddSteps(
                    'Row number for web table ' + weTable + ' should be fetched for column data compare at column ' + iColumnNumber + '. ',
                    'Row number for web table ' + weTable + ' cannot be fetched for column data compare at column ' + iColumnNumber + '. ',
                    strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    # User should pass column number(1 onwards) and row number (iStartRow)(1 onwards) along with data to compare
    # and function will return the matched row number. It will return 0 if data not found.
    def getRowNumOnMultiColumnDataCompare(self, weTable, csvLstColumn, csvLstRowDataToCompare, searchFormat='ascending', iStartRow=0):
        if not globalVar.bln_SkipTestCase:
            try:
                csvLstRowData = ''
                for val in csvLstRowDataToCompare:
                    csvLstRowData = csvLstRowData + ',' + val
                csvLstRowData = csvLstRowData[1:]

                lstRows = weTable.find_elements_by_tag_name('tr')
                #iRowCount = self.get_row_count(weTable) - 1
                iRowCount = self.get_row_count(weTable)
                iRowFound = 0
                if iStartRow > 0:
                    iStartRow = iStartRow - 1

                if searchFormat == 'ascending':
                    start = iStartRow
                    stop = iRowCount
                    step = 1
                else:
                    start = iRowCount - 1
                    stop = iStartRow
                    step = -1

                for iRow in range(start, stop, step):
                    weRow = lstRows[iRow]
                    strActualData = ""
                    if (len(weRow.find_elements_by_tag_name("td")) > 0):
                        for iCol in csvLstColumn:
                            strActualData = strActualData + "," + weRow.find_elements_by_tag_name("td")[int(iCol) - 1].text.strip()
                        strActualData = strActualData[1:]

                    if strActualData.strip() == csvLstRowData.strip():
                        iRowFound = iRow + 1
                        break
                return iRowFound
            except Exception as ex:
                print(
                    'Row number for web table ' + str(weTable) + ' cannot be fetched for column data data compare')
                reportFact.AddSteps(
                    'Row number for web table ' + weTable + ' should be fetched for column data compare.',
                    'Row number for web table ' + weTable + ' cannot be fetched for column data compare. ',
                    strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    # Get table data on passing row number (1 onwards) and column number(1 onwards)
    def getCellData(self, weTable, iRow, iCol):
        if not globalVar.bln_SkipTestCase:
            try:
                if iRow > 0:
                    time.sleep(globalVar.MTAFDelay)
                    return weTable.find_elements_by_tag_name("tr")[int(iRow) - 1].find_elements_by_tag_name("td")[
                    int(iCol) - 1].text
            except Exception as ex:
                print(
                    'Cell data for web table ' + weTable + ' at row ' + iRow + ' and column ' + iCol + ' cannot be fetched. ' + str(
                        ex))
                reportFact.AddSteps(
                    'Cell data for web table ' + weTable + ' at row ' + iRow + ' and column ' + iCol + ' should be fetched. ',
                    'Cell data for web table ' + weTable + ' at row ' + iRow + ' and column ' + iCol + ' cannot be fetched. ',
                    strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    # Click table cell on passing row number (1 onwards) and column number(1 onwards)
    def clickCell(self, weTable, iRow, iCol):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                weTable.find_elements_by_tag_name("tr")[int(iRow) - 1].find_elements_by_tag_name("td")[
                    int(iCol) - 1].click()
            except Exception as ex:
                print(
                    'Cell data for web table ' + weTable + ' at row ' + iRow + ' and column ' + iCol + ' cannot be clicked. ' + str(
                        ex))
                reportFact.AddSteps(
                    'Cell data for web table ' + weTable + ' at row ' + iRow + ' and column ' + iCol + ' should be clicked. ',
                    'Cell data for web table ' + weTable + ' at row ' + iRow + ' and column ' + iCol + ' cannot be clicked. ',
                    strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    # Double Click table cell on passing row number (1 onwards) and column number(1 onwards)
    def doubleClickCell(self, weTable, iRow, iCol):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                ActionChains(selenium_driver.connect()).double_click(weTable.find_elements_by_tag_name("tr")[int(iRow) - 1].find_elements_by_tag_name("td")
                                 [int(iCol)]).perform()
            except Exception as ex:
                print(
                    'Cell data for web table ' + str(weTable) + ' at row ' + iRow + ' and column ' + iCol + ' cannot be '
                                                                                                       'double clicked. ' + str(
                        ex))
                reportFact.AddSteps('Cell data for web table ' + str(weTable) + ' at row ' + iRow + ' and column ' + iCol +
                                    ' should be double clicked. ',
                                    "Cell data for web table " + str(weTable) + ' at row ' + iRow + ' and '
                                                                                               'column ' + iCol + ' cannot be double clicked. ',
                                    strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def clickLinkInCell(self, weTable, iColumnNumber, strLinkText, iStartRow=0):
        global iRow
        if not globalVar.bln_SkipTestCase:
            try:
                iRowCount = self.get_row_count(weTable)
                time.sleep(globalVar.MTAFDelay)
                lstRows = weTable.find_elements_by_tag_name("tr")
                if iStartRow > 0:
                    iStartRow = iStartRow - 1

                for iRow in range(iStartRow, iRowCount):
                    weRow = lstRows[iRow]
                    if iColumnNumber == 0:
                        strActualData = weRow.text
                    else:
                        strActualData = weRow.find_elements_by_tag_name("td")[int(iColumnNumber) - 1].text
                    if strLinkText == strActualData:
                        iRow = iRow + 1
                        if iColumnNumber == 0:
                            weRow.find_elements_by_tag_name("td")[0].click()
                        else:
                            weRow.find_elements_by_tag_name("td")[int(iColumnNumber) - 1].click()
                        break
            except Exception as ex:
                print('Row number ' + str(iRow) + ' with data ' + strLinkText + 'cannot be clicked.' + str(ex))
                reportFact.AddSteps(
                    'Row number ' + str(iRow) + ' with data ' + strLinkText + 'should be clicked.',
                    'Row number ' + str(iRow) + ' with data ' + strLinkText + 'cannot be clicked.', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
