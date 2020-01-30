from MTAF.ReusableFunctions import globalVar, reportFact
from MTAF.ReusableFunctions.WebElementFactory import WebElementFactory
from MTAF.ReusableFunctions.WebTableFactory import WebTableFactory
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions


class QueuedTaskDiaryPage:
    def __init__(self):
        self.weFact = WebElementFactory()
        self.weTableFact = WebTableFactory()
        self.drivFunc = DriverFunctions()

    def clickRequest_a_Task(self):
        we = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "Request_a_Task")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Request_a_Task button should be clicked.', 'Request_a_Task button clicked successfully.')

    def clickOutstanding(self):
        we = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "chkOutstanding")
        self.weFact.clickElement(we)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Outstanding button should be clicked.', 'Outstanding button clicked successfully.')

    def getStatusByTaskId(self, taskId):
        we = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "QueuedTasksTable", enabled=False)
        weBtnNext = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "btnQueuedTaskPaginationNext")
        blnFlag = False
        iRowNumber = 0
        strStatus = ''

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 1, taskId)
                if iRowNumber > 0:
                    blnFlag = True
                    break
                else:
                    self.weFact.clickElement(weBtnNext)

            if blnFlag:
                strStatus = self.weTableFact.getCellData(we,iRowNumber,4)
                self.weTableFact.clickCell(we, iRowNumber, 1)
                if not globalVar.bln_SkipTestCaseLog:
                    reportFact.AddSteps('Status should be fetched.', "Fetched Status value is:'" + strStatus + "'.")
            else:
                strExpMsg = "Row with task id '" + taskId + "' should be present in the Queued Task table to fetch the status."
                strActMsg = "Row with task id '" + taskId + "' is not present in the Queued Task table."
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
        return strStatus

    def clickAndGetNextAvailableJob(self, taskId, jobName):
        we = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "QueuedTasksTable", enabled=False)
        weRun = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "QueuedTasksRunTable", enabled=False)
        weBtnNext = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "btnQueuedTaskPaginationNext")

        weJob = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "btnJob")
        self.weFact.clickElement(weJob)
        blnFlag = False
        newTaskId = 0

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 2, jobName)
                newTaskId = 0
                if iRowNumber > 0:
                    newTaskId = self.weTableFact.getCellData(we, iRowNumber, 1)
                    if int(taskId) < int(newTaskId):
                        self.weTableFact.clickCell(weRun, iRowNumber, 1)
                        blnFlag = True
                        break
                else:
                    self.weFact.clickElement(weBtnNext)

            if blnFlag and (newTaskId != 0) and not globalVar.bln_SkipTestCaseLog:
                reportFact.AddSteps("'" + jobName + "' should be fetch and click.", "'" + jobName + "' with task id '" + str(newTaskId) + "' fetched and clicked" )
            else:
                strExpMsg = "'" + jobName + "' should be fetched and click."
                strActMsg = "'" + jobName + "' is not present in the list."
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
        return newTaskId

    def taskProcessedAssert(self, strActStatus):
        self.drivFunc.MTAFAssert("Processed", strActStatus)
        if not globalVar.bln_SkipTestCaseLog:
            reportFact.AddSteps('Task status should be Processed',"Task status is Processed.")

    def scrollQueuedTaskTableUntilElementVisible(self, taskId):
        we = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "QueuedTasksTable", enabled=False)
        weBtnNext = self.weFact.getElementFromJson("QueuedTaskDiaryPage", "btnQueuedTaskPaginationNext")
        blnFlag = False

        if not globalVar.bln_SkipTestCase:
            while not blnFlag and self.weTableFact.get_row_count(we) > 1:
                iRowNumber = self.weTableFact.getRowNumOnColumnDataCompare(we, 1, taskId)
                if iRowNumber > 0:
                    blnFlag = True
                    webElem = we.find_elements_by_tag_name("tr")[iRowNumber].find_elements_by_tag_name("td")[1]
                    self.weFact.scrollPageUntilElementVisible(webElem)
                    break
                else:
                    self.weFact.clickElement(weBtnNext)

            if blnFlag and not globalVar.bln_SkipTestCaseLog:
                reportFact.AddSteps("Screen should be scrolled till task id '" + str(taskId) + "' is visible." , "Screen is scrolled till task id '" + str(taskId) + "' is visible")
            else:
                strExpMsg = "Screen should be scrolled till task id '" + str(taskId) + "' is visible."
                strActMsg = "Screen could not be scrolled until the task id '" + str(taskId) + "' is visible as it is not present in the list"
                self.drivFunc.MTAFAssertBoolean(blnFlag, strExpMsg, strActMsg)
