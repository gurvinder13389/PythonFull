from MTAF.ReusableFunctions import reportFact, globalVar
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory


class TaskDetailsPage:
    def __init__(self):
        self.weFact = WebElementFactory()

    def clickClose(self):
        we = self.weFact.getElementFromJson("TaskDetailsPage","lnkClose")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Close link on the Task Details Page should be clicked.',
                                "Close link on the Task Details Page clicked successfully")
