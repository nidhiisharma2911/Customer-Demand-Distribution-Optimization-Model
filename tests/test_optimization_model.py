import tempfile
from pathlib import Path
import sys
import pandas as pd
# ensure repo root is on PYTHONPATH for tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.optimization_model import build_and_solve


def make_sample_files(tmpdir):
    customers = pd.DataFrame([
        {"customer_id": "C1", "x": 0.0, "y": 0.0, "demand": 10},
        {"customer_id": "C2", "x": 1.0, "y": 1.0, "demand": 5},
    ])
    warehouses = pd.DataFrame([
        {"warehouse_id": "W1", "x": 0.0, "y": 0.0, "capacity": 20},
    ])
    transport = pd.DataFrame([
        {"warehouse_id": "W1", "customer_id": "C1", "cost_per_unit": 1.0},
        {"warehouse_id": "W1", "customer_id": "C2", "cost_per_unit": 2.0},
    ])
    customers_fp = tmpdir / 'customers.csv'
    warehouses_fp = tmpdir / 'warehouses.csv'
    transport_fp = tmpdir / 'transport_cost.csv'
    customers.to_csv(customers_fp, index=False)
    warehouses.to_csv(warehouses_fp, index=False)
    transport.to_csv(transport_fp, index=False)
    return customers_fp, warehouses_fp, transport_fp


def test_build_and_solve_creates_output(tmp_path):
    customers_fp, warehouses_fp, transport_fp = make_sample_files(tmp_path)
    out_fp = tmp_path / 'optimal_allocation.csv'
    res = build_and_solve(customers_fp, warehouses_fp, transport_fp, out_fp)
    assert 'status' in res
    assert Path(res['output_path']).exists()
    df = pd.read_csv(res['output_path'])
    # Quantities should sum to total demand
    total_qty = df['quantity'].sum()
    expected = 10 + 5
    assert abs(total_qty - expected) < 1e-6
