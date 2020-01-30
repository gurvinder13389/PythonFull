import pytest
import time
from MTAF.Pages.HomePage import HomePage
from MTAF.Pages.LoginPage import LoginPage
from MTAF.ReusableFunctions import globalVar, reportFact, ExcelUtil, selenium_driver
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.Pages.PolicyServicingandEnquiriesPage import PolicyServicingandEnquiriesPage
from MTAF.Pages.LapsePage import LapsePage


class Test_LapseImmediate:
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
        global oPolicyServicingandEnquiriesPage
        global oLapsePage

        oDriverFunctions = DriverFunctions()
        oLogin = LoginPage()
        oHome = HomePage()
        oPolicyServicingandEnquiriesPage = PolicyServicingandEnquiriesPage()
        oLapsePage = LapsePage()

    def test_LapseImmediate(self, setUp, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        reportFact.openAndCreateFile(globalVar.testCaseName)
        # Data for test case will be contained in dataDict
        dataDict = ExcelUtil.getTestCaseData(globalVar.testCaseName)

        # get the row numbers from the dictionary object with the help of column name next to RunMode.
        iterDict = dataDict[ExcelUtil.getData(globalVar.testCaseName, 1, 2)]
        globalVar.logFileAttrData = logFileAttr
        size = 1
        rowCnt = 2

        for iKey in iterDict.keys():
            if dataDict['PolicyNo'][iKey]:
                # common for each iteration
                time.sleep(1)
                if not globalVar.bln_SkipTestModule:
                    globalVar.bln_SkipTestCase = False
                    globalVar.bln_SkipTestCaseLog = False

                reportFact.addIterationStep()
                globalVar.testStepNum = 1

                # Navigating to Policy
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oHome.clickPolicy()

                # Fetch the policy and click on Lapse link
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oPolicyServicingandEnquiriesPage.setPolicy(dataDict['PolicyNo'][iKey])
                oDriverFunctions.keyPress('Tab')
                oDriverFunctions.setScreenShotFlag()
                oPolicyServicingandEnquiriesPage.clickLapse()
                oDriverFunctions.takeScreenShot()

                # Click OK to Lapse the Policy
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oDriverFunctions.setScreenShotFlag()
                oLapsePage.clickOKProceed()
                oDriverFunctions.takeScreenShot()

                # Validate Policy status should be Lapsed
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oPolicyServicingandEnquiriesPage.verifyStatusLapsed()

                # common for each iteration
                if globalVar.bln_SkipTestCase:
                    globalVar.bln_IterationFailure = True
                    globalVar.bln_SkipTestCase = False

                if size == len(iterDict.keys()):
                    oDriverFunctions.goToInitialScreen()
                else:
                    oDriverFunctions.goToInitialScreenAndExit()
                    selenium_driver.close()
                    selenium_driver.connect()
                    globalVar.bln_SkipTestCase = False
                    LoginPage().lissiaLogin()
                    size = size+1
                ExcelUtil.setCellData(globalVar.testCaseName, rowCnt, 3, "Test case executed")
                ExcelUtil.removeCellColor(globalVar.testCaseName, rowCnt, 3)
                rowCnt = rowCnt + 1
            else:
                if globalVar.bln_enableE2E:
                    ExcelUtil.setCellData(globalVar.testCaseName, rowCnt, 3, "Policy Number not provided")
                    ExcelUtil.fillCellColor(globalVar.testCaseName, rowCnt, 3, 'FFFF0000')
                rowCnt = rowCnt + 1

        # Changing the bln_SkipTestCase to True when bln_IterationFailure is True, so that we could use the same
        # after test steps for both iterative and non-iterative test case summary report
        if globalVar.bln_IterationFailure:
            globalVar.bln_SkipTestCase = True
