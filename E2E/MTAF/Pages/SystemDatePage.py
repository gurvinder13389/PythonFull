from MTAF.ReusableFunctions import reportFact, globalVar
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions


class SystemDatePage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.drivFunc = DriverFunctions()

    def setSystemDate(self,strData):
        we = self.weFact.getElementFromJson("SystemDatePage", "txtSystemDate")
        self.weFact.setData(we,strData)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('System Date should be entered', "System Date '" + strData + "' has been entered successfully.")

    def getSystemDate(self):
        we = self.weFact.getElementFromJson("SystemDatePage", "txtLissiaSystemDate", enabled=False)
        sysDate = self.weFact.getElementAttributeValue(we, "value")
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('System Date should be fetched.', "Fetched system date value is:'" + sysDate + "'.")
        return sysDate

    def clickOK(self):
        we = self.weFact.getElementFromJson("SystemDatePage", "btnOK")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Ok button should be clicked.', 'Ok button clicked successfully.')

    def systemDateAssert(self, strExpSysDate):
        strActDate = self.getSystemDate()
        self.drivFunc.MTAFAssert(strExpSysDate,strActDate)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('System Date should update.',"System Date updated successfully.")
