from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class TransactionEnquiryPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def verifyAccountTransactionAmount(self, account, transactionAmount):
        we = self.weFact.getElementFromJson("TransactionEnquiryPage", "tblAccountingPostings", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                csvCol = [4, 6]
                csvValue = [account, transactionAmount]
                iRowNumber = self.weTableFact.getRowNumOnMultiColumnDataCompare(we, csvCol, csvValue)
                if iRowNumber > 0:
                    self.weTableFact.clickCell(we, iRowNumber, 1)
                    blnFlag = True
                    break
                elif rowCnt == self.weTableFact.get_row_count(we):
                    break

            if blnFlag and not globalVar.bln_SkipTestCaseLog:
                reportFact.AddSteps('Transaction entry for ' + account + ' with amount ' + transactionAmount + ' should be clicked.', 'Transaction entry for ' + account + ' with amount ' + transactionAmount + ' fetched and clicked.')
            else:
                strExpMsg = 'Transaction entry for ' + account + ' with amount ' + transactionAmount + ' should be clicked.'
                strActMsg = 'No Transaction entry for ' + account + ' with amount ' + transactionAmount + '.'
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
