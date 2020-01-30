import pytest
from MTAF.Pages.CollectionPage import CollectionPage
from MTAF.Pages.HomePage import HomePage
from MTAF.Pages.RejectionPage import RejectionPage
from MTAF.ReusableFunctions import globalVar, reportFact, ExcelUtil
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions


class Test_ManualRejection:
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
        global oHome
        global oCollectionPage
        global oRejectionPage

        oHome = HomePage()
        oDriverFunctions = DriverFunctions()
        oCollectionPage = CollectionPage()
        oRejectionPage = RejectionPage()

    def test_ManualRejection(self, setUp, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        # Data for test case will be contained in dataDict
        reportFact.openAndCreateFile(globalVar.testCaseName)
        dataDict = ExcelUtil.getTestCaseData(globalVar.testCaseName)

        # get the row numbers from the dictionary object with the help of column name next to RunMode.
        iterDict = dataDict[ExcelUtil.getData(globalVar.testCaseName, 1, 2)]
        globalVar.logFileAttrData = logFileAttr

        for iKey in iterDict.keys():
            # common for each iteration
            if not globalVar.bln_SkipTestModule:
                globalVar.bln_SkipTestCase = False
                globalVar.bln_SkipTestCaseLog = False

            reportFact.addIterationStep()
            globalVar.testStepNum = 1

            # Navigating to Collection
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.clickCollection()

            # Clicking on Manual Rejection Link
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oCollectionPage.clickManualRejection()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])

            # Selection by Policy details
            oRejectionPage.setPolicy(str(dataDict['PolicyID'][iKey]))
            oDriverFunctions.keyPress('Tab')
            oRejectionPage.selectRejectionReason(str(dataDict['RejectionReason'][iKey]))

            # Selection by Bank Account details
            oRejectionPage.setReference(str(dataDict['Reference'][iKey]))
            oRejectionPage.setBankAccountNumber(str(dataDict['BankAccountNumber'][iKey]))
            oRejectionPage.setSortCode(str(dataDict['SortCode'][iKey]))
            oRejectionPage.setSuspensionReason(str(dataDict['SuspensionReason'][iKey]))
            oRejectionPage.setAmount(str(dataDict['Amount'][iKey]))
            oRejectionPage.setTransactionCode(str(dataDict['TransactionCode'][iKey]))
            oRejectionPage.selectRejectionType(str(dataDict['RejectionType'][iKey]))

            oRejectionPage.clickRejectBankCollection()
            oDriverFunctions.setScreenShotFlag()
            oRejectionPage.verifyManualRejectionComplete()
            oDriverFunctions.takeScreenShot()

            # common for each iteration
            if globalVar.bln_SkipTestCase:
                globalVar.bln_IterationFailure = True
                oDriverFunctions.captureScreenShot()
            oDriverFunctions.goToInitialScreen()

        # Changing the bln_SkipTestCase to True when bln_IterationFailure is True, so that we could use the same
        # after test steps for both iterative and non-iterative test case summary report
        if globalVar.bln_IterationFailure:
            globalVar.bln_SkipTestCase = True
