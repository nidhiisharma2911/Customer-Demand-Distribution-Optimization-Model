"""Run scenario experiments programmatically and save results.

Scenarios:
- baseline
- demand_increase_20pct
- capacity_reduction_30pct
- cost_increase_25pct

Writes per-scenario allocation CSVs in `outputs/scenario_<name>/optimal_allocation.csv`
and a summary `outputs/scenario_results.csv`.
"""
from pathlib import Path
import pandas as pd
from src.optimization_model import build_and_solve


def run():
    base = Path(__file__).resolve().parents[1]
    data_dir = base / 'data'
    out_dir = base / 'outputs'
    out_dir.mkdir(parents=True, exist_ok=True)

    customers = pd.read_csv(data_dir / 'customers.csv')
    warehouses = pd.read_csv(data_dir / 'warehouses.csv')
    transport = pd.read_csv(data_dir / 'transport_cost.csv')

    results = []

    def run_scenario(name, cust_df=None, wh_df=None, tr_df=None):
        scenario_dir = out_dir / f'scenario_{name}'
        scenario_dir.mkdir(parents=True, exist_ok=True)

        cust_fp = scenario_dir / 'customers.csv'
        wh_fp = scenario_dir / 'warehouses.csv'
        tr_fp = scenario_dir / 'transport_cost.csv'
        out_fp = scenario_dir / 'optimal_allocation.csv'

        (cust_df if cust_df is not None else customers).to_csv(cust_fp, index=False)
        (wh_df if wh_df is not None else warehouses).to_csv(wh_fp, index=False)
        (tr_df if tr_df is not None else transport).to_csv(tr_fp, index=False)

        res = build_and_solve(cust_fp, wh_fp, tr_fp, out_fp)
        results.append({'scenario': name, 'total_cost': res.get('total_cost'), 'status': res.get('status'), 'allocation_csv': res.get('output_path')})

    # Baseline
    run_scenario('baseline')

    # Demand +20%
    cust_up = customers.copy()
    cust_up['demand'] = (cust_up['demand'] * 1.2).round().astype(int)
    run_scenario('demand_increase_20pct', cust_df=cust_up)

    # Capacity -30%
    wh_down = warehouses.copy()
    wh_down['capacity'] = (wh_down['capacity'] * 0.7).apply(int)
    run_scenario('capacity_reduction_30pct', wh_df=wh_down)

    # Cost +25%
    tr_up = transport.copy()
    tr_up['cost_per_unit'] = tr_up['cost_per_unit'] * 1.25
    run_scenario('cost_increase_25pct', tr_df=tr_up)

    # Save summary
    df_res = pd.DataFrame(results)
    df_res.to_csv(out_dir / 'scenario_results.csv', index=False)
    print('Wrote', out_dir / 'scenario_results.csv')


if __name__ == '__main__':
    run()
