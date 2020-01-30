import pytest
from MTAF.Pages.ControlsPage import ControlsPage
from MTAF.Pages.HomePage import HomePage
from MTAF.Pages.SystemDatePage import SystemDatePage
from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions


class Test_SystemConfig:
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
        global oControlsPage
        global oSystemDatePage

        oHome = HomePage()
        oControlsPage = ControlsPage()
        oSystemDatePage = SystemDatePage()
        oDriverFunctions = DriverFunctions()

    def test_ChangeSystemDate(self, setUp, param1, logFileAttr, beforeTestCase, initialize, request):
        globalVar.testCaseName = reportFact.getTestCaseName(request.node.name)
        if not globalVar.bln_SkipTestModule:
            reportFact.openAndCreateFile(globalVar.testCaseName)
            globalVar.logFileAttrData = logFileAttr

            # Navigating to SetUp
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oHome.moveSetup()
            oHome.clickControls()

            # Changing System Date
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oControlsPage.clickSystemDate()
            oControlsPage.clickChangeControlValue()

            # Setting system date
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oSystemDatePage.setSystemDate(param1)
            oDriverFunctions.keyPress("tab")
            oSystemDatePage.clickOK()

            oDriverFunctions.setScreenShotFlag()
            oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            oSystemDatePage.systemDateAssert(param1)
            oDriverFunctions.takeScreenShot()
