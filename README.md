# Customer Demand Distribution Optimization Model

A Python-based optimization model that minimizes transportation costs by optimally allocating customer demand across multiple warehouses using linear programming.

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Input Data](#input-data)
- [Usage](#usage)
- [Scenario Analysis](#scenario-analysis)
- [Testing](#testing)
- [Outputs](#outputs)
- [Dashboard](#dashboard)
- [Contributing](#contributing)

## Overview

This project solves the **Warehouse Allocation Problem** — a classic optimization challenge in supply chain management. Given customer demand, warehouse capacity, and transportation costs, the model determines the optimal shipment allocation from warehouses to customers that minimizes total transportation costs while satisfying all constraints.

The solution uses **linear programming** with the PuLP library and can evaluate multiple scenarios to understand how business changes impact costs and feasibility.

## Problem Statement

**Given:**
- Multiple warehouses with limited capacity
- Multiple customers with known demand
- Transportation cost per unit between each warehouse-customer pair
- Geographic locations (x, y coordinates) of warehouses and customers

**Objective:**
Minimize total transportation cost by determining optimal shipment quantities from each warehouse to each customer

**Constraints:**
- Customer demand must be fully satisfied
- Warehouse capacity cannot be exceeded
- Shipment quantities must be non-negative

## Features

✅ **Linear Programming Optimization** — Uses PuLP with default solver for efficient solutions  
✅ **Multi-Scenario Analysis** — Compare baseline vs. demand changes, capacity reductions, and cost increases  
✅ **Data-Driven** — CSV-based input with flexible schema  
✅ **Reproducible** — Pinned dependencies for consistent environment  
✅ **Interactive Analysis** — Jupyter notebooks for scenario exploration  
✅ **Business Intelligence Ready** — Power BI integration for dashboard visualization  
✅ **Comprehensive Testing** — Unit tests for optimization correctness and infeasibility detection

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Customer-Demand-Distribution-Optimization-Model
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Run the Optimization Model

To solve the baseline warehouse allocation problem:

```bash
python -m src.main
```

This will:
- Read customer, warehouse, and transport cost data from `data/` folder
- Solve the optimization problem
- Output the optimal allocation to `outputs/optimal_allocation.csv`

### Run Scenario Analysis

To run all four predefined scenarios:

```bash
python -m src.run_scenarios
```

This generates:
- Individual scenario allocations in `outputs/scenario_<name>/optimal_allocation.csv`
- A summary comparison in `outputs/scenario_results.csv`

### Explore in Jupyter

For interactive analysis:

```bash
jupyter notebook notebooks/
```

Available notebooks:
- `demand_analysis.ipynb` — Exploratory data analysis of customer and warehouse data
- `scenario_analysis.ipynb` — Interactive scenario comparison and visualization

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py                      # Entry point (runs single optimization)
│   ├── optimization_model.py         # Core LP optimization logic
│   ├── run_scenarios.py              # Scenario runner
│   └── __pycache__/
├── data/
│   ├── customers.csv                # Customer data (id, x, y, demand)
│   ├── warehouses.csv               # Warehouse data (id, x, y, capacity)
│   └── transport_cost.csv           # Cost matrix (warehouse_id, customer_id, cost_per_unit)
├── outputs/
│   ├── optimal_allocation.csv       # Baseline solution
│   ├── scenario_results.csv         # Scenario comparison summary
│   ├── allocations_folder/          # Individual scenario allocations
│   └── scenario_*/                  # Scenario output folders
├── notebooks/
│   ├── demand_analysis.ipynb        # Data exploration
│   └── scenario_analysis.ipynb      # Scenario analysis
├── dashboard/
│   ├── powerbi_spec.json            # Power BI configuration
│   ├── powerquery_import_allocations.pq
│   └── README.md                    # Dashboard setup instructions
├── tests/
│   ├── test_optimization_model.py   # Unit tests
│   └── test_optimization_infeasible.py
├── requirements.txt
├── README.md                        # This file
├── CONTRIBUTING.md
└── LICENSE
```

## Input Data

### customers.csv

| Column | Type | Description |
|--------|------|-------------|
| customer_id | string | Unique customer identifier |
| x | float | X-coordinate of customer location |
| y | float | Y-coordinate of customer location |
| demand | float | Customer demand quantity |

### warehouses.csv

| Column | Type | Description |
|--------|------|-------------|
| warehouse_id | string | Unique warehouse identifier |
| x | float | X-coordinate of warehouse location |
| y | float | Y-coordinate of warehouse location |
| capacity | float | Maximum capacity available |

### transport_cost.csv

| Column | Type | Description |
|--------|------|-------------|
| warehouse_id | string | Source warehouse |
| customer_id | string | Destination customer |
| cost_per_unit | float | Cost per unit shipped |

## Usage

### Python API

```python
from pathlib import Path
from src.optimization_model import build_and_solve

# Define file paths
customers_fp = Path('data/customers.csv')
warehouses_fp = Path('data/warehouses.csv')
transport_fp = Path('data/transport_cost.csv')
output_fp = Path('outputs/optimal_allocation.csv')

# Run optimization
build_and_solve(customers_fp, warehouses_fp, transport_fp, output_fp)
```

### Output Format

The solution is saved to `optimal_allocation.csv` with columns:

| Column | Description |
|--------|-------------|
| warehouse_id | Source warehouse |
| customer_id | Destination customer |
| quantity | Optimal shipment quantity |
| cost_per_unit | Unit cost |
| total_cost | quantity × cost_per_unit |

## Scenario Analysis

The model includes four predefined scenarios to test robustness:

### Baseline
No modifications to the data. Serves as the reference point.

### Demand Increase (+20%)
All customer demands increased by 20%. Tests capacity sufficiency.

### Capacity Reduction (-30%)
All warehouse capacities reduced by 30%. Tests feasibility and cost impact.

### Cost Increase (+25%)
All transportation costs increased by 25%. Tests cost sensitivity.

Each scenario generates its own optimal allocation, allowing decision-makers to understand how business changes impact operations.

## Testing

Run the test suite to verify the optimization model:

```bash
pytest tests/ -v
```

Tests include:
- ✓ Feasible problem solutions with correct constraint satisfaction
- ✓ Infeasibility detection (when total capacity < total demand)
- ✓ Objective function validation

## Outputs

### Generated Files

After running the model:

- **`outputs/optimal_allocation.csv`** — Optimal allocation for the baseline scenario
- **`outputs/scenario_results.csv`** — Summary metrics for all scenarios (total cost, feasibility, etc.)
- **`outputs/scenario_*/optimal_allocation.csv`** — Individual scenario solutions

### Key Metrics

- **Total Cost** — Sum of (quantity × cost_per_unit) across all allocations
- **Solver Status** — "Optimal", "Infeasible", or other status from the optimization engine
- **Constraint Satisfaction** — Whether demand is met and capacity is respected

## Dashboard

A Power BI dashboard is provided for interactive visualization of results:

📊 **Setup Instructions:** See [dashboard/README.md](dashboard/README.md)

The dashboard includes:
- Allocation heatmaps by scenario
- Cost breakdowns and trends
- Capacity utilization charts
- Scenario comparison metrics

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and testing requirements
- PR workflow
- Documentation standards
- Data file handling

Before submitting a PR, ensure:
- All tests pass: `pytest tests/ -v`
- Code is well-documented
- Changes are focused and minimal

---

**Built with:** Python · PuLP · Pandas · Jupyter · Power BI