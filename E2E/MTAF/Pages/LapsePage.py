from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions import reportFact, globalVar


class LapsePage:
    def __init__(self):
        self.weFact = WebElementFactory()

    def clickOKProceed(self):
        we = self.weFact.getElementFromJson("LapsePage", "btnOkProceed")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('OK - Proceed button should be clicked.', 'OK - Proceed button clicked successfully.')
