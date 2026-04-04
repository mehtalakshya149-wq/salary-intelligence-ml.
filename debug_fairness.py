
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from ml.src.fairness import run_bias_audit
import json

try:
    report = run_bias_audit()
    print("RECORDS ANALYZED:", report['records_analyzed'])
    print("BIAS FLAGS COUNT:", len(report['bias_flags']))
    print("FAIRNESS SCORE:", report['fairness_score'])
    
    total_groups = sum(len(report["dimensions"][d]) for d in report["dimensions"])
    print("TOTAL GROUPS ANALYZED:", total_groups)
    
    under_flags = sum(1 for f in report["bias_flags"] if f["status"] == "Flagged - Underrepresented")
    over_flags = sum(1 for f in report["bias_flags"] if f["status"] == "Flagged - Overrepresented")
    print(f"FLAGS: {under_flags} Under, {over_flags} Over")

    # Re-simulating the math
    total_penalty = (under_flags * 10) + (over_flags * 5)
    denominator = (total_groups * 10)
    score = 100.0 * (1.0 - (total_penalty / denominator))
    print("SIMULATED SCORE:", score)

except Exception as e:
    print(f"ERROR: {e}")
