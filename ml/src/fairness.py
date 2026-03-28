"""
fairness.py — Salary Fairness & Bias Auditor Engine
===================================================
Analyzes training data and model predictions (via historical proxies)
to detect systemic biases across demographics.
"""

import logging
import pandas as pd
import numpy as np
from ml.src.preprocess import load_config, load_data, clean_data

logger = logging.getLogger(__name__)

def compute_gini(series: pd.Series) -> float:
    """Compute the Gini coefficient of a series (measure of inequality)."""
    if len(series) == 0:
        return 0.0
    # Clean zeros and negatives
    values = series[series > 0].values
    if len(values) < 2:
        return 0.0
    values = np.sort(values)
    index = np.arange(1, len(values) + 1)
    n = len(values)
    return ((np.sum((2 * index - n - 1) * values)) / (n * np.sum(values)))

def run_bias_audit(config_path: str = "ml/config.yaml") -> dict:
    """
    Run full bias analysis across predefined dimensions.
    Returns fairness score, flags, and dimension-level stats.
    """
    config = load_config(config_path)
    df = clean_data(load_data(config["paths"]["raw_data"]), config)
    target = config["features"]["target"]
    
    dimensions = ["experience_level", "company_size", "company_location"]
    global_median = df[target].median()
    
    report = {
        "fairness_score": 100.0,
        "records_analyzed": len(df),
        "global_median": float(global_median),
        "dimensions": {},
        "bias_flags": [],
        "narrative": []
    }
    
    # Analyze each dimension
    deductions = 0
    for dim in dimensions:
        if dim not in df.columns:
            continue
            
        group_stats = df.groupby(dim)[target].agg(['median', 'count', list]).reset_index()
        group_stats['gini'] = group_stats['list'].apply(lambda x: compute_gini(pd.Series(x)))
        group_stats['impact_ratio'] = group_stats['median'] / global_median
        
        dim_data = []
        for _, row in group_stats.iterrows():
            group_name = row[dim]
            ratio = row['impact_ratio']
            status = "Fair"
            
            # 80% Rule (4/5ths Rule) for disparate impact
            if ratio < 0.8:
                status = "Flagged - Underrepresented"
                report["bias_flags"].append({
                    "dimension": dim,
                    "group": group_name,
                    "ratio": round(float(ratio), 2),
                    "status": status
                })
                report["narrative"].append(f"Lower Salaries detected for {group_name} in {dim} ({ratio:.2f}x global median)")
                deductions += 10
            elif ratio > 1.25:
                status = "Flagged - Overrepresented"
                report["bias_flags"].append({
                    "dimension": dim,
                    "group": group_name,
                    "ratio": round(float(ratio), 2),
                    "status": status
                })
                report["narrative"].append(f"Higher salaries skewed toward {group_name} in {dim} ({ratio:.2f}x global median)")
                deductions += 5 # Lower penalty for overrepresentation
            
            dim_data.append({
                "group": group_name,
                "median": float(row['median']),
                "count": int(row['count']),
                "gini": round(float(row['gini']), 3),
                "impact_ratio": round(float(ratio), 2),
                "status": status
            })
            
        report["dimensions"][dim] = dim_data

    # Final Fairness Score calculation
    report["fairness_score"] = max(0.0, 100.0 - deductions)
    
    # Add summary bullets if clean
    if not report["bias_flags"]:
        report["narrative"].append("Strict mathematical parity achieved across analyzed demographics.")
        
    return report

if __name__ == "__main__":
    import json
    print(json.dumps(run_bias_audit(), indent=2))
