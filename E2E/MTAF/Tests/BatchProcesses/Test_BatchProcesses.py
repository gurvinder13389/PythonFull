import pytest
import os
import shutil
import time
from MTAF.Pages.BillingRunDetailsPage import BillingRunDetailsPage
from MTAF.Pages.CollectionPage import CollectionPage
from MTAF.Pages.HomePage import HomePage
from MTAF.Pages.LoginPage import LoginPage
from MTAF.Pages.QueuedTaskDiaryPage import QueuedTaskDiaryPage
from MTAF.Pages.TaskDetailsPage import TaskDetailsPage
from MTAF.Pages.TaskRequestPage import TaskRequestPage
from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.Pages.ControlsPage import ControlsPage


class Test_BatchProcesses:
    @pytest.fixture()
    def beforeTestCase(self):
        globalVar.moduleName = __name__
        if not globalVar.bln_SkipTestModule:
            reportFact.resetReportFlags()
        yield self.beforeTestCase
        if not globalVar.bln_SkipTestModule:
            if globalVar.bln_SkipTestCase:
                strPassFail = "Fail"
                if not globalVar.bln_IterationFailure:
                    oDriverFunctions.captureScreenShot()
            else:
                strPassFail = "Pass"
            oDriverFunctions.goToInitialScreen()
            reportFact.closeFile()
        else:
            strPassFail = "Abort"
        reportFact.AddSummarySteps(globalVar.testCaseName, strPassFail)

    @pytest.fixture("module")
    def initialize(self):
        global oDriverFunctions
        global oLogin
        global oHome
        global oQueuedTaskDiaryPage
        global oTaskRequestPage
        global oWebElementFactory
        global oCollectionPage
        global oBillingRunDetailsPage
        global oTaskDetailsPage
        global oControlsPage

        oLogin = LoginPage()
        oHome = HomePage()
        oQueuedTaskDiaryPage = QueuedTaskDiaryPage()
        oTaskRequestPage = TaskRequestPage()
        oDriverFunctions = DriverFunctions()
        oCollectionPage = CollectionPage()
        oBillingRunDetailsPage = BillingRunDetailsPage()
        oTaskDetailsPage = TaskDetailsPage()
        oControlsPage = ControlsPage()

    def test_DirectDebitRunRequestBatch(self, setUp, param1, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()

            # Clicking on Request A Task Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.clickRequest_a_Task()

            # Run Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickDirectDebitRunRequest()
            oTaskRequestPage.setBank(param1)
            oDriverFunctions.keyPress("tab")
            oTaskRequestPage.clickOkImmediate()
            oDriverFunctions.setScreenShotFlag()
            oTaskRequestPage.verifyBatchComplete()
            oDriverFunctions.takeScreenShot()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()

    def test_DDRejection(self, setUp, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Moving the AIG file to production folder
            pathAIG = globalVar.projectLocation + globalVar.configData["DDRejectionAIGFileLocation"]
            for file in os.listdir(pathAIG):
                if file.endswith(".csv"):
                    pathAIG = os.path.join(pathAIG, file)
                    break

            pathProd = globalVar.configData["DDRejectionProdFile"]
            pathProd = os.path.join(pathProd["Path"], pathProd["FileName"])

            # shutil.move(pathAIG, pathProd)
            shutil.copyfile(pathAIG, pathProd)

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()

            # Clicking on Request A Task Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.clickRequest_a_Task()

            # Run Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickDDRejectionFileSetUpClick()
            oTaskRequestPage.clickOkImmediate()
            oTaskRequestPage.verifyBatchComplete()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()

            iTaskNumberDDRejectionImport = 0
            oQueuedTaskDiaryPage.clickOutstanding()
            iTaskNumberDDRejectionImport = oQueuedTaskDiaryPage.clickAndGetNextAvailableJob(iTaskNumber, "DD Rejection Import")
            oQueuedTaskDiaryPage.clickOutstanding()
            time.sleep(5)
            oQueuedTaskDiaryPage.taskProcessedAssert(oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumberDDRejectionImport))

    def test_AgentStatement(self, setUp, param1, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()

            # Clicking on Request A Task Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.clickRequest_a_Task()

            # Run Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickAgentStatementClick()
            oTaskRequestPage.setAgent(param1)
            oTaskRequestPage.clickOkImmediate()
            oDriverFunctions.setScreenShotFlag()
            oTaskRequestPage.verifyBatchComplete()
            oDriverFunctions.takeScreenShot()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()

    def test_NLIReport(self, setUp, param1, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            #Navigating to  Controls screen
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveSetup()
            oHome.clickControls()

            #Fetch the Current Posting Set
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oControlsPage.clickAccounting()
            strCurrentPostingSet = oControlsPage.getCurrentPostingSetValue()
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()

            # Clicking on Request A Task Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.clickRequest_a_Task()

            # Run Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickNominalLedgerExport()
            oTaskRequestPage.setPostSet(strCurrentPostingSet)
            oDriverFunctions.keyPress("tab")
            oTaskRequestPage.clickOkImmediate()
            oDriverFunctions.setScreenShotFlag()
            oTaskRequestPage.verifyBatchComplete()
            oDriverFunctions.takeScreenShot()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()

    def test_DDUpdate(self, setUp, param1, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Navigating to Collection
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.clickCollection()

            # Get the latest Collection Run Details
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskID = oCollectionPage.getAndDoubleClickLatestCollectionRun("Direct Debit", "Active", param1)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oBillingRunDetailsPage.clickClose()

            # Click on DD Update link for the selected Run task
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oCollectionPage.selectCollectionRun(taskID)
            oCollectionPage.clickDirectDebitUpdate()

            # Run DD Update Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickOkImmediate()
            oDriverFunctions.setScreenShotFlag()
            oTaskRequestPage.verifyBatchComplete()
            oDriverFunctions.takeScreenShot()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()

    def test_PolicyEventProcessing(self, setUp, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()

            # Clicking on Request A Task Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.clickRequest_a_Task()

            # Run Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickPolicyEventProcessing()
            oDriverFunctions.keyPress("tab")
            oTaskRequestPage.clickOkImmediate()
            oDriverFunctions.setScreenShotFlag()
            oTaskRequestPage.verifyBatchComplete()
            oDriverFunctions.takeScreenShot()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()

    def test_PremiumWaiverPayment(self, setUp, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()

            # Clicking on Request A Task Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.clickRequest_a_Task()

            # Run Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickPremiumWaiverPayment()
            oDriverFunctions.keyPress("tab")
            oTaskRequestPage.clickOkImmediate()
            oDriverFunctions.setScreenShotFlag()
            oTaskRequestPage.verifyBatchComplete()
            oDriverFunctions.takeScreenShot()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()

    def test_LapseProcessing(self, setUp, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()

            # Clicking on Request A Task Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.clickRequest_a_Task()

            # Run Batch
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskRequestPage.clickLapseProcessing()
            oDriverFunctions.keyPress("tab")
            oTaskRequestPage.clickOkImmediate()
            oDriverFunctions.setScreenShotFlag()
            oTaskRequestPage.verifyBatchComplete()
            oDriverFunctions.takeScreenShot()
            iTaskNumber = oTaskRequestPage.getTaskId()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.goToInitialScreen()

            # Navigating to Tasks
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveOperations()
            oHome.clickTasks()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oDriverFunctions.setScreenShotFlag()
            taskStatus = oQueuedTaskDiaryPage.getStatusByTaskId(iTaskNumber)
            time.sleep(5)
            oDriverFunctions.takeScreenShot()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oTaskDetailsPage.clickClose()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oQueuedTaskDiaryPage.scrollQueuedTaskTableUntilElementVisible(iTaskNumber)
            oDriverFunctions.setScreenShotFlag()
            oQueuedTaskDiaryPage.taskProcessedAssert(taskStatus)
            oDriverFunctions.takeScreenShot()
