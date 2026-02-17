import pandas as pd
from pathlib import Path
from src.optimization_model import build_and_solve


def test_infeasible_when_capacity_insufficient(tmp_path):
    # Create data where total warehouse capacity < total demand
    customers = pd.DataFrame([
        {"customer_id": "C1", "x": 0.0, "y": 0.0, "demand": 100},
        {"customer_id": "C2", "x": 1.0, "y": 1.0, "demand": 50},
    ])
    warehouses = pd.DataFrame([
        {"warehouse_id": "W1", "x": 0.0, "y": 0.0, "capacity": 50},
    ])
    transport = pd.DataFrame([
        {"warehouse_id": "W1", "customer_id": "C1", "cost_per_unit": 1.0},
        {"warehouse_id": "W1", "customer_id": "C2", "cost_per_unit": 1.0},
    ])

    customers_fp = tmp_path / 'customers.csv'
    warehouses_fp = tmp_path / 'warehouses.csv'
    transport_fp = tmp_path / 'transport_cost.csv'
    out_fp = tmp_path / 'optimal_allocation.csv'

    customers.to_csv(customers_fp, index=False)
    warehouses.to_csv(warehouses_fp, index=False)
    transport.to_csv(transport_fp, index=False)

    res = build_and_solve(customers_fp, warehouses_fp, transport_fp, out_fp)

    # Solver should not report Optimal because capacity < demand
    assert res['status'] != 'Optimal'
*** End Patch