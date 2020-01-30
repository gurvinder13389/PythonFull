SET mypath=%~dp0
cd %SOAPUI_PATH%
testrunner.bat -s"myTestSuite" -c"myTestCase" "%mypath%\getUserGroups-soapui-project.xml"