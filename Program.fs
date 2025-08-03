open System.IO
open System.Text
open System.Text.RegularExpressions
open Sylvan.Data.Excel

module A = Array
module AP = Array.Parallel

[<Struct>]
type Contact = { Name: string; Email: string }

module Contact =
    let private emailRegex = Regex @"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    let isValidEmail (email: string) = emailRegex.IsMatch email

module CsvProcessor =
    let delimiter = ";"
    let header = $"name{delimiter}email"

    let toCsv (contact: Contact) =
        $"{contact.Name}{delimiter}{contact.Email}"

    let extractFirstName (fullName: string) =
        let firstWord (s: string) = s |> _.Trim() |> _.Split(' ') |> A.head

        let capitalize =
            function
            | "" as s -> s
            | s -> s.ToLower() |> fun lower -> lower[0].ToString().ToUpper() + lower[1..]

        let nameDelimiter = ','
        let maxNameParts = 2

        fullName.Split(nameDelimiter, maxNameParts)
        |> function
            | [| _; name |] when name.Trim() <> "" -> firstWord name
            | _ -> firstWord fullName
        |> capitalize

    let tryParseContact (line: string) =
        let expectedCsvFields = 3

        line.Split(delimiter, expectedCsvFields)
        |> function
            | [| name; _; email |] when name <> "" && Contact.isValidEmail email ->
                Some
                    { Name = extractFirstName name
                      Email = email }
            | _ -> None

    let processLines =
        A.skip 1 // header
        >> AP.choose tryParseContact
        >> AP.map toCsv
        >> A.append [| header |]

module ExcelProcessor =
    let private excelExtensions = Set.ofList [ ".xls"; ".xlsx" ]

    let isExcelFile (filePath: string) =
        filePath |> Path.GetExtension |> _.ToLower() |> excelExtensions.Contains

    let convertExcelToCsv (filePath: string) =
        Encoding.RegisterProvider CodePagesEncodingProvider.Instance
        use reader = ExcelDataReader.Create filePath
        let lines = ResizeArray()

        while reader.Read() do
            [| for i in 0 .. reader.FieldCount - 1 -> if reader.IsDBNull i then "" else reader.GetString i |]
            |> String.concat CsvProcessor.delimiter
            |> lines.Add

        lines.ToArray()

let processFile file =
    task {
        let! lines =
            file
            |> function
                | file when ExcelProcessor.isExcelFile file -> task { return ExcelProcessor.convertExcelToCsv file }
                | file -> File.ReadAllLinesAsync file

        let processedLines = CsvProcessor.processLines lines
        let outputFile = Path.ChangeExtension(file, "parsed.csv")
        do! File.WriteAllLinesAsync(outputFile, processedLines)
    }

[<EntryPoint>]
let main =
    function
    | [| inputFile |] ->
        processFile(inputFile).Wait()
        0
    | _ ->
        eprintfn "Usage: bday [file]"
        1
