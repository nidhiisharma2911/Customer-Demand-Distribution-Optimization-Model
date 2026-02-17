"""Optimization model to allocate shipments from warehouses to customers minimizing transport cost.

Reads CSVs from `data/`:
- customers.csv (customer_id, x, y, demand)
- warehouses.csv (warehouse_id, x, y, capacity)
- transport_cost.csv (warehouse_id, customer_id, cost_per_unit)

Writes results to `outputs/optimal_allocation.csv` with columns:
warehouse_id,customer_id,quantity,cost_per_unit,total_cost
Prints the minimum total cost and solver status.
"""
from pathlib import Path
import pandas as pd

def build_and_solve(customers_fp: Path, warehouses_fp: Path, transport_fp: Path, out_fp: Path):
    # Read data
    customers = pd.read_csv(customers_fp)
    warehouses = pd.read_csv(warehouses_fp)
    transport = pd.read_csv(transport_fp)

    # Prepare dictionaries
    demand = customers.set_index('customer_id')['demand'].to_dict()
    capacity = warehouses.set_index('warehouse_id')['capacity'].to_dict()

    # Build cost mapping
    # transport may contain a subset or superset; create dict of costs
    cost = {(row.warehouse_id, row.customer_id): row.cost_per_unit for row in transport.itertuples()}

    # Check that every customer has demand and that there is at least one feasible warehouse
    for c in demand:
        # ensure at least one warehouse has cost entry; if not, raise
        if not any((w, c) in cost for w in capacity.keys()):
            raise ValueError(f"No transport cost available for customer {c} from any warehouse")

    # Solve LP using pulp
    try:
        import pulp
    except Exception as e:
        raise RuntimeError("The 'pulp' package is required to run optimization. Install with 'pip install pulp'") from e

    # Create LP problem
    prob = pulp.LpProblem('WarehouseAllocation', pulp.LpMinimize)

    # Decision variables: shipment quantities (continuous, >=0)
    x = {}
    for w in capacity:
        for c in demand:
            key = (w, c)
            # use provided cost if available, else a large penalty to discourage use
            unit_cost = cost.get(key, 1e6)
            x[key] = pulp.LpVariable(f'x_{w}_{c}', lowBound=0, cat='Continuous')

    # Objective: minimize total transport cost
    prob += pulp.lpSum((cost.get((w, c), 1e6) * x[(w, c)]) for w in capacity for c in demand)

    # Constraints: satisfy customer demand
    for c in demand:
        prob += pulp.lpSum(x[(w, c)] for w in capacity) == demand[c]

    # Constraints: do not exceed warehouse capacity
    for w in capacity:
        prob += pulp.lpSum(x[(w, c)] for c in demand) <= capacity[w]

    # Solve
    solver = pulp.PULP_CBC_CMD(msg=False)
    result = prob.solve(solver)

    status = pulp.LpStatus[prob.status]
    total_cost = pulp.value(prob.objective)

    # Collect shipments with non-zero quantity
    rows = []
    for (w, c), var in x.items():
        qty = var.value() if var.value() is not None else 0.0
        if qty is None:
            qty = 0.0
        if qty > 1e-9:
            unit_cost = cost.get((w, c), float('inf'))
            rows.append({
                'warehouse_id': w,
                'customer_id': c,
                'quantity': float(qty),
                'cost_per_unit': float(unit_cost),
                'total_cost': float(qty) * float(unit_cost)
            })

    df_out = pd.DataFrame(rows)
    # If no shipments (infeasible), create empty file with headers
    if df_out.empty:
        df_out = pd.DataFrame(columns=['warehouse_id','customer_id','quantity','cost_per_unit','total_cost'])

    out_fp.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(out_fp, index=False)

    # Print summary
    print(f"Solver status: {status}")
    if total_cost is None:
        print("No objective value (problem may be infeasible).")
    else:
        print(f"Minimum total cost: {total_cost}")

    return {'status': status, 'total_cost': total_cost, 'output_path': str(out_fp)}


def main():
    base = Path(__file__).resolve().parents[1]
    data_dir = base / 'data'
    out_dir = base / 'outputs'

    customers_fp = data_dir / 'customers.csv'
    warehouses_fp = data_dir / 'warehouses.csv'
    transport_fp = data_dir / 'transport_cost.csv'
    out_fp = out_dir / 'optimal_allocation.csv'

    res = build_and_solve(customers_fp, warehouses_fp, transport_fp, out_fp)
    return res


if __name__ == '__main__':
    main()
