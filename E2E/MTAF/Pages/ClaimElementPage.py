from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class ClaimElementPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def selectClaimant(self, status):
        we = self.weFact.getElementFromJson("ClaimElementPage", "tblClaimant", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 6, status)
                rowCnt = rowCnt + 1
                if iRowNumber > 0:
                    self.weTableFact.clickCell(we, iRowNumber, 1)
                    blnFlag = True
                    break
                elif rowCnt == self.weTableFact.get_row_count(we):
                    break

            if blnFlag:
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Claimant details should be selected.', "Claimant details selected.")
            else:
                strExpMsg = "Claimant table should have details to be selected"
                strActMsg = "Claimant table does not have data to select"
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def selectBenefit(self, benefit):
        we = self.weFact.getElementFromJson("ClaimElementPage", "tblBenefit", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1 and not globalVar.bln_SkipTestCase:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 3, benefit)
                rowCnt = rowCnt + 1
                if iRowNumber > 0:
                    self.weTableFact.clickCell(we, iRowNumber, 1)
                    blnFlag = True
                    break
                elif rowCnt == self.weTableFact.get_row_count(we):
                    break

            if blnFlag:
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Benefit details should be selected.', "Benefit details selected.")
            else:
                strExpMsg = "Benefit table should have details to be selected"
                strActMsg = "Benefit details does not have data to select"
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def selectSubBenefit(self, benefit):
        we = self.weFact.getElementFromJson("ClaimElementPage", "tblSubBenefit", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1 and not globalVar.bln_SkipTestCase:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 1, benefit)
                rowCnt = rowCnt + 1
                if iRowNumber > 0:
                    self.weTableFact.clickCell(we, iRowNumber, 1)
                    blnFlag = True
                    break
                elif rowCnt == self.weTableFact.get_row_count(we):
                    break

            if blnFlag:
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Sub Benefit details should be selected.', "Sub Benefit details selected.")
            else:
                strExpMsg = "Sub Benefit table should have details to be selected"
                strActMsg = "Sub Benefit details does not have data to select"
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def getNotifiedDate(self):
        we = self.weFact.getElementFromJson("ClaimElementPage", "txtNotifiedDate")
        notifiedDate = self.weFact.getElementAttributeValue(we, "value")
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Notified Date should be fetched.', 'Fetched notified date value is:"' + notifiedDate + "'.")
        return notifiedDate

    def setClaimDate(self, strData):
        we = self.weFact.getElementFromJson("ClaimElementPage", "txtClaimDate")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Claim date should be entered', "Claim Date '" + strData + "' has been entered successfully.")

    def clickEnterorUpdateClaim(self):
        we = self.weFact.getElementFromJson("ClaimElementPage", "btnEnterorUpdateClaim")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Enter or Update Claim button should be clicked.', 'Enter or Update Claim button clicked successfully.')

    def clickEnterorAmendClaimPayment(self):
        we = self.weFact.getElementFromJson("ClaimElementPage", "lnkEnterAmendClaimPayment")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Enter/Amend Claim Payment link should be clicked.', 'Enter/Amend Claim Payment link clicked successfully.')

    def selectChangeStatus(self, strData):
        we = self.weFact.getElementFromJson("ClaimElementPage", "selectChangeStatus")
        self.weFact.selectDropdownDataByPartialText(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Select data from Change Status dropdown menu',
                                "Change Status value '" + strData + "' has been selected successfully")

    def clickAcceptStatusChange(self):
        we = self.weFact.getElementFromJson("ClaimElementPage", "btnAcceptStatusChange")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Accept Status Change button should be clicked.', 'Accept Status Change button clicked successfully.')
