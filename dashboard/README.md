**Power BI Recipe**

- **Data sources:**
  - **Optimal allocation rows:** [outputs/optimal_allocation.csv](outputs/optimal_allocation.csv)
  - **Scenario summary:** [outputs/scenario_results.csv](outputs/scenario_results.csv)
  - **Customers:** [data/customers.csv](data/customers.csv)
  - **Warehouses:** [data/warehouses.csv](data/warehouses.csv)

- **Relationships to create (Power BI Model view):**
  - `optimal_allocation[warehouse_id] -> warehouses[warehouse_id]` (one-to-many)
  - `optimal_allocation[customer_id] -> customers[customer_id]` (one-to-many)

- **Recommended measures (DAX)**
  - **Total Logistics Cost:**
    - DAX: `TotalLogisticsCost = SUM(optimal_allocation[total_cost])`
  - **Warehouse Utilization (%):**
    - DAX: `WarehouseUtilization = DIVIDE(SUM(optimal_allocation[quantity]), SUM(warehouses[capacity]), 0)`
    - Use on a per-warehouse visual; format as percentage.
  - **Total Demand (by customer):**
    - DAX: `TotalDemand = SUM(customers[demand])`
  - **Total Supplied (by customer):**
    - DAX: `TotalSupplied = SUM(optimal_allocation[quantity])`
  - **Unmet Demand (if any):**
    - DAX: `UnmetDemand = [TotalDemand] - [TotalSupplied]`
  - **Scenario Total Cost (from scenario table):**
    - Use `scenario_results[total_cost]` directly in visuals.

- **Visuals to build (report page suggestions):**
  1. **Total logistics cost** — Card visual showing `TotalLogisticsCost` filtered by scenario. Use slicer on `scenario` if you import per-scenario allocation tables or switch to scenario folder.
  2. **Warehouse utilization** — Bar chart: axis = `warehouses[warehouse_id]`, values = `WarehouseUtilization` (format %). Add tooltip with `SUM(optimal_allocation[quantity])` and `warehouses[capacity]`.
  3. **Demand vs Supply** — Combined clustered bar chart: axis = `customers[customer_id]`, values = `TotalDemand` and `TotalSupplied`. Add small multiples or a table for details.
  4. **Scenario comparison** — Bar chart using [outputs/scenario_results.csv](outputs/scenario_results.csv): axis = `scenario`, value = `total_cost`. Optionally add `status` as color.

- **Filter & slicer suggestions**
  - Slicer for `scenario` (if using scenario summary table) or a dropdown to switch data sources.
  
- **Practical notes**
  - If you want to compare allocations for each scenario in visuals, import each `outputs/scenario_<name>/optimal_allocation.csv` and add a `scenario` column (Power Query: add column with fixed value). Append them into a single `Allocations` table, then use `scenario` as a slicer.
  - Refresh: set `Data Source` to folder-level for scenario CSVs if you'll append many scenario files.

---

If you want, I can produce the appended `Allocations` CSV (all scenarios combined) so the report can use a single table for allocation rows.
