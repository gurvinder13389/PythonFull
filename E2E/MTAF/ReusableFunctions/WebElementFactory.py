import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from MTAF.ReusableFunctions import selenium_driver, globalVar, reportFact


class WebElementFactory:
    def getElementFromJson(self,oPageName,oElementName,enabled=True):
        if not globalVar.bln_SkipTestCase:
            try:
                oLocatorData = globalVar.locatorsData
                oPageJson = oLocatorData[oPageName]
                oElementJson = oPageJson[oElementName]
                loc = oElementJson["locatorType"]
                locVal = oElementJson["locatorValue"]
                return self.getElement(selenium_driver.connect(),locVal,loc,enabled)
            except Exception as ex:
                print('Web element could not be fetched using the JSON locator details. ' + str(ex))
                reportFact.AddSteps('Web element should be fetched using the JSON locator details. ',
                                    'Web element could not be fetched using the JSON locator details. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def getElement(self,driver,locVal,loc="xpath",enabled=True):
        if not globalVar.bln_SkipTestCase:
            try:
                if loc.lower() == "xpath":
                    locator = (By.XPATH,locVal)
                elif loc.lower() == "id":
                    locator = (By.ID,locVal)

                if enabled:
                    we = WebDriverWait(driver, globalVar.MTAFWebElementDelay).until(EC.element_to_be_clickable(locator))
                else:
                    we = WebDriverWait(driver, globalVar.MTAFWebElementDelay).until(EC.visibility_of_element_located(locator))
                return we
            except Exception as ex:
                print('Web element could not be fetched using ID/XPATH locator. ' + str(ex))
                reportFact.AddSteps('Web element should be fetched using ID/XPATH locator. ',
                                    'Web element could not be fetched using ID/XPATH locator: ' + locVal, strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def setData(self, webElem, strData):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                webElem.clear()
                time.sleep(globalVar.MTAFDelay)
                webElem.send_keys(strData)
                time.sleep(globalVar.MTAFDelay)
            except Exception as ex:
                print('Data ' + strData + ' could not be set to web element ' + webElem + '. ' + str(ex))
                reportFact.AddSteps('Data ' + strData + ' should be set to web element ' + webElem + '. ',
                                    'Data ' + strData + ' could not be set to web element ' + webElem + '. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def selectDropdownData(self, webElem, strData):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                select = Select(webElem)
                select.select_by_visible_text(strData)
            except Exception as ex:
                print('Data ' + strData + ' could not be selected from the dropdown ' + webElem + '. ' + str(ex))
                reportFact.AddSteps('Data ' + strData + ' should be selected from the dropdown ' + webElem + '. ',
                                    'Data ' + strData + ' could not be selected from the dropdown ' + webElem + '. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def selectDropdownDataByPartialText(self, webElem, strData):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                select = Select(webElem)
                for opt in select.options:
                    if strData in opt.text:
                        opt.click()
                        break
            except Exception as ex:
                print('Data ' + strData + ' could not be selected from the dropdown ' + webElem + '. ' + str(ex))
                reportFact.AddSteps('Data ' + strData + ' should be selected from the dropdown ' + webElem + '. ',
                                    'Data ' + strData + ' could not be selected from the dropdown ' + webElem + '. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def clickElement(self, webElem):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                webElem.click()
                time.sleep(1)
            except Exception as ex:
                print('Web element ' + webElem + ' could not be clicked. ' + str(ex))
                reportFact.AddSteps('Web element ' + webElem + ' should be clicked. ',
                                    'Web element ' + webElem + ' could not be clicked. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def moveToElement(self, webElem):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                ActionChains(selenium_driver.connect()).move_to_element(webElem).perform()
            except Exception as ex:
                print('Move to element action failed for Web element ' + webElem + '. ' + str(ex))
                reportFact.AddSteps('Move to element action should happen for Web element ' + webElem + '. ',
                                    'Move to element action failed for Web element ' + webElem + '. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True

    def isElementDisplay(self, we):
        if not globalVar.bln_SkipTestCase:
            try:
                return we.is_displayed()
            except Exception as ex:
                print('Web element ' + we + ' is not displayed. ' + str(ex))
                reportFact.AddSteps('Web element ' + we + ' should be displayed. ',
                                    'Web element ' + we + ' is not displayed. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def getElementText(self, we):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                return we.text
            except Exception as ex:
                print('Text for Web element ' + we + ' could not be fetched. ' + str(ex))
                reportFact.AddSteps('Text for Web element ' + we + ' should be fetched. ',
                                    'Text for Web element ' + we + ' could not be fetched. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def getElementAttributeValue(self, we, attribute):
        if not globalVar.bln_SkipTestCase:
            try:
                time.sleep(globalVar.MTAFDelay)
                return we.get_attribute(attribute)
            except Exception as ex:
                print('Data for ' + attribute + ' attribute of Web element ' + we + ' could not be fetched. ' + str(ex))
                reportFact.AddSteps('Data for ' + attribute + ' attribute of Web element ' + we + ' should be fetched. ',
                                    'Data for ' + attribute + ' attribute of Web element ' + we + ' could not be fetched. ', strPassFail="Fail")
                globalVar.bln_SkipTestCaseLog = True
                globalVar.bln_SkipTestCase = True
                return None

    def scrollPageUntilElementVisible(self, webElem):
        # selenium_driver.connect().execute_script("arguments[0].scrollIntoView(true);", webElem)
        time.sleep(globalVar.MTAFDelay)
        ActionChains(selenium_driver.connect()).move_to_element(webElem).perform()
