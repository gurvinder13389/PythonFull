from MTAF.Pages.HomePage import HomePage
from MTAF.ReusableFunctions import reportFact, globalVar
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory


class LoginPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.oDriverFunctions = DriverFunctions()
        self.oHome = HomePage()

    def setUsername(self, strData):
        we = self.weFact.getElementFromJson("LoginPage", "txtUsername")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('UserName should be entered', "UserName '" + strData + "' has been entered successfully.")

    def setPassword(self, strData):
        we = self.weFact.getElementFromJson("LoginPage", "txtPassword")
        self.weFact.setData(we, strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Password should be entered', "Password '" + strData + "' has been entered successfully.")

    def clickLogin(self):
        we = self.weFact.getElementFromJson("LoginPage", "btnLogin")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Login button should be clicked.', 'Login button clicked successfully.')

    def lissiaLogin(self):
        self.oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
        self.setUsername(globalVar.configData["userName"])
        self.setPassword(globalVar.configData["password"])
        self.clickLogin()

        self.oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
        self.oHome.pageVerify_Home()
        if globalVar.bln_SkipTestCase:
            globalVar.bln_SkipTestModule = True
        else:
            globalVar.bln_SkipTestCaseLog = False

    def lissiaLoginWithCredentials(self, username, password):
        if not globalVar.bln_SkipTestCase:
            self.oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            self.setUsername(username)
            self.setPassword(password)
            self.clickLogin()

            self.oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
            self.oHome.pageVerify_Home()
            if globalVar.bln_SkipTestCase:
                globalVar.bln_SkipTestModule = True
            else:
                globalVar.bln_SkipTestCaseLog = False
