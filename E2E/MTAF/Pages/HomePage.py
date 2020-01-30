from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions import reportFact, globalVar


class HomePage:
    def __init__(self):
        self.weFact = WebElementFactory()

    def moveSetup(self):
        we = self.weFact.getElementFromJson("HomePage", "Setup")
        self.weFact.moveToElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Mouse should navigate to Setup menu', 'Mouse navigated to Setup menu')

    def clickControls(self):
        we = self.weFact.getElementFromJson("HomePage", "Controls")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Controls menu should be clicked', 'Controls menu is clicked')

    def clickCollection(self):
        we = self.weFact.getElementFromJson("HomePage", "Collection")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Collection menu should be clicked', 'Collection menu is clicked')

    def clickPolicy(self):
        we = self.weFact.getElementFromJson("HomePage", "Policy")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Policy menu should be clicked', 'Policy menu is clicked')

    def moveOperations(self):
        we = self.weFact.getElementFromJson("HomePage", "Operations")
        self.weFact.moveToElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Mouse should navigate to Operations menu', 'Mouse navigated to Operations menu')

    def clickTasks(self):
        we = self.weFact.getElementFromJson("HomePage", "Tasks")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Tasks menu should be clicked', 'Tasks menu is clicked')

    def pageVerify_Home(self):
        we = self.weFact.getElementFromJson("HomePage", "Exit")
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Home Page should open.', 'Home page opened successfully.')
        else:
            reportFact.AddSteps('Home Page should open.', 'Home page does not opened.')
