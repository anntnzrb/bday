open System.IO
open System.Text
open System.Text.RegularExpressions
open Sylvan.Data.Excel

module A = Array
module AP = Array.Parallel

/// <summary>
/// Contact record with name and email
/// </summary>
[<Struct>]
type Contact = { Name: string; Email: string }

/// <summary>
/// Contact validation and processing functions
/// </summary>
module Contact =
    let private emailRegex = Regex @"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    /// <summary>
    /// Validates if an email address has correct format
    /// </summary>
    /// <param name="email">Email address to validate</param>
    /// <returns>True if email format is valid</returns>
    let isValidEmail (email: string) = emailRegex.IsMatch email

/// <summary>
/// CSV processing functions for contact data
/// </summary>
module CsvProcessor =
    let delimiter = ";"
    let header = $"name{delimiter}email"

    /// <summary>
    /// Converts a contact to CSV format
    /// </summary>
    /// <param name="contact">Contact record to convert</param>
    /// <returns>Semicolon-delimited string</returns>
    let toCsv (contact: Contact) =
        $"{contact.Name}{delimiter}{contact.Email}"

    /// <summary>
    /// Extracts and capitalizes the first name from a full name string
    /// </summary>
    /// <param name="fullName">Full name string (may contain commas)</param>
    /// <returns>Capitalized first name</returns>
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

    /// <summary>
    /// Attempts to parse a CSV line into a Contact record
    /// </summary>
    /// <param name="line">CSV line with name, middle, email format</param>
    /// <returns>Some Contact if valid, None otherwise</returns>
    let tryParseContact (line: string) =
        let expectedCsvFields = 3

        line.Split(delimiter, expectedCsvFields)
        |> function
            | [| name; _; email |] when name <> "" && Contact.isValidEmail email ->
                Some
                    { Name = extractFirstName name
                      Email = email }
            | _ -> None

    /// <summary>
    /// Processes CSV lines: skips header, parses contacts, converts to CSV format
    /// </summary>
    /// <param name="lines">Array of CSV lines</param>
    /// <returns>Array of processed CSV lines with header</returns>
    let processLines =
        A.skip 1 // header
        >> AP.choose tryParseContact
        >> AP.map toCsv
        >> A.append [| header |]

/// <summary>
/// Excel file processing functions
/// </summary>
module ExcelProcessor =
    let private excelExtensions = Set.ofList [ ".xls"; ".xlsx" ]

    /// <summary>
    /// Checks if a file has an Excel extension (.xls or .xlsx)
    /// </summary>
    /// <param name="filePath">Path to the file</param>
    /// <returns>True if file has Excel extension</returns>
    let isExcelFile (filePath: string) =
        filePath |> Path.GetExtension |> _.ToLower() |> excelExtensions.Contains

    /// <summary>
    /// Converts an Excel file to CSV format
    /// </summary>
    /// <param name="filePath">Path to Excel file (.xls or .xlsx)</param>
    /// <returns>Array of semicolon-delimited strings</returns>
    let convertExcelToCsv (filePath: string) =
        Encoding.RegisterProvider CodePagesEncodingProvider.Instance
        use reader = ExcelDataReader.Create filePath
        let lines = ResizeArray()

        while reader.Read() do
            [| for i in 0 .. reader.FieldCount - 1 -> if reader.IsDBNull i then "" else reader.GetString i |]
            |> String.concat CsvProcessor.delimiter
            |> lines.Add

        lines.ToArray()

/// <summary>
/// Processes a file (Excel or CSV) and outputs parsed contact data to a new CSV file
/// </summary>
/// <param name="file">Input file path (Excel or CSV)</param>
/// <returns>Task that completes when processing is done</returns>
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

/// <summary>
/// Main entry point - processes a single file argument
/// </summary>
/// <param name="args">Command line arguments</param>
/// <returns>Exit code: 0 for success, 1 for error</returns>
[<EntryPoint>]
let main =
    function
    | [| inputFile |] ->
        processFile(inputFile).Wait()
        0
    | _ ->
        eprintfn "Usage: bday [file]"
        1
