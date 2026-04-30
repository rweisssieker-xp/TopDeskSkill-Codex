// TOPdesk Power Query helper snippets.
// Paste into blank queries/functions and adapt names.

// fnDateKey
(inputDate as nullable date) as nullable number =>
if inputDate = null then null
else Date.Year(inputDate) * 10000 + Date.Month(inputDate) * 100 + Date.Day(inputDate)

// fnSafeRecordField
(recordValue as any, fieldName as text) as any =>
try Record.Field(recordValue, fieldName) otherwise null
