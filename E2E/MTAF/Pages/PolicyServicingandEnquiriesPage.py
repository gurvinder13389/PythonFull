from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory


class PolicyServicingandEnquiriesPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def setPolicy(self, strData):
        we = self.weFact.getElementFromJson("PolicyServicingandEnquiriesPage", "txtEnterPolicy")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Policy should be entered',
                                "Policy '" + strData + "' has been entered successfully.")

    def clickClaims(self):
        we = self.weFact.getElementFromJson("PolicyServicingandEnquiriesPage", "lnkClaims")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Claims link should be clicked.', 'Claims link clicked successfully.')

    def clickTransactions(self):
        we = self.weFact.getElementFromJson("PolicyServicingandEnquiriesPage", "lnkTransactions")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Transactions link should be clicked.', 'Transactions link clicked successfully.')

    def verifyStatusDeathSettlement(self):
        we = self.weFact.getElementFromJson("PolicyServicingandEnquiriesPage", "lnkStatus")

        if not globalVar.bln_SkipTestCase:
            if self.weFact.getElementText(we) == 'Death Settlement':
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Policy status should be Death Settlement.',
                                        'Policy status is Death Settlement.')
            else:
                strExpMsg = 'Policy status should be Death Settlement.'
                strActMsg = 'Policy status is not Death Settlement.'
                self.drivFunc.MTAFAssertBoolean(False, strExpMsg, strActMsg)

    def clickLapse(self):
        we = self.weFact.getElementFromJson("PolicyServicingandEnquiriesPage", "lnkLapse")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Lapse link should be clicked.', 'Lapse link clicked successfully.')

    def verifyStatusLapsed(self):
        we = self.weFact.getElementFromJson("PolicyServicingandEnquiriesPage", "lnkStatus")

        if not globalVar.bln_SkipTestCase:
            if self.weFact.getElementText(we) == 'Lapsed':
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Policy status should be Lapsed.',
                                        'Policy status is Lapsed.')
            else:
                strExpMsg = 'Policy status should be Lapsed.'
                strActMsg = 'Policy status is not Lapsed.'
                self.drivFunc.MTAFAssertBoolean(False, strExpMsg, strActMsg)
