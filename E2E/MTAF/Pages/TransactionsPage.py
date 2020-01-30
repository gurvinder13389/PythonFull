from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class TransactionsPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def doubleClickTransactionRecord(self, strDate, transactionName):
        we = self.weFact.getElementFromJson("TransactionsPage", "tblTransactions", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                csvCol = [1, 3]
                csvValue = [strDate, transactionName]
                iRowNumber = self.weTableFact.getRowNumOnMultiColumnDataCompare(we, csvCol, csvValue)
                if iRowNumber > 0:
                    self.weTableFact.doubleClickCell(we, iRowNumber, 1)
                    blnFlag = True
                    break
                elif rowCnt == self.weTableFact.get_row_count(we):
                    break

            if blnFlag and not globalVar.bln_SkipTestCaseLog:
                reportFact.AddSteps('Transaction entry for ' + transactionName + ' on date ' + strDate + ' should be clicked.', 'Transaction entry for ' + transactionName + ' on date ' + strDate + ' fetched and clicked.')
            else:
                strExpMsg = 'Transaction entry for ' + transactionName + ' on date ' + strDate + ' should be clicked.'
                strActMsg = 'Transaction entry for ' + transactionName + ' on date ' + strDate + ' could not be clicked.'
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
