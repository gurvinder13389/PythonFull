from MTAF.ReusableFunctions import reportFact, globalVar
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class RejectionPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def setPolicy(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "txtEnterPolicy")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Policy ID should be entered',
                                "Policy ID '" + strData + "' has been entered successfully")

    def setReference(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "txtReference")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Reference should be entered',
                                "Reference '" + strData + "' has been entered successfully")

    def setBankAccountNumber(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "txtBankAccountNumber")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Bank Account Number should be entered',
                                "Bank Account Number '" + strData + "' has been entered successfully")

    def setSortCode(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "txtSortCode")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Sort Code should be entered',
                                "Sort Code '" + strData + "' has been entered successfully")

    def setSuspensionReason(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "txtSuspensionReason")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Suspension Reason should be entered',
                                "Suspension Reason '" + strData + "' has been entered successfully")

    def setAmount(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "txtAmount")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Amount should be entered',
                                "Amount '" + strData + "' has been entered successfully")

    def setTransactionCode(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "txtTransactionCode")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Transaction Code should be entered',
                                "Transaction Code '" + strData + "' has been entered successfully")

    def clickRejectPolicyCollection(self):
        we = self.weFact.getElementFromJson("RejectionPage","btnRejectPolicyCollection")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Reject Policy Collection Button should be clicked.',
                                'Reject Policy Collection Link clicked successfully')

    def clickRejectBankCollection(self):
        we = self.weFact.getElementFromJson("RejectionPage","btnRejectBankCollection")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Reject Bank Collection Button should be clicked.',
                                'Reject Bank Collection Button clicked successfully')

    def clickClose(self):
        we = self.weFact.getElementFromJson("RejectionPage","lnkClose")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Close link should be clicked.', 'Close link clicked successfully')

    def selectRejectionReason(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "selectRejectionReason")
        self.weFact.selectDropdownData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Select data from Rejection Reason dropdown menu',
                                "Rejection Reason value '" + strData + "' has been selected successfully")

    def selectRejectionType(self, strData):
        we = self.weFact.getElementFromJson("RejectionPage", "tblRejectionType")
        self.weTableFact.clickLinkInCell(we, 0, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Select data from Rejection Type dropdown menu',
                                "Rejection Type value '" + strData + "' has been selected successfully")

    def verifyManualRejectionComplete(self):
        we = self.weFact.getElementFromJson("RejectionPage", "ManualRejectionComplete")
        self.drivFunc.MTAFAssert('OK :    The Process has Successfully Completed',
                                 self.weFact.getElementAttributeValue(we, 'value'))
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Manual Rejection Process Complete message should occur.',
                                'Manual Rejection Process Complete message occured successfully')
