Attribute VB_Name = "Module3"
Option Explicit

'How to use:
' 1) No sheets that do not contain the tables you want to combine.
'    If you want to keep them, adjust WS_Count - x and move them to then end
' 2) tables must all have the same number of rows, be row header format, and have the same row headers
' 3) All tables must be in the same row range on each sheet.
' 4) Last row will contain the name of the sheet it was taken from, adjust header accordingly
' 5) Define variables in the section below
' 6) Do not have any data sheets named "Results"
' 7) If you want to fix the fields this macro asks for to increase speed, remove the apostrophes for the relevant sections



'Input in prompt
Sub TableCombiner()
Dim ReadCell As Range
Dim WriteCell As Range
Dim I As Integer
Dim J As Integer
Dim FinalTable As ListObject
Dim EndCell As Range

'User variables
Dim NumRows As Integer
Dim StartCell As Range
Dim SheetName As String

'Warning box
Dim Msg, Style, Title, Response
Msg = "This macro only works on specific formatting." & Chr(13) _
& "If you are unsure what that is, read the readme in the folder containing this macro." & Chr(13) & Chr(13) _
& "It is highly recommended to only use this macro on a copy of your data. Continue?"
Style = vbYesNo
Title = "Table Combiner"
Response = MsgBox(Msg, Style, Title)
If Response = vbNo Then End



''Get user input
Worksheets(1).Activate
NumRows = InputBox("Enter the number of rows in one of your tables", Title)
Set StartCell = Application.InputBox("Select the top left cell for your tables(i.e the topmost row header)", Title, Type:=8)
SheetName = InputBox("What do the sheet names represent?", Title)


''Example of fixed fields, use these instead for speed
'NumRows = 5
'StartCell = "A1"
'SheetName = "Airline"




'Find the last cell
Set EndCell = StartCell.Offset(NumRows - 1, 0)

'Disable screen updating and alerts for speed
Application.ScreenUpdating = False
Application.DisplayAlerts = False

'Delete sheets and remake them
On Error Resume Next
Worksheets("Results").Delete
On Error GoTo 0
ActiveWorkbook.Sheets.Add After:=Worksheets(Worksheets.Count)
ActiveSheet.Name = "Results"



'Add row headers
Worksheets(1).Activate
For J = 1 To NumRows
  Worksheets("Results").Range("A1").Offset(0, J - 1).Value = StartCell.Offset(J - 1, 0).Value
  If J = NumRows Then Worksheets("Results").Range("A1").Offset(0, J).Value = SheetName
Next J
  
  
'iterate through worksheets and write info to "Results" tab
For I = 1 To ActiveWorkbook.Worksheets.Count - 1
  'Set readcell and writecell depending on worksheet
  Set ReadCell = Worksheets(I).Range(StartCell.Address).Offset(0, 1)
  If I = 1 Then
    Set WriteCell = Worksheets("Results").Range("A2")
  Else
    Set WriteCell = Worksheets("Results").UsedRange.End(xlDown).Offset(1, 0)
  End If
  
  'Iterate through worksheet and write info in results
  Do While ReadCell.Value <> ""
  
    For J = 1 To NumRows
      WriteCell.Offset(0, J - 1).Value = ReadCell.Offset(J - 1, 0).Value
    Next J
    WriteCell.Offset(0, NumRows).Value = Worksheets(I).Name
    
    Set WriteCell = WriteCell.Offset(1, 0)
    Set ReadCell = ReadCell.Offset(0, 1)
    
  Loop
  
Next I

'Make table
Worksheets("Results").Activate
Worksheets("Results").UsedRange.Select
Set FinalTable = ActiveSheet.ListObjects.Add(xlSrcRange, Selection, , xlYes)
FinalTable.Name = "FinalTable"


'Formatting
Selection.Columns.AutoFit
Selection.Rows.AutoFit
With Selection
    .HorizontalAlignment = xlLeft
    .VerticalAlignment = xlCenter
    .WrapText = True
End With

'Freeze top row
With ActiveWindow
    .SplitColumn = 0
    .SplitRow = 1
End With
ActiveWindow.FreezePanes = True
      
'Reenable updating and alerts
Application.ScreenUpdating = True
Application.DisplayAlerts = True
End Sub

'Combine Results and master tab
'Fix the start and end cell finding
