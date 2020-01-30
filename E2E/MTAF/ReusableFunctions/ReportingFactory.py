from MTAF.ReusableFunctions import globalVar


class ReportingFactory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not globalVar.bln_SkipTestCase:
            try:
                if not cls._instance:
                    cls._instance = super(ReportingFactory, cls).__new__(cls, *args, **kwargs)
                return cls._instance
            except Exception as ex:
                print('Issue with class instantiation. ' + str(ex))
                globalVar.reportMessage = 'Issue with class instantiation. '

    def getTestCaseName(self, TCName):
        return str(TCName).split("_")[1]

    def openAndCreateFile(self, testCaseName):
        globalVar.testCaseFilePath = globalVar.reportFolderPath + '/' + testCaseName + ".html"
        with open(globalVar.testCaseFilePath, 'a+') as oDetailedReport:
            self.createHeader(oDetailedReport)

    def createHeader(self, oDetailedReport):
        oDetailedReport.write("<html>")
        oDetailedReport.write("<title>Automation Execution Detailed Report</title>")
        oDetailedReport.write("<head></head>")
        oDetailedReport.write("<body>")
        oDetailedReport.write("<font face='Tahoma'size='2'>")
        oDetailedReport.write("<h1><center>Automation Detailed Execution Report</center></h1>")
        oDetailedReport.write("<br><center><b><font face='Tahoma' size='5'><a href='SummaryReport.html'>Summary "
                              "Report</a></center></h1>")
        oDetailedReport.write("<table border='1px solid black' width='100%' height='47'>")
        oDetailedReport.write("<tr>")
        oDetailedReport.write(
            "<td width='13%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
            "size='2'>TestCase Name</font></b></td>")
        oDetailedReport.write(
            "<td width='10%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
            "size='2'>StepNo</font></b></td>")
        oDetailedReport.write(
            "<td width='23%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
            "size='2'>Expected Result</font></b></td>")
        oDetailedReport.write(
            "<td width='22%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' size='2'>Actual "
            "Result</font></b></td>")
        oDetailedReport.write(
            "<td width='18%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
            "size='2'>Pass/Fail</font></b></td>")

    def addIterationStep(self):
        with open(globalVar.testCaseFilePath, 'a+') as oDetailedReport:
            oDetailedReport.write("<tr>")
            oDetailedReport.write(
                "<td width='13%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
                "size='2'>Iteration " + str(globalVar.iterationNum) + "</font></b></td>")
            oDetailedReport.write(
                "<td width='10%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
                "size='2'></font></b></td>")
            oDetailedReport.write(
                "<td width='23%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
                "size='2'></font></b></td>")
            oDetailedReport.write(
                "<td width='22%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
                "size='2'></font></b></td>")
            oDetailedReport.write(
                "<td width='18%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
                "size='2'></font></b></td>")
            globalVar.iterationNum = globalVar.iterationNum + 1

    def CreateSteps(self, strTestCaseName, strStepNo, strExpectedResult, strActualResult, strPassFail):
        with open(globalVar.testCaseFilePath, 'a+') as oDetailedReport:
            oDetailedReport.write("<tr>")
            oDetailedReport.write(
                "<td width='13%' bgcolor='#FFFFFF' valign='top' align='center'><font color='#000000' face='Tahoma' "
                "size='2'>" + strTestCaseName + "</td>")
            oDetailedReport.write(
                "<td width='10%' bgcolor='#FFFFFF' valign='top' align='center'><font color='#000000' face='Tahoma' "
                "size='2'>" + strStepNo + "</td>")
            oDetailedReport.write(
                "<td width='23%' bgcolor='#FFFFFF' valign='top' align='center'><font color='#000000' face='Tahoma' "
                "size='2'>" + strExpectedResult + "</td>")
            oDetailedReport.write(
                "<td width='22%' bgcolor='#FFFFFF' valign='top' align='center'><font color='#000000' face='Tahoma' "
                "size='2'>" + strActualResult + "</td>")
            if strPassFail == "Pass":
                if globalVar.bln_takeScreenshot:
                    globalVar.screenShotPath = globalVar.reportFolderPath + "/Screenshots/" + globalVar.testCaseName + \
                                               str(globalVar.screenShotCounter) + ".png"
                    oDetailedReport.write(
                        "<td width='18%' bgcolor='#FFFFFF' valign='middle' align='center'><b><font color='Green' "
                        "face='Tahoma' size='2'><a href = Screenshots/" + globalVar.testCaseName + str(
                            globalVar.screenShotCounter) + ".png >" + strPassFail + "</a></font></b></td>")
                    globalVar.screenShotCounter = globalVar.screenShotCounter + 1
                else:
                    oDetailedReport.write(
                    "<td width='18%' bgcolor='#FFFFFF' valign='middle' align='center'><b><font color='Green' "
                    "face='Tahoma' size='2'>" + strPassFail + "</font></b></td>")
            else:
                globalVar.screenShotPath = globalVar.reportFolderPath + "/Screenshots/" + globalVar.testCaseName + \
                                           str(globalVar.screenShotCounter) + ".png"
                oDetailedReport.write(
                    "<td width='18%' bgcolor='#FFFFFF' valign='middle' align='center'><b><font color='Red' "
                    "face='Tahoma' size='2'><a href = Screenshots/" + globalVar.testCaseName + str(
                        globalVar.screenShotCounter) + ".png ><font color='FF0000'>" + strPassFail +
                    "</font></a></font></b></td>")
                globalVar.screenShotCounter = globalVar.screenShotCounter + 1
            globalVar.bln_takeScreenshot = False

    def AddSteps(self, strExpectedResult, strActualResult, strPassFail="Pass"):
        if not globalVar.bln_SkipTestCaseLog:
            self.CreateSteps(globalVar.testCaseName, str(globalVar.testStepNum),
                             strExpectedResult, strActualResult, strPassFail)
            globalVar.testStepNum = globalVar.testStepNum + 1

    def closeFile(self):
        with open(globalVar.testCaseFilePath, 'a+') as oDetailedReport:
            oDetailedReport.write("</table>")
            oDetailedReport.write("</font>")
            oDetailedReport.write("</body>")
            oDetailedReport.write("</html>")

    def openAndCreateSummaryFile(self):
        globalVar.summaryFilePath = globalVar.reportFolderPath + '\\SummaryReport.html'
        with open(globalVar.summaryFilePath, 'a+') as oSummaryReport:
            self.createSummaryHeader(oSummaryReport)

    def createSummaryHeader(self, oSummaryReport):
        oSummaryReport.write("<html>")
        oSummaryReport.write("<title>Automation Execution Summary Report</title>")
        oSummaryReport.write("<head></head>")
        oSummaryReport.write("<body>")
        oSummaryReport.write("<font face='Tahoma'size='2'>")
        oSummaryReport.write("<h1><center>Automation Summary Execution Report</center></h1>")
        oSummaryReport.write("<table border='1px solid black' width='100%' height='47'>")
        oSummaryReport.write("<tr>")
        oSummaryReport.write(
            "<td width='50%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
            "size='2'>TestCase Name</font></b></td>")
        oSummaryReport.write(
            "<td width='50%' bgcolor='#CCCCFF' align='center'><b><font color='#000000' face='Tahoma' "
            "size='2'>Pass/Fail</font></b></td>")

    def AddSummarySteps(self, strTestCaseName, strPassFail):
        with open(globalVar.summaryFilePath, 'a+') as oSummaryReport:
            oSummaryReport.write("<tr>")
            if strPassFail == "Abort":
                oSummaryReport.write(
                    "<td width='50%' bgcolor='#FFFFFF' valign='top' align='center'><font color='#000000' "
                    "face='Tahoma' size='2'>" + strTestCaseName + "</td>")
            else:
                oSummaryReport.write(
                    "<td width='50%' bgcolor='#FFFFFF' valign='top' align='center'><font color='#000000' "
                    "face='Tahoma' size='2'><a href ='" + strTestCaseName + ".html'>" + strTestCaseName + "</a></td>")
            if strPassFail == "Pass":
                oSummaryReport.write(
                    "<td width='50%' bgcolor='#FFFFFF' valign='middle' align='center'><b><font color='Green' "
                    "face='Tahoma' size='2'>" + strPassFail + "</font></b></td>")
            else:
                if strPassFail == "Abort":
                    oSummaryReport.write(
                        "<td width='50%' bgcolor='#FFFFFF' valign='middle' align='center'><b><font color='Red' "
                        "face='Tahoma' size='2'><font color='FF0000'>" + strPassFail + "-Due to prerequisite "
                                                                                       "failure.</font></font></b></td>")
                else:
                    oSummaryReport.write(
                        "<td width='50%' bgcolor='#FFFFFF' valign='middle' align='center'><b><font color='Red' "
                        "face='Tahoma' size='2'><font color='FF0000'>" + strPassFail + "</font></font></b></td>")

    def closeSummaryFile(self):
        with open(globalVar.summaryFilePath, 'a+') as oSummaryReport:
            oSummaryReport.write("</table>")
            oSummaryReport.write("</font>")
            oSummaryReport.write("</body>")
            oSummaryReport.write("</html>")

    def resetReportFlags(self):
        globalVar.bln_SkipTestCase = False
        globalVar.bln_SkipTestCaseLog = False
        globalVar.testStepNum = 1
        globalVar.screenShotCounter = 1
