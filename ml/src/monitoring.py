import pandas as pd
import numpy as np
from ml.src.preprocess import load_config, load_data, clean_data
from api.database import SessionLocal
from api.models import SalaryPrediction

def detect_live_drift(config_path="ml/config.yaml") -> dict:
    """
    Tracks model performance and data drift by comparing Live inference queries
    (from PostgreSQL) against the historical training baseline medians.
    """
    config = load_config(config_path)
    historic_df = clean_data(load_data(config["paths"]["raw_data"]), config)
    target = config["features"]["target"]
    historic_median = historic_df[target].median()
    historic_std = historic_df[target].std()
    
    try:
        db = SessionLocal()
        preds = db.query(SalaryPrediction).all()
        db.close()
        
        if not preds:
            return {"status": "Awaiting Live Data", "message": "No live predictions have been routed to the Postgres log yet."}
            
        live_predictions = [p.predicted_average for p in preds]
        live_median = np.median(live_predictions)
        
        # Calculate drift
        drift_delta = live_median - historic_median
        drift_z_score = drift_delta / historic_std if historic_std > 0 else 0
        
        status = "Stable"
        if abs(drift_z_score) > 1.5:
            status = "Warning - High Structural Drift Detected (Live inferences skew significantly differently than training data bounds)"
            
        return {
            "status": status,
            "historic_median": historic_median,
            "live_inference_median": live_median,
            "live_queries_analyzed": len(live_predictions),
            "drift_z_score": round(drift_z_score, 2)
        }
    except Exception as e:
        return {"error": f"Failed to interface with live PostgreSQL Monitoring logger: {str(e)}"}
