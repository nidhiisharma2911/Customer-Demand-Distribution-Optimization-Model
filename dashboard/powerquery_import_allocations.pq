let
    // Change the folder path to your repository absolute path or select the folder in Power BI UI
    Source = Folder.Files("/workspaces/Customer-Demand-Distribution-Optimization-Model/outputs/allocations_folder"),
    CSVFiles = Table.SelectRows(Source, each Text.EndsWith([Name], ".csv")),
    // Read CSV content for each file
    AddCSV = Table.AddColumn(CSVFiles, "Data", each Csv.Document(File.Contents([Folder Path] & [Name]),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.Csv])),
    Expand = Table.ExpandTableColumn(AddCSV, "Data", {"Column1","Column2","Column3","Column4","Column5"}, {"warehouse_id","customer_id","quantity","cost_per_unit","total_cost"}),
    // Convert types
    Typed = Table.TransformColumnTypes(Expand, {{"warehouse_id", type text}, {"customer_id", type text}, {"quantity", type number}, {"cost_per_unit", type number}, {"total_cost", type number}}),
    // Derive scenario from file name (remove extension)
    AddScenario = Table.AddColumn(Typed, "scenario", each Text.BeforeDelimiter([Name], ".csv"), type text),
    Result = Table.SelectColumns(AddScenario, {"warehouse_id","customer_id","quantity","cost_per_unit","total_cost","scenario"})
in
    Result
