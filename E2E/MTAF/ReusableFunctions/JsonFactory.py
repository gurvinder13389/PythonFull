import json
import os
from MTAF.ReusableFunctions import globalVar, reportFact


def getProjectPath():
    if not globalVar.bln_SkipTestCase:
        try:
            return os.path.join(os.path.dirname(__file__), "..")
        except Exception as ex:
            print('Project location could not be fetched. ' + str(ex))
            reportFact.AddSteps('Project location should be fetched. ',
                                'Project location could not be fetched. ',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True
            return None


#reusability by making a single fn for load.
def loadData():
    if not globalVar.bln_SkipTestCase:
        try:
            jsonObj = open(getProjectPath() + '/Resources/config.json')
            configJson = json.loads(jsonObj.read())
            jsonObj.close()
            return configJson
        except Exception as ex:
            print('Json file ' + getProjectPath() + '/Resources/config.json cannot be opened. ' + str(ex))
            reportFact.AddSteps('Json file ' + getProjectPath() + '/Resources/config.json should be opened. ',
                                'Json file ' + getProjectPath() + '/Resources/config.json cannot be opened. ',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True
            return None


def loadLocatorsData():
    if not globalVar.bln_SkipTestCase:
        try:
            jsonObj = open(getProjectPath() + '/Resources/locators.json')
            configJson = json.loads(jsonObj.read())
            jsonObj.close()
            return configJson
        except Exception as ex:
            print('Json file ' + getProjectPath() + '/Resources/locators.json cannot be opened. ' + str(ex))
            reportFact.AddSteps('Json file ' + getProjectPath() + '/Resources/locators.json should be opened. ',
                                'Json file ' + getProjectPath() + '/Resources/locators.json cannot be opened. ',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True
            return None


def getData(key):
    if not globalVar.bln_SkipTestCase:
        try:
            jsonObj = open(getProjectPath() + '/Resources/config.json')
            configJson = json.loads(jsonObj.read())
            jsonObj.close()
            return configJson[key]
        except Exception as ex:
            print('Key cannot be fetched from the json file ' + getProjectPath() + '/Resources/config.json. ' + str(ex))
            reportFact.AddSteps('Key should be fetched from the json file ' + getProjectPath() + '/Resources/config.json. ',
                                'Key cannot be fetched from the json file ' + getProjectPath() + '/Resources/config.json. ',strPassFail="Fail")
            globalVar.bln_SkipTestCaseLog = True
            globalVar.bln_SkipTestCase = True
            return None
