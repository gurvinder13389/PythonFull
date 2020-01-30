from MTAF.ReusableFunctions import reportFact, globalVar
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory


class BillingRunDetailsPage:
    def __init__(self):
        self.weFact = WebElementFactory()

    def clickClose(self):
        we = self.weFact.getElementFromJson("BillingRunDetailsPage","lnkClose")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Close link on the Billing Run Details Page should be clicked.',
                                "Close link on the Billing Run Details Page clicked successfully")
