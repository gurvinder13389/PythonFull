from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory


class TaskRequestPage:
    def __init__(self):
        self.weFact = WebElementFactory()

    def clickDirectDebitRunRequest(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "DirectDebitRunRequest")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('DirectDebitRunRequest task Link should be clicked.',
                                'DirectDebitRunRequest task Link clicked successfully.')

    def clickDDRejectionFileSetUpClick(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "DDRejectionFileSetup")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('DDRejectionFileSetUp task Link should be clicked.', 'DDRejectionFileSetUp task Link clicked successfully.')

    def clickAgentStatementClick(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "AgentStatement")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('AgentStatement task Link should be clicked.', 'AgentStatement task Link clicked successfully.')

    def clickNominalLedgerExport(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "NominalLedgerExport")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('NominalLedgerExport task link should be clicked.', 'NominalLedgerExport task Link clicked successfully.')

    def clickPolicyEventProcessing(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "PolicyEventProcessing")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('PolicyEventProcessing task Link should be clicked.',
                                'PolicyEventProcessing task Link clicked successfully.')

    def clickPremiumWaiverPayment(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "PremiumWaiverPayment")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('PremiumWaiverPayment task Link should be clicked.',
                                'PremiumWaiverPayment task Link clicked successfully.')

    def clickLapseProcessing(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "LapseProcessing")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('LapseProcessing task Link should be clicked.',
                                'LapseProcessing task Link clicked successfully.')

    def setBank(self, strData):
        we = self.weFact.getElementFromJson("TaskRequestPage", "txtBank")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Bank value should be entered', "Bank value '" + strData + "' has been entered successfully.")

    def setAgent(self, strData):
        we = self.weFact.getElementFromJson("TaskRequestPage", "txtAgent")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Agent should be entered', "Agent '" + strData + "' has been entered successfully.")

    def setPostSet(self, strData):
        we = self.weFact.getElementFromJson("TaskRequestPage", "txtPostSet")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Post Set should be entered', "Post Set '" + strData + "' has been entered successfully.")

    def clickOkImmediate(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "btnOkImmediate")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('OkImmediate button should be clicked.', 'OkImmediate button clicked successfully.')

    def verifyBatchComplete(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "BatchComplete")
        self.weFact.isElementDisplay(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Batch Complete message should occur.', 'Batch Complete message occured successfully.')

    def getTaskId(self):
        we = self.weFact.getElementFromJson("TaskRequestPage", "Task_Job", enabled=False)
        taskId = self.weFact.getElementAttributeValue(we, "value")
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Task id should be fetched.', "Fetched task id value is:'" + taskId + "'." )
        return taskId
