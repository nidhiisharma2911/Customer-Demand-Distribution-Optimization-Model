Power BI build script / video storyboard

1) Open Power BI Desktop.
2) Get Data -> Text/CSV: import `outputs/optimal_allocation.csv`, `outputs/scenario_results.csv`, `data/customers.csv`, `data/warehouses.csv`.
3) In Power Query:
   - For scenario allocations: use Folder or Import each `outputs/scenario_*/optimal_allocation.csv`, add a column `scenario` with the folder name, then `Append` into a single `Allocations` table.
   - Ensure types: `quantity` numeric, `cost_per_unit` decimal, `total_cost` decimal, `capacity` integer, `demand` integer.
   - Close & Apply.
4) Model view: create relationships:
   - `Allocations[warehouse_id] -> Warehouses[warehouse_id]`
   - `Allocations[customer_id] -> Customers[customer_id]`
5) Create measures (Modeling -> New measure):
   - `TotalLogisticsCost = SUM(Allocations[total_cost])`
   - `WarehouseUtilization = DIVIDE(SUM(Allocations[quantity]), SUM(Warehouses[capacity]), 0)` (format as %)
   - `TotalDemand = SUM(Customers[demand])`
   - `TotalSupplied = SUM(Allocations[quantity])`
   - `UnmetDemand = [TotalDemand] - [TotalSupplied]`
6) Report page layout:
   - Top-left: Card visual showing `TotalLogisticsCost`.
   - Right: Slicer `scenario`.
   - Middle: Bar chart `Warehouses[warehouse_id]` vs `WarehouseUtilization` (percent).
   - Bottom-left: Clustered bar `Customers[customer_id]` with `TotalDemand` and `TotalSupplied`.
   - Bottom-right: Bar chart `ScenarioResults[scenario]` vs `total_cost`.
7) Add tooltips and conditional formatting: color warehouses by utilization (green/yellow/red thresholds).
8) Save file as `dashboard/distribution_dashboard.pbix` locally.

Notes: I cannot write a .pbix file in this environment. Use the steps above to assemble the report locally; I can iterate on visuals or DAX after you upload a screenshot or the .pbix.
