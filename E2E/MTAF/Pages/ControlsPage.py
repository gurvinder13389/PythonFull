from MTAF.ReusableFunctions import reportFact, globalVar
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory


class ControlsPage:
    def __init__(self):
        self.weFact = WebElementFactory()

    def clickChangeControlValue(self):
        we = self.weFact.getElementFromJson("ControlsPage", "ChangeControlValue")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('ChangeControlValue link should be clicked.', 'ChangeControlValue link clicked successfully.')

    def clickSystemDate(self):
        we = self.weFact.getElementFromJson("ControlsPage","SystemDate")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('SystemDate Link should be clicked.', 'SystemDate Link clicked successfully.')

    def clickAccounting(self):
        we = self.weFact.getElementFromJson("ControlsPage","Accounting")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Accounting Link should be clicked.', 'Accounting Link clicked successfully.')

    def getCurrentPostingSetValue(self):
        we = self.weFact.getElementFromJson("ControlsPage", "CurrentPostingSetValue", enabled=False)
        CurrentPostingSetValue = self.weFact.getElementText(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('CurrentPostingSetValue should be fetched.', "Fetched CurrentPostingSet Value is:'" + CurrentPostingSetValue + "'." )
        return CurrentPostingSetValue
