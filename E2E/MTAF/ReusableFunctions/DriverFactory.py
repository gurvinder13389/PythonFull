from selenium import webdriver
import os
from MTAF.ReusableFunctions import globalVar


class DriverFactory:
    _instance = None
    driver = None

    def __new__(cls, *args, **kwargs):
        try:
            if not cls._instance:
                cls._instance = super(DriverFactory, cls).__new__(cls, *args, **kwargs)
            return cls._instance
        except Exception as ex:
            print('Issue with driver factory class instantiation. ' + str(ex))
            # reportFact.AddSteps('DriverFactory class should be instantiated',
            #                     'Issue with driver factory class instantiation.',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True
            return None

    def connect(self):
        try:
            if self.driver is None:
                strDriverPath = os.path.join(os.path.dirname(__file__), "..")
                self.driver = webdriver.Chrome(executable_path=strDriverPath + globalVar.configData["chromePath"])
                self.launchApp()
                # self.driver.implicitly_wait(10)
            return self.driver
        except Exception as ex:
            print('Issue with web driver instantiation. ' + str(ex))
            # reportFact.AddSteps('Web Driver should be instantiated',
            #                     'Issue with Web driver instantiation.',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True
            return None

    def launchApp(self):
        try:
            self.driver.get(globalVar.configData["url"])
            self.driver.maximize_window()
        except Exception as ex:
            print('Application could not be launched. ' + str(ex))
            # reportFact.AddSteps('Application should be launched',
            #                     'Application could not be launched.',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True

    def launchUrl(self,strUrl):
        try:
            self.driver.get(strUrl)
        except Exception as ex:
            print('Url could not be launched. ' + str(ex))
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True

    def close(self):
        try:
            self.driver.quit()
            self.driver = None
        except Exception as ex:
            print('Issue with tear down of web driver instance. ' + str(ex))
            # reportFact.AddSteps('Webdriver instance should get closed.',
            #                     'Issue with tear down of web driver instance.',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True
