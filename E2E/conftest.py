import datetime
import sys
import os
import pytest
from MTAF.Pages.LoginPage import LoginPage
from MTAF.ReusableFunctions import globalVar, selenium_driver, reportFact, ExcelUtil, JsonFactory

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def pytest_addoption(parser):
    try:
        parser.addoption("--param1", action="store", default="", help="Provide Parameter value")
        parser.addoption("--logFileAttr", action="store", default="", help="Provide data for log details")
        parser.addoption("--enableE2E", action="store", default=False, help="Provide boolean to enable E2E framework")
    except Exception as ex:
        print('Command line options could not be added. ' + str(ex))


@pytest.fixture
def param1(request):
    try:
        return request.config.getoption("--param1")
    except Exception as ex:
        print('Command line options param1 could not be fetched. ' + str(ex))


@pytest.fixture
def logFileAttr(request):
    try:
        return request.config.getoption("--logFileAttr")
    except Exception as ex:
        print('Command line options logFileAttr could not be fetched. ' + str(ex))


def pytest_sessionstart(session):
    try:
        session.results = dict()
    except Exception as ex:
        print('pytest_sessionstart. ' + str(ex))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    try:
        outcome = yield
        result = outcome.get_result()

        if result.when == 'call':
            item.session.results[item] = result
    except Exception as ex:
        print('pytest_runtest_makereport. ' + str(ex))


def pytest_sessionfinish(session, exitstatus):
    try:
        if globalVar.bln_SkipTestCase:
            exitstatus = 1
        resultStatus = ""
        if str(exitstatus) == "0":
            resultStatus = "Test passed successfully"
        elif str(exitstatus) == "1":
            resultStatus = "Test was collected and run but some part of the test failed"
        elif str(exitstatus) == "2":
            resultStatus = "Test execution was interrupted by the user"
        elif str(exitstatus) == "3":
            resultStatus = "Internal error happened while executing test"
        elif str(exitstatus) == "4":
            resultStatus = "pytest command line usage error"
        elif str(exitstatus) == "5":
            resultStatus = "No test was collected"

        print()
        print('run status code:', exitstatus)
        print(resultStatus)
        passed_amount = sum(1 for result in session.results.values() if result.passed)
        failed_amount = sum(1 for result in session.results.values() if result.failed)
        print(f'{passed_amount} passed and {failed_amount} failed tests')

        with open("captureTestStatus.txt", 'a', encoding='utf-8') as f:
            f.write(globalVar.logFileAttrData + ',' + str(exitstatus) + "," + globalVar.testCaseFilePath + '\n')
    except Exception as ex:
        print('Exit Status code for the test cannot be captured successfully. ' + str(ex))


@pytest.fixture(scope="session")
def setUp():
    try:
        globalVar.projectLocation = JsonFactory.getProjectPath()
        globalVar.configData = JsonFactory.loadData()
        globalVar.locatorsData = JsonFactory.loadLocatorsData()
        strFolderName = str(datetime.datetime.now()).replace(':', "_")
        globalVar.reportFolderPath = os.path.join(os.path.dirname(__file__),"MTAF") + '/Reports/' + strFolderName
        os.mkdir(globalVar.reportFolderPath)
        os.mkdir(globalVar.reportFolderPath + "/Screenshots")
        reportFact.openAndCreateSummaryFile()
        selenium_driver.connect()
        LoginPage().lissiaLogin()
        yield setUp
        reportFact.closeSummaryFile()
        selenium_driver.close()
        # selenium_driver.launchUrl(globalVar.summaryFilePath)
    except Exception as ex:
        print('Issue with Setup or tear down. ' + str(ex))
        globalVar.bln_SkipTestCase = True


def pytest_collection_modifyitems(config, items):
    globalVar.bln_enableE2E = config.getoption("--enableE2E")
    if not globalVar.bln_enableE2E:
        # open pyxl code need to be placed here in order to get all the testcases
        # with mode as 'y' or '' and add them in run marker.
        for item in items:
            strTestCase = str(item.nodeid).split('_')[len(str(item.nodeid).split('_')) - 1]

            globalVar.excelWBName = "Runner"
            globalVar.excelWB = ExcelUtil.getExcelWB()

            iTestCaseRow = ExcelUtil.findRowPos("Runner",strTestCase,2)
            if iTestCaseRow > 0:
                strMode = ExcelUtil.getData("Runner",iTestCaseRow,1)
                if strMode==None:
                    strMode = ''

                if strMode.lower()!="n":
                    item.add_marker(pytest.mark.run)
