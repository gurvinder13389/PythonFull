from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class ClaimsPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def clickAddaNewClaim(self):
        we = self.weFact.getElementFromJson("ClaimsPage", "lnkAddaNewClaim")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Add a new Claim link should be clicked.', 'Add a new Claim link clicked successfully.')

    def getPolicyStatus(self):
        we = self.weFact.getElementFromJson("ClaimsPage", "txtStatus")
        policyStatus = self.weFact.getElementAttributeValue(we, "value")
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Policy Status should be fetched.', 'Fetched Policy Status value is:"' + policyStatus + "'.")
        return policyStatus

    def getClaimStatus(self, benefit):
        claimStatus = ''
        we = self.weFact.getElementFromJson("ClaimsPage", "tblClaimDetails", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 5, benefit)
                if iRowNumber > 0:
                    claimStatus = self.weTableFact.getCellData(we, iRowNumber, 6)
                    blnFlag = True
                    break
                elif rowCnt == self.weTableFact.get_row_count(we):
                    break

            if blnFlag:
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Claim status should be fetched for "' + benefit + '" benefit.', 'Claim status fetched successfully for "' + benefit + '" benefit.')
            else:
                strExpMsg = 'Claim status should be fetched for "' + benefit + '" benefit.'
                strActMsg = 'Claim status could not be fetched for "' + benefit + '" benefit.'
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
        return claimStatus

    def claimStatusAssert(self, strExpStatus, strActStatus):
        self.drivFunc.MTAFAssert(strExpStatus, strActStatus)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Claim status should be "' + strExpStatus + '".','Claim status is "' + strActStatus + '".')

    def policyStatusAssert(self, strExpStatus, strActStatus):
        self.drivFunc.MTAFAssert(strExpStatus, strActStatus)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Policy status should be "' + strExpStatus + '".','Policy status is "' + strActStatus + '".')

    def clickClaimBenefitRow(self, benefit, status):
        we = self.weFact.getElementFromJson("ClaimsPage", "tblClaimDetails", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                csvRow = [5, 6]
                csvValue = [benefit, status]
                iRowNumber = self.weTableFact.getRowNumOnMultiColumnDataCompare(we, csvRow, csvValue)
                if iRowNumber > 0:
                    self.weTableFact.doubleClickCell(we, iRowNumber, 1)
                    blnFlag = True
                    break
                elif rowCnt == self.weTableFact.get_row_count(we):
                    break

            if blnFlag:
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Claim row for the "' + benefit + '" benefit should be clicked.',
                                        'Claim row for the "' + benefit + '" benefit clicked successfully.')
            else:
                strExpMsg = 'Claim row for the "' + benefit + '" benefit should be clicked.'
                strActMsg = 'Claim row for the "' + benefit + '" benefit could not be clicked.'
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def clickClose(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage","lnkClose")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Close link on the Billing Run Details Page should be clicked.',
                                "Close link on the Billing Run Details Page clicked successfully")