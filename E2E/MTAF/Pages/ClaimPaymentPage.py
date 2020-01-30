from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class ClaimPaymentPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def selectBeneficiary(self, strData):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "selectBeneficiary")
        self.weFact.selectDropdownDataByPartialText(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Select data from Rejection Reason dropdown menu',
                                "Rejection Reason value '" + strData + "' has been selected successfully")

    def selectBankDetails(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "tblBankDetails")
        blnFlag = False

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                self.weTableFact.clickCell(we, 2, 1)
                blnFlag = True
                break

            if blnFlag:
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Bank Account details should be selected.',
                                        'Bank Account details selected successfully.')
            else:
                strExpMsg = 'Bank Account details should be selected.'
                strActMsg = 'Bank Account details not availabe to select.'
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def clickAcceptChanges(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "btnAcceptChanges")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Accept Changes button should be clicked.', 'Accept Changes button should be clicked.')

    def clickAcceptChangesandExit(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "btnAcceptChangesandExit")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Accept Changes and Exit button should be clicked.', 'Accept Changes and Exit button should be clicked.')

    def clickAuthorisePayment(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "btnAuthorisePayment")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Authorise Payment button should be clicked.', 'Authorise Payment button should be clicked.')

    def claimStatusAssert(self, strExpStatus, strActStatus):
        self.drivFunc.MTAFAssert(strExpStatus, strActStatus)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Claim status should be "' + strExpStatus + '".','Claim status is "' + strActStatus + '".')

    def policyStatusAssert(self, strExpStatus, strActStatus):
        self.drivFunc.MTAFAssert(strExpStatus, strActStatus)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Policy status should be "' + strExpStatus + '".','Policy status is "' + strActStatus + '".')

    def clickClaimBenefitRow(self, benefit):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "tblClaimDetails", enabled=False)
        blnFlag = False
        rowCnt = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 5, benefit)
                rowCnt = rowCnt + 1
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

    def selectClaimPayment(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "tblClaimPayment")
        blnFlag = False

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                self.weTableFact.clickCell(we, 2, 1)
                blnFlag = True
                break

            if blnFlag:
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Claim Payment details should be selected.',
                                        'Claim Payment details selected successfully.')
            else:
                strExpMsg = 'Claim Payment details should be selected.'
                strActMsg = 'Claim Payment details not availabe to select.'
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def authorisedDateAssert(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "txtAuthorisedDate")
        authorisedDate = self.weFact.getElementAttributeValue(we, "value")
        blnFlag = False

        if authorisedDate!="":
            blnFlag = True

        if blnFlag and not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Authorised Date should not be blank.', 'Authorised Date is not blank')
        else:
            strExpMsg = "Authorised Date should not be blank"
            strActMsg = "Authorised Date is blank"
            self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def authorisedTimeAssert(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "txtAuthorisedTime")
        authorisedDate = self.weFact.getElementAttributeValue(we, "value")
        blnFlag = False

        if authorisedDate!="":
            blnFlag = True

        if blnFlag and not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Authorised Time should not be blank.', 'Authorised Time is not blank')
        else:
            strExpMsg = "Authorised Time should not be blank"
            strActMsg = "Authorised Time is blank"
            self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)

    def selectPaymentStatus(self, strData):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "selectPaymentStatus")
        self.weFact.selectDropdownData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Select data from Payment Status dropdown menu',
                                'Payment Status value "' + strData + '" has been selected successfully')

    def getPaymentAmount(self):
        we = self.weFact.getElementFromJson("ClaimPaymentPage", "txtPaymentAmount")
        paymentAmount = self.weFact.getElementAttributeValue(we, "value")
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Payment Amount should be fetched.', 'Fetched Payment Amount value is:"' + paymentAmount + "'.")
        return paymentAmount
