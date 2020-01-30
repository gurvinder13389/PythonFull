import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from MTAF.ReusableFunctions import selenium_driver, globalVar, reportFact
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverFunctions:
    def switchFrameName(self, sFrameName):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                selenium_driver.connect().switch_to.default_content()
                locator = (By.NAME, sFrameName)
                WebDriverWait(selenium_driver.connect(), 10).until(EC.frame_to_be_available_and_switch_to_it(locator))
                time.sleep(globalVar.MTAFDelay)
            except Exception as ex:
                print('Frame ' + sFrameName + ' of the application could not be switched. ' + str(ex))
                reportFact.AddSteps('Frame ' + sFrameName + ' of the application should be switched.' ,
                                    'Frame ' + sFrameName + ' of the application could not be switched.',strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def keyPress(self, key):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                if key.lower().find("tab") >= 0:
                    ky = Keys.TAB
                elif key.lower().find("enter") >= 0:
                    ky = Keys.ENTER
                else:
                    ky = Keys.ENTER
                ActionChains(selenium_driver.connect()).send_keys(ky).perform()
                time.sleep(globalVar.MTAFDelay)
            except Exception as ex:
                print('Key ' + key + ' could not be pressed. ' + str(ex))
                reportFact.AddSteps('Key ' + key + ' should be pressed.',
                                    'Key ' + key + ' could not be pressed.',strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def goToInitialScreen(self):
        try:
            bln = True
            while bln:
                time.sleep(globalVar.MTAFDelay)
                selenium_driver.connect().switch_to.default_content()
                selenium_driver.connect().switch_to.frame("AppWindow")
                lstClose = selenium_driver.connect().find_elements_by_xpath("//*[normalize-space(text())='Close']")
                if len(lstClose) > 0:
                    lstClose[0].click()
                    time.sleep(1)
                else:
                    bln = False
        except Exception as ex:
            reportFact.AddSteps('Application should be navigated to the initial screen. ',
                                'Application could not be navigated to the initial screen. ',strPassFail="Fail")
            print('Application could not be navigated to the initial screen. ' + str(ex))
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True

    def goToInitialScreenAndExit(self):
        try:
            self.goToInitialScreen()
            time.sleep(globalVar.MTAFDelay)
            selenium_driver.connect().switch_to.default_content()
            selenium_driver.connect().switch_to.frame("AppWindow")
            selenium_driver.connect().find_element_by_xpath("//span[text()='Exit']").click()
        except Exception as ex:
            print('Application could not be navigated to the initial screen to exit. ' + str(ex))
            reportFact.AddSteps('Application should be navigated to the initial screen to exit. ',
                                'Application could not be navigated to the initial screen to exit. ',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True

    def getTitle(self):
        if not globalVar.bln_SkipTestCase:
            try:
                return selenium_driver.connect().title
            except Exception as ex:
                print('Title of the page could not be fetched. ' + str(ex))
                reportFact.AddSteps('Title of the page should be fetched. ',
                                    'Title of the page could not be fetched. ',strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def maximizeBrowser(self):
        if not globalVar.bln_SkipTestCase:
            try:
                selenium_driver.connect().maximize_window()
            except Exception as ex:
                print('Browser window could not be maximized. ' + str(ex))
                reportFact.AddSteps('Browser window should be maximized. ',
                                    'Browser window could not be maximized. ',strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def MTAFAssert(self, strExp, strAct):
        if not globalVar.bln_SkipTestCase:
            try:
                assert strExp == strAct
            except Exception as ex:
                print("Verification Failed.Expected value = '" + strExp + "' and Actual value is '" + strAct + "'" + str(ex))
                reportFact.AddSteps('Verification should pass.',
                                    "Verification Failed.Expected value = '" + strExp + "' and Actual value is '" + strAct + "'",strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def MTAFAssertBoolean(self, blnFlag, expMessage, actMessage):
        if not globalVar.bln_SkipTestCase:
            try:
                assert blnFlag
            except Exception as ex:
                print(expMessage + " and " + actMessage + " " + str(ex))
                reportFact.AddSteps(expMessage, actMessage, strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def captureScreenShot(self):
        selenium_driver.connect().save_screenshot(globalVar.screenShotPath)
        time.sleep(1)

    def setScreenShotFlag(self):
        if not globalVar.bln_SkipTestCase:
            globalVar.bln_takeScreenshot = True

    def takeScreenShot(self):
        if not globalVar.bln_SkipTestCase:
            time.sleep(1)
            self.captureScreenShot()
