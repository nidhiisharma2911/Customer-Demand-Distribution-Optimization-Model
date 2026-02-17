Power Query (M) import instructions

1. In Power BI Desktop, choose `Get Data` -> `More...` -> `Blank Query`.
2. In the Query Editor, open `Advanced Editor` and paste the contents of `powerquery_import_allocations.pq`.
3. Update the `Folder.Files` path in the first line if your repository is located elsewhere on disk.
4. Click `Done`. Power Query will list and append all CSVs from the `outputs/allocations_folder` folder and add a `scenario` column derived from each filename.
5. Rename the query to `Allocations` and `Close & Apply`.

Notes:
- Alternatively, use `Get Data` -> `Folder` and point to `outputs/allocations_folder`, then use the built-in `Combine` UI. After combining, add a column with the file name and extract the scenario name similarly.
- Make sure column types are set correctly (numeric columns: `quantity`, `cost_per_unit`, `total_cost`; text columns: `warehouse_id`, `customer_id`, `scenario`).

This script anticipates CSVs named like `scenario_baseline.csv`, `scenario_demand_increase_20pct.csv`, etc.
