import pandas as pd
import numpy as np
from ml.src.preprocess import load_config, load_data, clean_data

def compute_disparate_impact(df: pd.DataFrame, target_col: str, protected_attribute: str) -> dict:
    """
    Computes a simplified Structural Disparate Impact mathematically comparing the median salary
    of different classes within a protected attribute against the global median to flag systemic reporting biases.
    """
    if protected_attribute not in df.columns:
        return {"error": f"Attribute {protected_attribute} not structurally detected in dataset."}
        
    global_median = df[target_col].median()
    group_stats = df.groupby(protected_attribute)[target_col].median()
    
    anomalies = {}
    for group, median in group_stats.items():
        ratio = median / global_median
        if ratio < 0.8: # Traditional 80% rule
            anomalies[group] = {"median": median, "ratio_to_global": round(ratio, 2), "status": "Flagged - Underrepresented"}
        elif ratio > 1.25:
            anomalies[group] = {"median": median, "ratio_to_global": round(ratio, 2), "status": "Flagged - Overrepresented"}
            
    return {
        "attribute": protected_attribute,
        "global_median": global_median,
        "group_medians": group_stats.to_dict(),
        "disparate_impact_flags": anomalies
    }

def get_fairness_report(config_path="ml/config.yaml"):
    config = load_config(config_path)
    df = clean_data(load_data(config["paths"]["raw_data"]), config)
    target = config["features"]["target"]
    
    # Analyze by Experience Level as a proxy
    exp_impact = compute_disparate_impact(df, target, "experience_level")
    
    # Analyze by Company Size
    size_impact = compute_disparate_impact(df, target, "company_size")
    
    return {
        "experience_level_bias": exp_impact,
        "company_size_bias": size_impact,
        "records_evaluated": len(df)
    }
