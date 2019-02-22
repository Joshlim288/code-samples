Attribute VB_Name = "Module2"
Option Explicit

Sub GetSheetInfo()
Dim WS As Integer
Dim F As Integer
Dim NumFields As Integer
Dim FinalTable As Object
Dim WriteCell As Range
Dim FieldRange As Range
Dim FieldsRef As Collection
Dim FieldsName As Collection
Set FieldsRef = New Collection
Set FieldsName = New Collection

'Warning box
Dim Msg, Style, Title, Response
Msg = "It is highly recommended to only use this macro on a copy of your data. Continue?"
Style = vbYesNo
Title = "Table Combiner"
Response = MsgBox(Msg, Style, Title)
If Response = vbNo Then End

'Ask user for how many fields to consolidate
Worksheets(1).Activate
Msg = "How many fields do you want to consolidate?"
Title = "Consolidate Forms"
NumFields = Application.InputBox(Msg, Title, Type:=1)
If NumFields = False Then End


'Ask for user input for names and references of data to consolidate

For F = 1 To NumFields
  Msg = "Enter the Cells you want to consolidate" & Chr(13) & Chr(13) & Chr(13) _
        & "Cell Reference of Field " & CStr(F) & ":"
  Set FieldRange = Application.InputBox(Msg, Title, Type:=8)
  FieldsRef.Add Item:=FieldRange.Address
  If FieldsRef(F) = False Then End
  Msg = "Enter the Cells you want to consolidate" & Chr(13) & Chr(13) & Chr(13) _
        & "Name of Field " & CStr(F) & ":"
  FieldsName.Add Item:=Application.InputBox(Msg, Title, Type:=2)
  If FieldsName(F) = False Then End
Next F

'Add sheetname header
FieldsName.Add Item:=("Sheet Name")

'For Speed
Application.ScreenUpdating = False
Application.DisplayAlerts = False

'Delete Results sheet and remake it
On Error Resume Next
Worksheets("Results").Delete
On Error GoTo 0
ActiveWorkbook.Sheets.Add After:=Worksheets(Worksheets.Count)
ActiveSheet.Name = "Results"

'Iterate through sheets
Set WriteCell = Worksheets("Results").Range("A1")
For WS = 0 To Worksheets.Count - 1
  For F = 1 To NumFields + 1
    If WS = 0 Then
      WriteCell.Offset(0, F - 1).Value = FieldsName(F)
    ElseIf F = NumFields + 1 Then
      WriteCell.Offset(0, F - 1).Value = Worksheets(WS).Name
    Else
      WriteCell.Offset(0, F - 1).Value = Worksheets(WS).Range(FieldsRef(F)).Value
    End If
  Next F
  Set WriteCell = WriteCell.Offset(1, 0)
Next WS

'Formatting
Worksheets("Results").UsedRange.Select
Selection.Columns.AutoFit
Selection.Rows.AutoFit
Set FinalTable = ActiveSheet.ListObjects.Add(xlSrcRange, Selection, , xlYes)
FinalTable.Name = "FinalTable"
With Selection
    .HorizontalAlignment = xlLeft
    .VerticalAlignment = xlCenter
    .WrapText = True
End With
With ActiveWindow
    .SplitColumn = 0
    .SplitRow = 1
End With
ActiveWindow.FreezePanes = True


Application.ScreenUpdating = True
Application.DisplayAlerts = True

End Sub
