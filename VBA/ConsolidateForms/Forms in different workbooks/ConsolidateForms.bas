Attribute VB_Name = "Module1"
Option Explicit


'How to use:
'1) Results sheet must be in same directory as workbooks to be consolidated
'2) For each field, data to extract must be in a single cell
'3) If you want to use the macro without prompts, delete the prompts section
'   and manually assign variables yourself in the section below it


Sub GetWorkbookInfo()
Dim wbOpen As Workbook
Dim WriteCell As Range
Dim I As Integer
Dim StrExtension As String
Dim FinalTable As ListObject

'User Variables
Dim NumFields As Integer
Dim FieldsRef As Collection
Dim FieldsName As Collection
Set FieldsRef = New Collection
Set FieldsName = New Collection
Dim FieldRange As Range


'Change directory to where Results workbook is,
'Set StrExtension to iterate through all.xls files in folder
'when StrExtension = Dir is called
ChDir (Application.ActiveWorkbook.Path)
StrExtension = Dir("*.xls")
If StrExtension = "Results.xlsm" Then StrExtension = Dir

'Warning box
Dim Msg, Style, Title, Response
Msg = "It is highly recommended to only use this macro on a copy of your data. Continue?"
Style = vbYesNo
Title = "Table Combiner"
Response = MsgBox(Msg, Style, Title)
If Response = vbNo Then End

''PROMPT
Workbooks.Open (StrExtension)
'Ask user for how many fields to consolidate
Msg = "How many fields do you want to consolidate?"
Title = "Consolidate Forms"
NumFields = Application.InputBox(Msg, Title, Type:=1)
If NumFields = False Then End


'Ask for user input for names and references of data to consolidate

For I = 1 To NumFields
  'Ref
  Msg = "Enter the Cells you want to consolidate" & Chr(13) & Chr(13) & Chr(13) _
        & "Select Cell " & CStr(I) & ":"
  Set FieldRange = Application.InputBox(Msg, Title, Type:=8)
  FieldsRef.Add Item:=FieldRange.Address
  If FieldsRef(I) = False Then End
  'Name
  Msg = "Enter the Cells you want to consolidate" & Chr(13) & Chr(13) & Chr(13) _
        & "Enter label for data in Cell " & CStr(I) & ":"
  FieldsName.Add Item:=Application.InputBox(Msg, Title, Type:=2)
  If FieldsName(I) = False Then End
Next I
Workbooks.Open(StrExtension).Close (False)

''END PROMPT



''IN CODE
'NumFields = 1

''Repeat these for as many fields as you have
'FieldsName.Add Item:="Name"
'FieldsRef.Add Item:="AV10"

''END IN CODE




'For Speed
Application.ScreenUpdating = False
Application.DisplayAlerts = False

'Clear cells
Workbooks("Results").Worksheets(1).Cells.Clear

'Create headers in results sheet
Set WriteCell = Workbooks("Results").Worksheets(1).Range("A1")
For I = 1 To NumFields
  WriteCell.Offset(0, I - 1).Value = FieldsName.Item(I)
Next I

'Set last column to sheet name
WriteCell.Offset(0, NumFields).Value = "Sheet Name"

'Iterate through workbooks and get info, writing to results workbook
Set WriteCell = WriteCell.Offset(1, 0)
        
  Do While StrExtension <> ""

    If StrExtension = "Results.xlsm" Then
      StrExtension = Dir
    Else
      Set wbOpen = Workbooks.Open(StrExtension)
    
      For I = 1 To NumFields
        WriteCell.Offset(0, I - 1).Value = wbOpen.Worksheets(1).Range(FieldsRef.Item(I)).Value
      Next I
      
      'Sheet name as last column
      WriteCell.Offset(0, NumFields).Value = wbOpen.Name
      
      Set WriteCell = WriteCell.Offset(1, 0)
      wbOpen.Close (False)
      StrExtension = Dir
    End If
  
Loop

'Formatting
Workbooks("Results").Worksheets(1).UsedRange.Select
Selection.Columns.AutoFit
Selection.Rows.AutoFit
Set FinalTable = ActiveSheet.ListObjects.Add(xlSrcRange, Selection, , xlYes)
FinalTable.Name = "FinalTable"
With Selection
    .HorizontalAlignment = xlLeft
    .VerticalAlignment = xlCenter
    .WrapText = True
End With
Worksheets(1).Activate
With ActiveWindow
    .SplitColumn = 0
    .SplitRow = 1
End With
ActiveWindow.FreezePanes = True


Application.ScreenUpdating = True
Application.DisplayAlerts = True
End Sub

'ToDo:
'1) Create Forms in same workbook version
'2) Make code work for results in diff directory
