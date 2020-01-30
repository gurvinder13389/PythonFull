import pytest
import time
from MTAF.Pages.HomePage import HomePage
from MTAF.Pages.LoginPage import LoginPage
from MTAF.ReusableFunctions import globalVar, reportFact, ExcelUtil, selenium_driver
from MTAF.ReusableFunctions.DriverFunctions import DriverFunctions
from MTAF.Pages.ClaimElementPage import ClaimElementPage
from MTAF.Pages.ClaimPaymentPage import ClaimPaymentPage
from MTAF.Pages.ClaimsPage import ClaimsPage
from MTAF.Pages.PolicyServicingandEnquiriesPage import PolicyServicingandEnquiriesPage
from MTAF.Pages.TransactionsPage import TransactionsPage
from MTAF.Pages.TransactionEnquiryPage import TransactionEnquiryPage


class Test_Claims:
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
        global oClaimsPage
        global oClaimElementPage
        global oClaimPaymentPage
        global oTransactionsPage
        global oTransactionEnquiryPage

        oDriverFunctions = DriverFunctions()
        oLogin = LoginPage()
        oHome = HomePage()
        oPolicyServicingandEnquiriesPage = PolicyServicingandEnquiriesPage()
        oClaimsPage = ClaimsPage()
        oClaimElementPage = ClaimElementPage()
        oClaimPaymentPage = ClaimPaymentPage()
        oTransactionsPage = TransactionsPage()
        oTransactionEnquiryPage = TransactionEnquiryPage()

    def test_Claims(self, setUp, logFileAttr, beforeTestCase, initialize, request):
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

                # Fetch the policy on claim is to be applied
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oPolicyServicingandEnquiriesPage.setPolicy(dataDict['PolicyNo'][iKey])
                oDriverFunctions.keyPress('Tab')
                oPolicyServicingandEnquiriesPage.clickClaims()

                # Add a new Claim
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimsPage.clickAddaNewClaim()

                # Select Claimant, Benefit and Sub-Benefit
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimElementPage.selectClaimant('Active')
                time.sleep(1)
                oClaimElementPage.selectBenefit(dataDict['Benefit'][iKey])
                time.sleep(1)
                oClaimElementPage.selectSubBenefit(dataDict['SubBenefit'][iKey])
                time.sleep(1)
                sNotifiedDate = oClaimElementPage.getNotifiedDate()
                oClaimElementPage.setClaimDate(sNotifiedDate)
                oClaimElementPage.clickEnterorUpdateClaim()
                time.sleep(2)

                # Validate Policy status should be Death Notified and claim status should be Pending
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                policyStatus = oClaimsPage.getPolicyStatus()
                claimStatus = oClaimsPage.getClaimStatus(dataDict['SubBenefit'][iKey])
                oClaimsPage.policyStatusAssert('Death Notified', policyStatus)
                oDriverFunctions.setScreenShotFlag()
                oClaimsPage.claimStatusAssert('Pending', claimStatus)
                oDriverFunctions.takeScreenShot()
                oClaimsPage.clickClaimBenefitRow(dataDict['SubBenefit'][iKey], 'Pending')
                time.sleep(1)

                # Enter/Amend Claim Payment
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimElementPage.clickEnterorAmendClaimPayment()
                time.sleep(3)

                # Add Beneficiary and Bank details
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimPaymentPage.selectBeneficiary(str(dataDict['Beneficiary'][iKey]))
                time.sleep(1)
                oClaimPaymentPage.selectBankDetails()
                oDriverFunctions.setScreenShotFlag()
                oClaimPaymentPage.clickAcceptChanges()
                time.sleep(2)
                oDriverFunctions.takeScreenShot()
                oClaimPaymentPage.clickClose()

                # Change Status to Admitted
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimElementPage.selectChangeStatus('Admitted')
                oDriverFunctions.setScreenShotFlag()
                oClaimElementPage.clickAcceptStatusChange()
                oDriverFunctions.takeScreenShot()
                oDriverFunctions.goToInitialScreenAndExit()
                selenium_driver.close()
                selenium_driver.connect()
                oLogin.lissiaLoginWithCredentials(str(dataDict['Username'][iKey]), str(dataDict['Password'][iKey]))

                # Fetch the policy on which claim is to be applied
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oHome.clickPolicy()
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oPolicyServicingandEnquiriesPage.setPolicy(str(dataDict['PolicyNo'][iKey]))
                oDriverFunctions.keyPress('Tab')
                oPolicyServicingandEnquiriesPage.clickClaims()
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimsPage.clickClaimBenefitRow(dataDict['SubBenefit'][iKey], 'Admitted')
                time.sleep(1)

                # Enter/Amend Claim Payment
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimElementPage.clickEnterorAmendClaimPayment()
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimPaymentPage.selectClaimPayment()
                sPaymentAmount = oClaimPaymentPage.getPaymentAmount()
                oClaimPaymentPage.clickAuthorisePayment()
                time.sleep(1)
                oClaimPaymentPage.authorisedDateAssert()
                oClaimPaymentPage.authorisedTimeAssert()
                oDriverFunctions.setScreenShotFlag()
                oClaimPaymentPage.selectPaymentStatus('Paid')
                oDriverFunctions.takeScreenShot()
                oClaimPaymentPage.clickAcceptChangesandExit()

                # Change Status to Paid
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimElementPage.selectChangeStatus('Paid and Closed')
                oDriverFunctions.setScreenShotFlag()
                oClaimElementPage.clickAcceptStatusChange()
                oDriverFunctions.takeScreenShot()
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oClaimsPage.clickClose()

                # Validate policy status is Death Settlement
                oDriverFunctions.setScreenShotFlag()
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oPolicyServicingandEnquiriesPage.verifyStatusDeathSettlement()
                oDriverFunctions.takeScreenShot()
                time.sleep(2)
                oDriverFunctions.setScreenShotFlag()
                oPolicyServicingandEnquiriesPage.clickTransactions()
                oDriverFunctions.takeScreenShot()
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oTransactionsPage.doubleClickTransactionRecord(sNotifiedDate, 'Claim')

                # Verify transaction amount is equal to payment amount
                oDriverFunctions.switchFrameName(globalVar.configData["commonFrame"])
                oDriverFunctions.setScreenShotFlag()
                if sPaymentAmount is not None:
                    sPaymentAmount = f'{int(float(sPaymentAmount)):,}' + '.00'
                    oTransactionEnquiryPage.verifyAccountTransactionAmount(dataDict['TransactionAccount'][iKey], sPaymentAmount)
                oDriverFunctions.takeScreenShot()

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
                    ExcelUtil.setCellData(globalVar.testCaseName, rowCnt, 3, "Policy Number not generated by GoLive")
                    ExcelUtil.fillCellColor(globalVar.testCaseName, rowCnt, 3, 'FFFF0000')
                rowCnt = rowCnt + 1

        # Changing the bln_SkipTestCase to True when bln_IterationFailure is True, so that we could use the same
        # after test steps for both iterative and non-iterative test case summary report
        if globalVar.bln_IterationFailure:
            globalVar.bln_SkipTestCase = True
