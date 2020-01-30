from MTAF.ReusableFunctions import reportFact, globalVar
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class CollectionPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def clickManualRejection(self):
        we = self.weFact.getElementFromJson("CollectionPage", "ManualRejection")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('ManualRejection link should be clicked.', 'ManualRejection link clicked successfully.')

    def clickDirectDebitUpdate(self):
        we = self.weFact.getElementFromJson("CollectionPage", "DirectDebitUpdate")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Direct Debit Update link should be clicked.',
                                "Direct Debit Update link clicked successfully.")

    def getAndDoubleClickLatestCollectionRun(self, collectionMethod, status, rowDataCompare):
        we = self.weFact.getElementFromJson("CollectionPage", "CollectionRunTable", enabled=False)
        taskId = ''

        if not globalVar.bln_SkipTestCase:
            strRowData = rowDataCompare.split(",")
            dict = {}
            csvLstCol = []
            for val in strRowData:
                varDetails = val.split("=")
                dict[varDetails[0]] = varDetails[1]

            for iKey in dict:
                if iKey == 'runDate':
                    # Adding the column number of runDate as per the Collection table in lissia
                    csvLstCol.append(3)
                elif iKey == 'bankNum':
                    # Adding the column number of bankNum as per the Collection table in lissia
                    csvLstCol.append(5)

            self.weFact.selectDropdownData(self.weFact.getElementFromJson("CollectionPage", "selectCollectionMethod"),
                                           collectionMethod)
            self.weFact.selectDropdownData(self.weFact.getElementFromJson("CollectionPage", "selectCollectionRunStatus"),
                                           status)
            self.weFact.setData(self.weFact.getElementFromJson("CollectionPage", "txtFromRunDate"), dict['runDate'])
            self.drivFunc.keyPress('Tab')

            weRunNo = self.weFact.getElementFromJson("CollectionPage", "btnRunNo")
            self.weFact.clickElement(weRunNo)

            blnFlag = True
            rowCnt = self.weTableFact.get_row_count(we)

            if rowCnt == 0:
                blnFlag = False
            else:
                csvLstRowData = []
                for iKey in dict:
                    # The list of bank number below are specific to AIG. We will have to update this list for other clients
                    if iKey == 'bankNum':
                        if dict[iKey] == '1':
                            csvLstRowData.append('B.A.C.S.')
                        elif dict[iKey] == '3':
                            csvLstRowData.append('Commidea/Worldpay')
                        elif dict[iKey] == '50':
                            csvLstRowData.append('B.A.C.S. DirectLine')
                        elif dict[iKey] == '51':
                            csvLstRowData.append('B.A.C.S. Churchill')
                        else:
                            csvLstRowData.append('Invalid Bank Number')
                    else:
                        csvLstRowData.append(dict[iKey])
                iRowNumber = self.weTableFact.getRowNumOnMultiColumnDataCompare(we, csvLstCol, csvLstRowData, 'descending')
                if iRowNumber == 0:
                    blnFlag = False
                else:
                    taskId = self.weTableFact.getCellData(we, iRowNumber, 1)
                    self.weTableFact.doubleClickCell(we, iRowNumber, 1)

            if blnFlag and not globalVar.bln_SkipTestCaseLog:
                reportFact.AddSteps("Latest Collection Run Task should be fetched and clicked for the run date " +
                                    dict['runDate'] + " and bank number " + dict['bankNum'],
                                    "Latest Collection Run with Task Id '" + taskId + "' fetched and clicked for the run date " +
                                    dict['runDate'] + " and bank number " + dict['bankNum'])
            else:
                strExpMsg = "Latest Collection Run Task should be fetched and clicked for the run date " + \
                            dict['runDate'] + " and bank number " + dict['bankNum']
                strActMsg = "No Collection Run Task could be fetched for the run date " + dict['runDate'] + \
                            " and bank number " + dict['bankNum']
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
        return taskId

    def selectCollectionRun(self, taskId):
        we = self.weFact.getElementFromJson("CollectionPage", "CollectionRunTable", enabled=False)
        blnFlag = True

        if not globalVar.bln_SkipTestCase:
            if self.weTableFact.get_row_count(we) == 0:
                blnFlag = False
            else:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 1, taskId)
                self.weTableFact.clickCell(we, iRowNumber, 1)

            if blnFlag and not globalVar.bln_SkipTestCaseLog:
                reportFact.AddSteps(
                    "Collection Run Task " + "'" + taskId + "' should be selected.",
                    "Collection Run Task " + "'" + taskId + "' could not be selected.")
            else:
                strExpMsg = "Collection Run Task " + "'" + taskId + "' should be selected."
                strActMsg = "Collection Run Task " + "'" + taskId + "' is not present in the list."
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
