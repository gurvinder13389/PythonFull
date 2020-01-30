Public strGoLive,strCurDir, selectedVal, strSelectedValue, objIE1, objExcel, objWB, strTagPrefix, strResponseTag, strExpSheetName, strTestCaseNameResponse, iDataRowPos, strProgressTitle, strMax, objFolder, blnTestCaseIdAtRowOne, iNodeRowNumber, blnDataAdded, dictTC, strParameters, usedRangeRNum, blnSheetFound, strResponsePath

With CreateObject("shell.application")
	.MinimizeAll
End With

strCurDir = WScript.Arguments(0)
strParameters = WScript.Arguments(1)
strGoLive = Trim(Split(strParameters, ",")(2))
strSelectedWS = Trim(Split(strParameters, ",")(0))
blnWSExecute = updateEndPoint(strSelectedWS)

If blnWSExecute Then
	Set objExcel = CreateObject("Excel.Application")
	initStart strCurDir & "\" & strSelectedWS

	objExcel.Quit
	Set objExcel = Nothing		
Else
	MsgBox "Invalid END POINT or WSDL.txt file is missing for the selected webservice."
End If

Function updateEndPoint(selectedValue)
	blnUpdate = true
	Const ForReading = 1
	Const ForWriting = 2	
	
	Set objFSO = CreateObject("Scripting.FileSystemObject")	
	Set objFolder = objFSO.GetFolder(strCurDir & "\" & selectedValue)
	Set colfiles = objFolder.Files
	strXmlPath = ""
	strWsdlTextPath = ""
	strNewString = ""
	For Each objFile In colfiles
		If StrComp(Right(objFile.Name, 3), "xml") = 0 Then
			strXmlPath = strCurDir & "\" & selectedValue & "\" & objFile.Name
		ElseIf StrComp(Right(objFile.Name, 3), "txt") = 0 Then
			strWsdlTextPath = strCurDir & "\" & selectedValue & "\" & objFile.Name
			Set objFile = objFSO.OpenTextFile(strWsdlTextPath, ForReading)
			strWsdl = Trim(objFile.ReadLine)
			If StrComp(LCase(Left(strWsdl, 4)), "http") = 0 Then
				If StrComp(LCase(Right(strWsdl, 4)), "wsdl") = 0 Then
					strWsdl = Replace(strWsdl, "?wsdl", "")
					strWsdl = Replace(strWsdl, "wsdl", "")
					strWsdl = Replace(strWsdl, "?WSDL", "")
					strWsdl = Replace(strWsdl, "WSDL", "")
				End If
				strNewString = strWsdl
			Else						
				blnUpdate = false
				updateEndPoint = blnUpdate
				Exit Function
			End If
		End If
	Next
	If strcomp(trim(strNewString),"") = 0 then
		blnUpdate = false
		updateEndPoint = blnUpdate
		Exit Function
	End If
	
	Set objFolder = Nothing
	Set colfiles = Nothing
	
	Set objFile = objFSO.OpenTextFile(strXmlPath, ForReading)			
	strText = objFile.ReadAll
	
	strPrefix = "<soap:address location="
	intPrefix = InStr(1, strText, strPrefix)
	intPrefix = intPrefix + Len(strPrefix) + 1
	strSuffix = "/>"
	intSuffix = InStr(intPrefix, strText, strSuffix) - 1
	
	strOldString = Mid(strText, intPrefix, intSuffix - intPrefix)			
	objFile.Close
	strNewText = Replace(strText, strOldString, strNewString)
	Set objFile = objFSO.OpenTextFile(strXmlPath, ForWriting)
	objFile.WriteLine strNewText
	
	objFile.Close
	Set objFile = Nothing
	Set objFSO = Nothing
	updateEndPoint = blnUpdate
End Function

Sub initStart(selectedVal)
	On Error Resume Next
	selectedVal = replace(selectedVal,"$"," ")

	'----Moving the already present files in Request and Response folders
	fileTransfer selectedVal
	
	arrVal = split(selectedVal,"\")
	strSelectedValue = arrVal(UBound(arrVal))
	
	Set objFSO = CreateObject("Scripting.FileSystemObject")
	Set objFolder = objFSO.GetFolder(selectedVal)
	Set colfiles = objFolder.Files
	Dim CurrentDirectory
	fileCounter = 0
	
	InitializeIE
	sbwait 2
	strMax = 4
	CreateProgressBar
	
	sGoLivePolTag = Trim(Split(strParameters,",")(1))
	
	If Strcomp(sGoLivePolTag, "") <> 0 Then
		backUpFile
		createTestDataTemplate
	End If

	For Each objFile In colfiles
		If InStr(1, objFile.Name, strSelectedValue)> 0 And Strcomp(Right(objFile.Name, 4), "xlsx") = 0 Then
			strWBPath = selectedVal & "\" & objFile.Name
			InitializeObjects strWBPath
			ClearRunnerSheet
			strProgressTitle = Split(objFile.Name,".")(0)
			
			UpdateTitle strProgressTitle
			'----Getting values from Base sheet
			strTagPrefix = Trim(objExcel.WorksheetFunction.Index(objWB.Worksheets("Base").Range("2:2"), objExcel.WorksheetFunction.Match("RequestPrefix", objWB.Worksheets("Base").Range("1:1"), 0)))
			
			CurrentDirectory = objWB.Path
			strRequestPath = CurrentDirectory & "\Request"

			If Not objFSO.FolderExists(strRequestPath) Then
				objFSO.CreateFolder strRequestPath
			End If
			
			strFileName = ""
			iRow = 2
			
			JSProgressCounter "Request",1,4
			intTotalTestCases = cint(objExcel.WorksheetFunction.CountA(objWB.Worksheets("Runner").Range("A:A")))-1
			intTotalYes = intTotalTestCases - cint(objExcel.WorksheetFunction.CountIf(objWB.Worksheets("Runner").Range("B:B"),"n"))
			iRequestBarCount = 0
			
			'Function call for copying GoLive policies to the required service test data template
			'Pre-requisite - Service using the policy ids generated from GoLive should have the same suffix of the test data template as it is of the GoLive test data template			
			Set dictTC = CreateObject("Scripting.Dictionary")		
			If Strcomp(sGoLivePolTag, "") <> 0 Then
				copyStaticData
				strSuffix = Mid(Split(objFile.Name, ".")(0), InStr(1, Split(objFile.Name, ".")(0), strSelectedValue) + Len(strSelectedValue))
				deleteTemplateRow
				copyPolicyToServiceTestDataTemplate sGoLivePolTag, strSuffix
			End If
			
			Do
				strTCName = ""
				If StrComp(LCase(Trim(objWB.Worksheets("Runner").Cells(iRow, 2).Value)), "n") <> 0 Then
					strFileName = Trim(objWB.Worksheets("Runner").Cells(iRow, 1).Value)
					strTCName = Trim(objWB.Worksheets("Runner").Cells(iRow, 1).Value)
					If StrComp(Trim(strFileName), "") = 0 Then
						Exit Do
					Else
						'---Removing .xlsm from filename
						strTempFileName = objWB.Name
						strTempFileName = Mid(strTempFileName, 1, InStrRev(strTempFileName, ".") - 1)
						strFileName = strTempFileName & "_"& strFileName
					End If
					
					If (Strcomp(sGoLivePolTag, "") <> 0 And dictTC.exists(Trim(objWB.Worksheets("Runner").Cells(iRow, 1).Value))) Or (Strcomp(sGoLivePolTag, "") = 0) Then
						strFileNameWithPath = strRequestPath & "\" & strFileName & ".xml"
						objFSO.CreateTextFile strFileNameWithPath
						Executor strFileNameWithPath, strTCName
					End If
					
					If Strcomp(sGoLivePolTag, "") <> 0 And not dictTC.exists(Trim(objWB.Worksheets("Runner").Cells(iRow, 1).Value)) Then
						objWB.Worksheets("Runner").Cells(iRow, 4).Value = "GoLive Policy not generated for this test case"
						objWB.Worksheets("Runner").Cells(iRow, 5).Value = "Fail"
						objWB.Worksheets("Runner").Cells(iRow, 5).Interior.ColorIndex = 3
					End If
					iRequestBarCount = iRequestBarCount + 1 
					JSProgressCounterSubTasks "Request",1,4,"Request Creation",Cstr(iRequestBarCount),Cstr(intTotalYes)
				End If
				iRow = iRow + 1
			Loop
			
			JSProgressCounter "Sending Soap Requests",2,4
			runBatchFile selectedVal
			'---Soap Progress-----------
			soapProgess "Soap Response generated"
			'---------------------------
			JSProgressCounter "Soap Response generated",3,4
			sbWait 2
			ResponseRunner
			JSProgressCounter "Soap Response Added to excel",4,4
			sbWait 2
			fileCounter = fileCounter + 1
			finalXMLFileTransfer selectedVal , Split(objFile.Name, ".")(0)
			'-----------Validation Code-----------------------------------
			Set oXMLFile = CreateObject("Microsoft.XMLDOM")
	
			iTestCaseName = 1
			iSheetName = 2
			iFieldHierarchy = 3
			iExpectedValue = 4
			iActualValue = 5
			iStatus = 6
			iIteration = 7
			
			Set objValWS = objWB.Worksheets("Validation")
			
			For iRow = 2 To objValWS.UsedRange.Rows.Count
				strTestCaseName = objValWS.Cells(iRow, iTestCaseName).Value
				
				strFN = Mid(objFile.Name, 1, InStrRev(objFile.Name, ".") - 1)				
				strFullFN = strResponsePath & "\" & strFN & "_" & strTestCaseName & "_Response.xml"				
				oXMLFile.Load (strFullFN)
				
				blnSheetFound = True
				iRowNodeCount = 1
				
				strSheetName = objValWS.Cells(iRow, iSheetName).Value
				strHierarchy = objValWS.Cells(iRow, iFieldHierarchy).Value
				strExpected = objValWS.Cells(iRow, iExpectedValue).Value
				strIteration = objValWS.Cells(iRow, iIteration).Value
				
				if isnumeric(strIteration) then
					strIteration = cint(strIteration)
				End If
				
				Set oSheetNode = getNode(oXMLFile, strSheetName)
				
				arrHierarchy = Split(strHierarchy, ">")
				
				Set oHierarchyNode = oSheetNode
				
				strHierarchyData = ""
				If strIteration <= oHierarchyNode.ChildNodes.Length Then
					If StrComp(arrHierarchy(0), "row") = 0 Then
						For Each oChildNode In oHierarchyNode.ChildNodes
							If StrComp(LCase(oChildNode.BaseName), LCase("row")) = 0 Then
								If strIteration = iRowNodeCount Then
									Set oHierarchyNode = oChildNode
									'----"following line will exclude 'row<' from the whole string to get the remaining string"
									strHierarchy = Right(strHierarchy, Len(strHierarchy) - 4)
									arrHierarchy = Split(strHierarchy, ">")
									Exit For
								End If
								iRowNodeCount = iRowNodeCount + 1
							End If
						Next
					End If
					
					For Each strVal In arrHierarchy
						blnSheetFound = True
						Set oHierarchyNode = getNode(oHierarchyNode, strVal)
					Next
					strHierarchyData = oHierarchyNode.Text
				Else
					strHierarchyData = "Not Found. Check the iteration number."
				End If
				
				If Err.Number <> 0 Then
					strHierarchyData = "Not Found. Check the Hierarchy or sheet Name."
				End If
				
				Err.Clear
				
				
				'For Each strVal In arrHierarchy
				'	blnSheetFound = True
				'	Set oHierarchyNode = getNode(oHierarchyNode, strVal)
				'Next							
				'msgbox oHierarchyNode.Text							
				'objValWS.Cells(iRow, iActualValue).Value = oHierarchyNode.Text
				objValWS.Cells(iRow, iActualValue).NumberFormat = "@"
				objValWS.Cells(iRow, iActualValue).Value = strHierarchyData
				
				If strcomp(objValWS.Cells(iRow, iExpectedValue).Value,objValWS.Cells(iRow, iActualValue).Value) = 0 then
					objValWS.Cells(iRow, iStatus).Value = "Pass"
					objValWS.Cells(iRow, iStatus).Interior.ColorIndex = 4
				Else
					objValWS.Cells(iRow, iStatus).Value = "Fail"
					objValWS.Cells(iRow, iStatus).Interior.ColorIndex = 3
				End If
				
			Next
			
			'-------------------------------------------------------------
			
			TearDown
			Set dictTC = Nothing
		End If
		deleteTemplateRow
	Next
	
	If instr(strSelectedValue, strGoLive) > 0 Then
		copyGoLivePoliciesToCSV selectedVal, colfiles
	End If
	
	If fileCounter = 0 Then
		msgbox "Input template FileName and Folder name mismatch!!!!"
		msgbox "Input template FileName and Folder Name should be same."
		''''' message saying file didn't present
	End If
	
	TeardownIE
	Set objFolder = Nothing
	Set colFiles = Nothing
	Set objReqFolder = Nothing
	Set objFSO = Nothing
End Sub

Function getNode(oNode, strSheetName)
    If StrComp(LCase(oNode.BaseName), LCase(strSheetName)) = 0 Then
        Set getNode = oNode
        blnSheetFound = False
    End If

    If oNode.ChildNodes.Length > 0 Then
        For Each oChildNode In oNode.ChildNodes
            If blnSheetFound Then
                Set getNode = getNode(oChildNode, strSheetName)
            End If
        Next
    Else
        Set getNode = Nothing
    End If
End Function

Sub InitializeIE()
	Set objIE1 = CreateObject("InternetExplorer.Application")

	objIE1.Navigate "about:blank"
	objIE1.ToolBar = 0
	objIE1.StatusBar = 0
	objIE1.Left = 450
	objIE1.Top = 250
	objIE1.Width = 350
	objIE1.Height = 150
	objIE1.Visible = 1
End Sub

Sub TeardownIE()
	'objIE1.Quit
	KillAll "iexplore.exe"
	Set objIE1 = Nothing
End Sub

Sub fileTransfer(strFtPath)
	Dim StrNewFolderName
	Set oFtFso = CreateObject("Scripting.FileSystemObject")
	strReq = strFtPath & "\Request"
	strRes = strFtPath & "\Response"
		
	Set objReqFolder = oFtFso.GetFolder(strReq)
	Set colReqFiles = objReqFolder.Files
	
	Set objResFolder = oFtFso.GetFolder(strRes)
	Set colResFiles = objResFolder.Files
	blnFirst = True
	StrNewFolderName = ""
	'---Moving Request Files
	For Each oFile In colReqFiles
		If blnFirst Then
			StrNewFolderName = Replace(Replace(Replace(CStr(CDate(oFile.DateLastModified)), " ", "_"), "/", "_"), ":", "_")
			oFtFso.CreateFolder strReq & "\" & StrNewFolderName
			oFtFso.CreateFolder strRes & "\" & StrNewFolderName
		End If
		blnFirst = False
		
		oFile.Move strReq & "\" & StrNewFolderName & "\"        
	Next
	
	For Each oFile In colResFiles
		If blnFirst Then
			StrNewFolderName = Replace(Replace(Replace(CStr(CDate(oFile.DateLastModified)), " ", "_"), "/", "_"), ":", "_")
			oFtFso.CreateFolder strReq & "\" & StrNewFolderName
			oFtFso.CreateFolder strRes & "\" & StrNewFolderName
		End If
		blnFirst = False
		oFile.Move strRes & "\" & StrNewFolderName & "\"
	Next
	
	Set oFtFso = Nothing
	Set objReqFolder = Nothing
	Set colReqFiles = Nothing
	Set objResFolder = Nothing
	Set colResFiles = Nothing
End Sub

Sub InitializeObjects(strWBPath)			
	Set objWB = objExcel.Workbooks.Open(strWBPath)
End Sub

Sub ClearRunnerSheet()
	If StrComp(objWB.Worksheets("Runner").Cells(1, 4).Value, "ResponseCaptured") = 0 And StrComp(objWB.Worksheets("Runner").Cells(1, 5).Value, "Status") = 0 Then
		iRow = 2
		Do While iRow <= objWB.Worksheets("Runner").UsedRange.Rows.Count
			objWB.Worksheets("Runner").Cells(iRow, 4).Value = ""
			objWB.Worksheets("Runner").Cells(iRow, 5).Clear
			iRow = iRow + 1
		Loop
	End If
End Sub

Sub copyStaticData()
	For Each sName In objWB.Worksheets
        If InStr(1, sName.Name, "Req_") = 1 Then
			iTemplateRow = objExcel.WorksheetFunction.Match("Template", objWB.Worksheets(sName.Name).Range("A:A"), 0)
			If objWB.Worksheets(sName.Name).UsedRange.Columns.Count > 2 Then
				objWB.Worksheets(sName.Name).Range("C" & iTemplateRow & ":" & ColumnLetter(objWB.Worksheets(sName.Name).UsedRange.Columns.Count) & iTemplateRow).copy objWB.Worksheets(sName.Name).Range("C" & (iTemplateRow + 1) & ":" & ColumnLetter(objWB.Worksheets(sName.Name).UsedRange.Columns.Count) & objWB.Worksheets(sName.Name).UsedRange.Rows.Count)
			End If
        End If
    Next
End Sub

Sub Executor(FilePath, TestCaseName)
	strFileNameWithPath = FilePath
	Set objFSO = CreateObject("Scripting.FileSystemObject")
	Set f = objFSO.OpenTextFile(strFileNameWithPath, 8)
	iExecutorRow = 1
	Do while iExecutorRow <= objWB.Worksheets("Base").UsedRange.Rows.Count
		strVal = Trim(objWB.Worksheets("Base").Cells(iExecutorRow, 1).Value)
		
		If StrComp(strVal, "") = 0 Then
			Exit Do
		ElseIf StrComp(strVal, "Go") = 0 Then
			f.Close
			Set f = objFSO.OpenTextFile(strFileNameWithPath, 8)
			CreateDynamicRequest f, TestCaseName
		Else
			f.Write strVal
		End If
		iExecutorRow = iExecutorRow + 1
	Loop      
	f.Close
	Set objFSO = Nothing
	Set f = Nothing
End Sub

Sub CreateDynamicRequest(ofile, TestCaseName)
	For Each wks In objWB.Worksheets			
		 If InStr(1, wks.Name, "Req_") = 1 Then
			strMappedSheetNode = mappedNode(wks.Name)
			CreateNodes ofile, strMappedSheetNode, TestCaseName
		 End If
	Next
End Sub

Function mappedNode(sheetName)
	iRowNumTemp = 2
	If InStr(1, sheetName, "Map_") > 0 Then
		Do While iRowNumTemp <= objWB.Worksheets("SheetMapper").UsedRange.Rows.Count
			If StrComp(Trim(objWB.Worksheets("SheetMapper").Cells(iRowNumTemp, 2).Value), sheetName) = 0 Then
				Exit Do
			End If
			iRowNumTemp = iRowNumTemp + 1
		Loop
		sheetName = Trim(objWB.Worksheets("SheetMapper").Cells(iRowNumTemp, 1).Value)
	End If
	mappedNode = sheetName
End Function

Function mappedSheet(oNodeName)
	iRowNumTemp = 2
	mappedSheetFound = False
	Do While iRowNumTemp <= objWB.Worksheets("SheetMapper").UsedRange.Rows.Count
		If StrComp(Trim(objWB.Worksheets("SheetMapper").Cells(iRowNumTemp, 1).Value), oNodeName) = 0 Then
			mappedSheetFound = True
			Exit Do
		End If
		iRowNumTemp = iRowNumTemp + 1
	Loop
	
	If mappedSheetFound Then
		sheetName = Trim(objWB.Worksheets("SheetMapper").Cells(iRowNumTemp, 2).Value)
	Else
		sheetName = oNodeName
	End If
	mappedSheet = sheetName
End Function

Sub CreateNodes(f, SheetName, TestCaseName)
	'TestCaseName for TestData filteration
	sheetNodeName = Mid(SheetName, 5)
	SheetName = mappedSheet(SheetName)
	
	f.Write "<" & strTagPrefix & sheetNodeName & ">" & vbNewLine
	
	iTotalRows = objWB.Worksheets(SheetName).UsedRange.Rows.Count
	Set Rng = objWB.Worksheets(SheetName).Range("A1:A" & iTotalRows) 
	
	If IsNumeric(TestCaseName) Then
		TestCaseName = CInt(TestCaseName)
	End If
	
	iRNum = objExcel.WorksheetFunction.Match(TestCaseName, Rng, 0)
	strRowNums = ""
	Do while iRNum <= objWB.Worksheets(SheetName).UsedRange.Rows.Count
		strTCNameTemp = Trim(objWB.Worksheets(SheetName).Cells(iRNum, 1).Value)
		
		If StrComp(strTCNameTemp, TestCaseName) = 0 Then
			strRowNums = strRowNums & "," & CStr(iRNum)
		ElseIf StrComp(strTCNameTemp, "") = 0 Then
			Exit Do
		End If
		iRNum = iRNum + 1
	Loop	
	
	'Exit for Null Data
	arrRowNums = Split(Right(strRowNums, Len(strRowNums) - 1), ",")
	'--- For all row numbers
	For iRNums = 0 To UBound(arrRowNums)
		iRowNumber = arrRowNums(iRNums)
		strSheetName = SheetName
		strHierarcy = ""
		iRowNum = 1
		' Loop to check the existance of 'TestCaseId'
		Do while iRowNum <= objWB.Worksheets(strSheetName).UsedRange.Rows.Count
			If StrComp(Trim(objWB.Worksheets(strSheetName).Cells(iRowNum, 1).Value), "TestCaseId") = 0 Then
				Exit Do
			Else
				strHierarcy = strHierarcy & ","
			End If
			iRowNum = iRowNum + 1
		Loop
		
		iHierarchyDepth = UBound(Split(strHierarcy, ","))
		If iHierarchyDepth = -1 Then
			iHierarchyDepth = 0
		End If
		iParamStartRow = iHierarchyDepth + 1
			
		iColCount = objExcel.WorksheetFunction.CountA(objWB.Worksheets(strSheetName).Range(CStr(iParamStartRow) & ":" & CStr(iParamStartRow)))
	   
		strXml = ""
		'---- For deleting the last comma
		If Len(strHierarcy) > 0 Then
			strHierOld = Left(strHierarcy, Len(strHierarcy) - 1)
		Else
			strHierOld = ""
		End If        
		
		For iCol = 3 To iColCount
			strColumnName = objWB.Worksheets(strSheetName).Cells(iParamStartRow, iCol).Value
			arrHierOld = Split(strHierOld, ",")
			blnDataWrite = False
			strHierNew = ""
			For iHierRow = iHierarchyDepth To 1 Step -1
				strParent = objWB.Worksheets(strSheetName).Range(ColumnLetter(iCol) & CStr(iHierRow)).MergeArea.Cells(1, 1).Value
				strOldParent = arrHierOld(iHierRow - 1)
				If StrComp(strParent, strOldParent) = 0 Then
					If Not (blnDataWrite) Then
						If Len(strHierNew) <> 0 Then
							strHierNewTemp = Left(strHierNew, Len(strHierNew) - 1)
							arrHierNewTemp = Split(strHierNewTemp, ",")
							For iHierNewTemp = 0 To UBound(arrHierNewTemp)
								strXml = strXml & "<" & strTagPrefix & arrHierNewTemp(iHierNewTemp) & ">" & vbNewLine
							Next
						End If
						'---Data
						Data = objWB.Worksheets(strSheetName).Cells(iRowNumber, iCol).Value
						strXml = strXml & "<" & strTagPrefix & strColumnName & ">" & Data & "</" & strTagPrefix & strColumnName & ">" & vbNewLine
						blnDataWrite = True
					Else
						blnDataWrite = True
					End If
					strHierNew = strParent & "," & strHierNew
				Else
					'---Adding New Tags and CLosing old one's
					If StrComp(strOldParent, "") <> 0 Then
						strXml = strXml & "</" & strTagPrefix & strOldParent & ">" & vbNewLine
					End If
					strHierNew = strParent & "," & strHierNew
				End If
			Next
			
			'--- If data is still not entered then firstly hierarchy needs to add
			If Not (blnDataWrite) Then
				If Len(strHierNew) > 0 Then
					strHierNew = Left(strHierNew, Len(strHierNew) - 1)
				End If
				arrHierNew = Split(strHierNew, ",")
				For iHierNew = 0 To UBound(arrHierNew)
					strXml = strXml & "<" & strTagPrefix & arrHierNew(iHierNew) & ">" & vbNewLine
				Next
				'---Data
				Data = objWB.Worksheets(strSheetName).Cells(iRowNumber, iCol).Value
				strXml = strXml & "<" & strTagPrefix & strColumnName & ">" & Data & "</" & strTagPrefix & strColumnName & ">" & vbNewLine
			End If
			If StrComp(Right(strHierNew, 1), ",") = 0 Then
				strHierNew = Left(strHierNew, Len(strHierNew) - 1)
			End If
			strHierOld = strHierNew
			strHierNew = ""
		Next
		arrHierOldTemp = Split(strHierOld, ",")
		For iHierOldTemp = UBound(arrHierOldTemp) To 0 Step -1
			strXml = strXml & "</" & strTagPrefix & arrHierOldTemp(iHierOldTemp) & ">" & vbNewLine
			'strXml = strXml & "/" & arrHierOldTemp(iHierOldTemp) & vbNewLine
		Next
		f.Write strXml
	Next
	
	f.Write "</" & strTagPrefix & sheetNodeName & ">"
	Set Rng = Nothing
End Sub

Public Function ColumnLetter(ColumnNumber)
	BlnDo = True
	If IsNumeric(ColumnNumber) Then
		ColumnNumber = CInt(ColumnNumber)
	ElseIf ColumnNumber = "" Then
		BlnDo = False
	End If
	If BlnDo Then
		If ColumnNumber > 26 Then
			ColumnLetter = Chr(Int((ColumnNumber - 1) / 26) + 64) & Chr(((ColumnNumber - 1) Mod 26) + 65)
		Else
			ColumnLetter = Chr(ColumnNumber + 64)
		End If
	Else
		ColumnLetter = ""
	End If
End Function

Sub runBatchFile(selectedVal)
	Set oWsh = CreateObject("WScript.Shell")
	strCommand = Chr(34) & selectedVal & "\runner.bat" & Chr(34)
	oWsh.Run strCommand, 0
	Set oWsh = Nothing
End Sub

Sub sbWait(iSeconds)
	Dim oShell  : Set oShell = CreateObject("WScript.Shell")
	oShell.run "cmd /c ping localhost -n " & iSeconds,0,True
	Set oShell = Nothing
End Sub

Sub soapProgess(strTitle)
	Dim oSoapFso
	CurrentDirectory = objWB.Path
	
	strRequestPath = CurrentDirectory & "\Request"
	strResponsePath = CurrentDirectory & "\Response"
	Set oSoapFso = CreateObject("Scripting.FileSystemObject")
	Set objFolder = oSoapFso.GetFolder(strRequestPath)
	Set colFiles = objFolder.Files
	
	iTotalFiles = colFiles.Count
	Dim AbortTime
	AbortTime = Now + TimeValue("0:01:10") 
	Do
		Set objFolder = oSoapFso.GetFolder(strResponsePath)
		Set colFiles = objFolder.Files
		'-----------------------
		'----To check if no reponse generated within 30 seconds.Exit the Do loop
		sbWait 2
		If colFiles.Count = 0 And Now > AbortTime then
			Exit Do
		End If
		'-----------------------
		If colFiles.Count < iTotalFiles Then
			JSProgressCounterSubTasks "Sending Soap Requests",2,4,"Requests",Cstr(colFiles.Count),Cstr(iTotalFiles)
		Else
			JSProgressCounterSubTasks "Sending Soap Requests",2,4,"Requests",Cstr(colFiles.Count),Cstr(iTotalFiles)
			sbWait 2
			Exit Do
		End If
	Loop
End Sub

Sub ResponseRunner()
	ClearResponseSheets
	strResponseTag = Trim(objExcel.WorksheetFunction.Index(objWB.Worksheets("Base").Range("2:2"), objExcel.WorksheetFunction.Match("ResponseTag", objWB.Worksheets("Base").Range("1:1"), 0)))
	Set fso = CreateObject("Scripting.FileSystemObject")
	Set folder = fso.GetFolder(objWB.Path & "\Response")
	iRow = 2
	iResponseBarCount = 0
	
	Do while iRow <= objWB.Worksheets("Runner").UsedRange.Rows.Count
		blnFound = False
		If StrComp(LCase(Trim(objWB.Worksheets("Runner").Cells(iRow, 2).Value)), "n") <> 0 And _
			StrComp(Trim(objWB.Worksheets("Runner").Cells(iRow, 4).Value), "GoLive Policy not generated for this test case") <> 0 Then
			strTCName = Trim(objWB.Worksheets("Runner").Cells(iRow, 1).Value)
			fileCnt = 0
			If StrComp(Trim(strTCName), "") = 0 Then
				Exit Do
			Else
				intResponseFilesCount = folder.Files.Count
				For Each file In folder.Files
					fileCnt = fileCnt + 1
					If Right(file.Name, 4) = ".xml" And InStr(1, file.Name, Left(objWB.Name, Len(objWB.Name) - 5) & "_" & strTCName & "_") > 0 Then
						strFileName = file.Name
						arrTCName = Split(Left(strFileName, Len(strFileName) - 4), "_")
						strTCName = arrTCName(UBound(arrTCName) - 1)
						exportTagFlag = getResponse(file.Path, strTCName, iRow)

						iResponseBarCount = iResponseBarCount + 1
						JSProgressCounterSubTasks "Soap Response generated",3,4,"Response XML to Excel",Cstr(iResponseBarCount),Cstr(intResponseFilesCount)

						If exportTagFlag Then
							errorTestCaseFound = 0
							For each sheet in objWB.Worksheets
								If Instr(1, Trim(sheet.Name), "Err") > 0 Then
									errSheetRow = 1
									For iErrRow = 1 to sheet.UsedRange.Rows.Count
										If Strcomp(Trim(sheet.Cells(iErrRow, 1).Value),strTCName) = 0 And iErrRow <=sheet.UsedRange.Rows.Count Then
											errorTestCaseFound = errorTestCaseFound + 1
										End If
									Next
								End If
							Next					
							
							If errorTestCaseFound = 0 Then
								objWB.Worksheets("Runner").Cells(iRow, 4).Value = "Response Captured successfully and Added to Excel"
								objWB.Worksheets("Runner").Cells(iRow, 5).Value = "Pass"
								objWB.Worksheets("Runner").Cells(iRow, 5).Interior.ColorIndex = 4
							Else
								objWB.Worksheets("Runner").Cells(iRow, 4).Value = "Response Captured With Errors and Added to Excel"
								objWB.Worksheets("Runner").Cells(iRow, 5).Value = "Fail"
								objWB.Worksheets("Runner").Cells(iRow, 5).Interior.ColorIndex = 3
							End If
							blnFound = True
							Exit For
						End If
					End If
				Next
				
				If fileCnt = 0 Then
					objWB.Worksheets("Runner").Cells(iRow, 4).Value = "Response not generated from Request"
					objWB.Worksheets("Runner").Cells(iRow, 5).Value = "Fail"
					objWB.Worksheets("Runner").Cells(iRow, 5).Interior.ColorIndex = 3
				End If
			End If
		End If
		iRow = iRow + 1
	Loop
End Sub

Sub ClearResponseSheets()
	For Each wks In objWB.Worksheets
		If Not (InStr(1, wks.Name, "Req_") = 1 Or StrComp(wks.Name, "Runner") = 0 Or StrComp(wks.Name, "Base") = 0 Or StrComp(wks.Name, "SheetMapper") = 0 Or StrComp(wks.Name, "Validation") = 0) Then
			iTCRowNum = objExcel.WorksheetFunction.Match("TestCaseId", objWB.Worksheets(wks.Name).Range("A:A"), 0)		
			iUsedRowCount = wks.UsedRange.Rows.Count
			iUsedColCount = wks.UsedRange.Columns.Count
			
			If iUsedRowCount > iTCRowNum Then
				wks.Range("A" & CStr(iTCRowNum + 1) & ":" & ColumnLetter(iUsedColCount) & CStr(iUsedRowCount)).Delete
			End If
		End If
	Next
End Sub

Function getResponse(strFilePath, sTestCaseNameReponse, iRow)
	On error resume next
	blnDataAdded = False
	Set oXMLFile = CreateObject("Microsoft.XMLDOM")
	oXMLFile.Load (strFilePath)
	Set TitleNodes = oXMLFile.SelectNodes("//" & strResponseTag)
	'--- need to fetch the name of the testcase from the response sheetname
	strTestCaseNameResponse = sTestCaseNameReponse
	Set rootNode = TitleNodes(0)
	exportTagFound = False
	
	If Not(rootNode is Nothing) Then
		For i = 0 To (rootNode.ChildNodes.Length - 1)
			Set childNode = rootNode.ChildNodes(i)
			
			If childNode.ChildNodes.Length > 0 Then
				strMappedSheet = mappedSheet(childNode.BaseName)
				addNodesAndData childNode, strMappedSheet
			End If		
		Next
		exportTagFound = True
	Else
		objWB.Worksheets("Runner").Cells(iRow, 4).Value = "Response generated with fault exception/Without Export Tags"
		objWB.Worksheets("Runner").Cells(iRow, 5).Value = "Fail"
		objWB.Worksheets("Runner").Cells(iRow, 5).Interior.ColorIndex = 3
		exportTagFound = False
	End If
	getResponse = exportTagFound
End Function

Sub addNodesAndData(oNode, sSheetName)
	strExpSheetName = sSheetName
	'---Added by Gurvinder
	blnDataAdded = False
	iNodeRowNumber = 1
	iDataRowPos = 0
	Set ChildNodes = oNode.ChildNodes     
	
	'----Calculating whether the hierarchy(Nodes) has only fields or complex elements
	iTCRowNum = objExcel.WorksheetFunction.Match("TestCaseId", objWB.Worksheets(sSheetName).Range("A:A"), 0)
	If iTCRowNum = 1 Then
		blnTestCaseIdAtRowOne = True
	Else
		blnTestCaseIdAtRowOne = False
	End If
	
	For Each oChildNode In ChildNodes
		addData oChildNode
		If Not (blnTestCaseIdAtRowOne) Then
			If StrComp(sSheetName, oChildNode.ParentNode.BaseName) = 0 Then
				blnDataAdded = False
			End If
		End If
	Next   
End Sub

Sub addData(oNode)
	If oNode.ChildNodes.Length > 0 Then
		If (oNode.ChildNodes.Length = 1) And StrComp(CStr(oNode.ChildNodes(0).NodeName), "#text") = 0 Then
			'strColumnName will have that node which has data
			strColumnName = oNode.BaseName
			'---Set Data
			'Find TestCaseId col
			iTCRowNum = objExcel.WorksheetFunction.Match("TestCaseId", objWB.Worksheets(strExpSheetName).Range("A:A"), 0)
			iColCount = objExcel.WorksheetFunction.CountA(objWB.Worksheets(strExpSheetName).Range(CStr(iTCRowNum) & ":" & CStr(iTCRowNum)))
			
			For iCol = 1 To iColCount
				If StrComp(objWB.Worksheets(strExpSheetName).Cells(iTCRowNum, iCol).Value, strColumnName) = 0 Then
					iTempTCRowNum = iTCRowNum
					Set oTempNode = oNode.ParentNode
					Do
						'-----New Code added to accomodate the case of no row
						If iTempTCRowNum <> 1 Then
							iTempTCRowNum = iTempTCRowNum - 1
						End If
						'---Get the parent name from merge area concept.
						strParent = objWB.Worksheets(strExpSheetName).Range(ColumnLetter(iCol) & CStr(iTempTCRowNum)).MergeArea.Cells(1, 1).Value
						'-----New Code added to accomodate the case of no row
						If StrComp(strColumnName, strParent) = 0 Then
							If Not (blnDataAdded) Then
								'--- add the testcase name entry
								'--- get the testcase name
								iDataRowPos = objWB.Worksheets(strExpSheetName).UsedRange.Rows.Count + 1
								objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, 1).NumberFormat = "@"
								objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, 1).Value = strTestCaseNameResponse
							End If
							blnDataAdded = True
							'Set the data
							objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, iCol).NumberFormat = "@"
							objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, iCol) = Trim(oNode.Text)
							Exit Sub
						End If
						
						'--- Code need to change
						If StrComp(strParent, oTempNode.BaseName) = 0 Then
							' check the parent if they are equal....till iTempTCRowNum is 1 then set the data
							
							If iTempTCRowNum = 1 Then
								If Not (blnDataAdded) Then
									'--- add the testcase name entry
									'--- get the testcase name
									iDataRowPos = objWB.Worksheets(strExpSheetName).UsedRange.Rows.Count + 1
									objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, 1).NumberFormat = "@"
									objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, 1).Value = strTestCaseNameResponse
								End If
								blnDataAdded = True
								'Set the data
								objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, iCol).NumberFormat = "@"
								objWB.Worksheets(strExpSheetName).Cells(iDataRowPos, iCol) = Trim(oNode.Text)
								Exit Sub
							End If
						Else
							Exit Do
						End If
						Set oTempNode = oTempNode.ParentNode						
					Loop
				End If
			Next
		Else
			For Each oChildNode In oNode.ChildNodes
				 addData oChildNode
			Next
		End If
	End If
End Sub

Sub finalXMLFileTransfer(strFtPath, strWB)
	Dim StrNewFolderName
	Set oFtFso = CreateObject("Scripting.FileSystemObject")
	strReq = strFtPath & "\Request"
	strRes = strFtPath & "\Response"
	
	Set objReqFolder = oFtFso.GetFolder(strReq)
	Set colReqFiles = objReqFolder.Files
	
	Set objResFolder = oFtFso.GetFolder(strRes)
	Set colResFiles = objResFolder.Files
	
	blnFirst = True
	StrNewFolderName = ""
	
	'---Moving Request Files
	For Each oFile In colReqFiles
		If blnFirst Then
			StrNewFolderName = Replace(Replace(Replace(CStr(CDate(oFile.DateLastModified)), " ", "_"), "/", "_"), ":", "_")
			oFtFso.CreateFolder strReq & "\" & strWB & "_" & StrNewFolderName
			oFtFso.CreateFolder strRes & "\" & strWB & "_" & StrNewFolderName
		End If
		blnFirst = False
		
		If InStr(1, oFile.Name, strWB) > 0 Then
			oFile.Move strReq & "\" & strWB & "_" & StrNewFolderName & "\" & oFile.Name
		End If				      
	Next
	
	For Each oFile In colResFiles
		If InStr(1, oFile.Name, strWB) > 0 Then
			oFile.Move strRes & "\" & strWB & "_" & StrNewFolderName & "\" & oFile.Name
			strResponsePath = strRes & "\" & strWB & "_" & StrNewFolderName
		End If
	Next
	
	Set oFtFso = Nothing
	Set objReqFolder = Nothing
	Set colReqFiles = Nothing
	Set objResFolder = Nothing
	Set colResFiles = Nothing
End Sub

Sub TearDown()
	objWB.Save
	objWB.Close
	Set objWB = Nothing
End Sub

Sub CreateProgressBar()
	objIE1.Document.Title = "PROGRESS - " & strSelectedValue & String(100,".")
End Sub

Sub UpdateTitle(strTitle)			
	objIE1.Document.Title = "PROGRESS - " & strTitle & String(100,".")
End Sub

Sub JSProgressCounter(strProcessName,strMin,strMax)
	'objIE1.Document.Title=UCASE(strProcessName) & String(100, ".")
	minPercentage = (cint(strMin)/cint(strMax))*100
	objIE1.Document.Body.InnerHTML = "<div id='myProgress' style='width: 100%; background-color: #ddd'><div id='myBar' style='width: " & minPercentage & "%; height: 20px; background-color: #4CAF50;text-align: center;line-height: 20px;color: white;'>" & strProcessName & "</div></div>"
End Sub

Sub JSProgressCounterSubTasks(strProcessName,strMin,strMax,strSubTask,subTaskMin,subTaskMax)
	minPercentage = (cint(strMin)/cint(strMax))*100
	objIE1.Document.Body.InnerHTML = "<div id='myProgress' style='width: 100%; background-color: #ddd'><div id='myBar' style='width: " & minPercentage & "%; height: 20px; background-color: #4CAF50;text-align: center;line-height: 20px;color: white;'>" & strProcessName & "</div></div>"
	
	If cint(subTaskMax) <> 0 Then
		subTaskMinPercentage = (cint(subTaskMin)/cint(subTaskMax))*100
		strHtml = objIE1.Document.Body.InnerHTML
		strHtml = strHtml & "<br>" & strSubTask & "(" & subTaskMin & "/" & subTaskMax & ")<br><div id='mySubTaskProgress' style='width: 100%; background-color: #ddd'><div id='mySubTaskBar' style='width: " & subTaskMinPercentage & "%; height: 20px; background-color: #4CAF50;text-align: center;line-height: 20px;color: white;'></div></div>"
		objIE1.Document.Body.InnerHTML = strHtml
	End If
End Sub

Sub copyPolicyToServiceTestDataTemplate(sPolicyTag, sSuffix)
	Set oFSO = CreateObject("Scripting.FileSystemObject")
	Set oFolder = oFSO.GetFolder(strCurDir)
	Set cFiles = oFolder.Files
	Set list = CreateObject("Scripting.Dictionary")
	
	If InStr(1, sPolicyTag, ";") > 0 Then
		tagList = Split(sPolicyTag, ";")
		For each ele in tagList
			strHier = Split(ele, "_")
			strSheetName = "Req_" + strHier(0)
			If UBound(strHier) = 2 Then
				strPolNodeName = strHier(2)
			Else
				strPolNodeName = strHier(1)
			End If
			list.add strSheetName, strPolNodeName
		Next
	Else
		strHier = Split(sPolicyTag, "_")
		strSheetName = "Req_" + strHier(0)
		If UBound(strHier) = 2 Then
			strPolNodeName = strHier(2)
		Else
			strPolNodeName = strHier(1)
		End If
		list.add strSheetName, strPolNodeName
	End If
	
	For Each oFile In cFiles
		If Strcomp(Right(oFile.Name, 3), "csv") = 0 and Strcomp(Mid(Split(oFile.Name, ".")(0), InStr(1, Split(oFile.Name, ".")(0), strGoLive) + Len(strGoLive)), sSuffix) = 0 Then
			Set oFile = oFSO.OpenTextFile(strCurDir + "\" + oFile.Name, 1)
			Do until oFile.AtEndOfStream
				sLine = oFile.ReadLine
				sTCName = Split(sLine,",")(0)
				sPol = Split(sLine,",")(1)
				dictTC.add sTCName, sPol
				
				For each sKey in list.Keys()
					iTCRow = objExcel.WorksheetFunction.Match("TestCaseId", objWB.Worksheets(sKey).Range("A:A"), 0)
					Set Rng = objWB.Worksheets(sKey).Range(iTCRow & ":" & iTCRow)
					intColNumberPolID = objExcel.WorksheetFunction.Match(list.item(sKey), Rng, 0)

					intRowNum = objExcel.WorksheetFunction.Match(sTCName, objWB.Worksheets(sKey).Range("A:A"), 0)
					objWB.Worksheets(sKey).Cells(intRowNum, intColNumberPolID).Value = ""
					objWB.Worksheets(sKey).Cells(intRowNum, intColNumberPolID).NumberFormat = "@"
					objWB.Worksheets(sKey).Cells(intRowNum, intColNumberPolID).Value = sPol
				Next
			Loop
			oFile.Close
			Set oFile = Nothing
		End If
	Next
	
	Set oFolder = Nothing
	Set cFiles = Nothing
	Set oFSO = Nothing
	Set list = Nothing
End Sub

Sub deleteTemplateRow()
	For Each sName In objWB.Worksheets
		If InStr(1, sName.Name, "Req_") = 1 Then
			iTemplateRow = objExcel.WorksheetFunction.Match("Template", objWB.Worksheets(sName.Name).Range("A:A"), 0)
			objWB.Worksheets(sName.Name).Rows(iTemplateRow).EntireRow.Delete
		End If
    Next
End Sub

Sub copyGoLivePoliciesToCSV(selectedVal, cfiles)	
	For Each fileObj In cfiles
		If InStr(1, fileObj.Name, strSelectedValue)> 0 And Strcomp(Right(fileObj.Name, 4), "xlsx") = 0 Then
			strWBPath = selectedVal & "\" & fileObj.Name
			InitializeObjects strWBPath
			
			Set unique = CreateObject("Scripting.Dictionary")
			sExpSheetName = "ExpGrpPolref"
			iTCRow = objExcel.WorksheetFunction.Match("TestCaseId", objWB.Worksheets(sExpSheetName).Range("A:A"), 0)
			iCol = objExcel.WorksheetFunction.Match("PolId", objWB.Worksheets(sExpSheetName).Range(iTCRow & ":" & iTCRow), 0)
			
			sPath = strCurDir + "\" + Split(fileObj.Name,".")(0) + ".csv"
			Set oFSO = CreateObject("Scripting.FileSystemObject") 
			Set oFile = oFSO.CreateTextFile(sPath, ForAppending)
			
			For iRCnt = iTCRow + 1 to objWB.Worksheets(sExpSheetName).UsedRange.Rows.Count
				If not unique.exists(objWB.Worksheets(sExpSheetName).Cells(iRCnt, 1).Value) Then
					unique.add objWB.Worksheets(sExpSheetName).Cells(iRCnt, 1).Value, objWB.Worksheets(sExpSheetName).Cells(iRCnt, iCol).Value
				End If
			Next
			
			For each sKey in unique.Keys()
				oFile.WriteLine sKey + "," + unique.Item(sKey)
			Next
			
			oFile.Close
			Set unique = Nothing
			Set oFile = Nothing
			Set oFSO = Nothing
			TearDown
		End If
	Next
End Sub

Sub KillAll(ProcessName)
    Dim objWMIService, colProcess
    Dim strComputer, strList, p
    strComputer = "."
    Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2") 
    Set colProcess = objWMIService.ExecQuery ("Select * from Win32_Process Where Name like '" & ProcessName & "'")
    For Each p in colProcess
        p.Terminate             
    Next
End Sub

Sub backUpFile()
	Dim StrNewFolderName
	strFtPath = strCurDir & "\" & strSelectedValue
	Set oRFso = CreateObject("Scripting.FileSystemObject")
	
	Set oFolder = oRFso.GetFolder(strFtPath)
	Set cntFiles = oFolder.Files
	
	blnFirst = True
	StrNewFolderName = ""
	
	For Each oFile In cntFiles
		If InStr(1, oFile.Name, strSelectedValue)> 0 And Strcomp(Right(oFile.Name, 4), "xlsx") = 0 Then
			If blnFirst Then
				StrNewFolderName = Replace(Replace(Replace(CStr(CDate(oFile.DateLastModified)), " ", "_"), "/", "_"), ":", "_")
				oRFso.CreateFolder strFtPath & "\Template\BackUp\" & StrNewFolderName
			End If
			blnFirst = False		
			
			oFile.Move strFtPath & "\Template\BackUp\" & StrNewFolderName & "\" & oFile.Name
		End If
	Next
	
	Set oRFso = Nothing
	Set oFolder = Nothing
	Set cntFiles = Nothing
End Sub

Sub createTestDataTemplate()	
	Set oFSO = CreateObject("Scripting.FileSystemObject")
	Set oFolder = oFSO.GetFolder(strCurDir + "\" + strGoLive)
	Set cFiles = oFolder.Files
	
	For Each oFile In cFiles
		If Strcomp(Right(oFile.Name, 4), "xlsx") = 0 Then
			strSuffix = Mid(Split(oFile.Name, ".")(0), InStr(1, Split(oFile.Name, ".")(0), strGoLive) + Len(strGoLive))
			srcFile = strCurDir & "\" & strSelectedValue & "\Template" & "\" & strSelectedValue & ".xlsx"
			dest = strCurDir & "\" & strSelectedValue & "\" & strSelectedValue & strSuffix & ".xlsx"
			
			oFSO.CopyFile srcFile, dest

			Set objWB1 = objExcel.Workbooks.Open(strCurDir & "\" & strGoLive & "\" & oFile.Name)
			Set objWB2 = objExcel.Workbooks.Open(dest)			
			objWB1.Worksheets("Runner").Range("A2:B" & objWB1.Worksheets("Runner").UsedRange.Rows.Count).Copy objWB2.Worksheets("Runner").Range("A2")
			
			For Each sSheet In objWB2.Worksheets
				If InStr(1, sSheet.Name, "Req_") = 1 Then
					iRow = objExcel.WorksheetFunction.Match("Template", sSheet.Range("A:A"), 0)
					
					objWB2.Worksheets("Runner").Range("A2:A" & objWB2.Worksheets("Runner").UsedRange.Rows.Count).Copy sSheet.Range("A" & (iRow + 1))
				End If
			Next
			
			formatTestDataTemplate objWB2.Worksheets
			objWB2.Worksheets(1).Activate			
			objWB2.Save
			objWB1.Close
			objWB2.Close
			Set objWB1 = Nothing
			Set objWB2 = Nothing
		End If
	Next
	
	Set oFSO = Nothing
	Set oFolder = Nothing
	Set cFiles = Nothing
End Sub

Sub formatTestDataTemplate(sSheets)
    For Each oSheet In sSheets
		If InStr(1, oSheet.Name, "Req_") > 0 Or StrComp(Trim(oSheet.Name), "Runner") = 0 Then
			oSheet.Activate		
			oSheet.Range("A1").Select

			iTestCaseIdRNum = objExcel.WorksheetFunction.Match("TestCaseId", oSheet.Range("A:A"), 0)
			colCntLetter = ColumnLetter(oSheet.UsedRange.Columns.Count)
			oSheet.Activate
			oSheet.Range("A" & CStr(iTestCaseIdRNum) & ":" & colCntLetter & CStr(oSheet.UsedRange.Rows.Count)).BorderAround 1
			oSheet.Range("A" & CStr(iTestCaseIdRNum) & ":" & colCntLetter & CStr(iTestCaseIdRNum)).Borders(9).LineStyle = 1			
			With oSheet.Range("A" & CStr(iTestCaseIdRNum) & ":" & colCntLetter & CStr(oSheet.UsedRange.Rows.Count))
				.Borders(11).LineStyle = 1
				.Borders(12).LineStyle = 1
				.NumberFormat = "@"
			End With
		End If
    Next
End Sub