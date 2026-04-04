import os
import joblib
import numpy as np
import logging
from fastapi import APIRouter, HTTPException
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from ml.src.preprocess import load_config

router = APIRouter()
logger = logging.getLogger(__name__)

def evaluate_models(config_path: str = "ml/config.yaml") -> dict:
    """
    Loads saved models and the test dataset, then computes comparison metrics.
    """
    try:
        config = load_config(config_path)
        model_dir = config["paths"]["model_dir"]
        
        # Define paths
        rf_path = os.path.join(model_dir, "random_forest.joblib")
        gb_path = os.path.join(model_dir, "gradient_boosting.joblib")
        test_path = os.path.join(model_dir, "test_data.joblib")
        
        # Verify existence
        if not (os.path.exists(rf_path) and os.path.exists(gb_path) and os.path.exists(test_path)):
            raise FileNotFoundError("Missing model or test data joblib files. Ensure the model has been trained.")
            
        # Load artifacts
        rf_model = joblib.load(rf_path)
        gb_model = joblib.load(gb_path)
        test_data = joblib.load(test_path)
        
        X_test = test_data["X_test"]
        y_test = test_data["y_test"].values
        
        # Inference
        rf_preds = rf_model.predict(X_test)
        gb_preds = gb_model.predict(X_test)
        
        # Compute metrics
        def calc_metrics(y_true, y_pred):
            return {
                "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
                "mae": float(mean_absolute_error(y_true, y_pred)),
                "r2": float(r2_score(y_true, y_pred))
            }
            
        return {
            "random_forest": calc_metrics(y_test, rf_preds),
            "gradient_boosting": calc_metrics(y_test, gb_preds)
        }
    except Exception as e:
        logger.error(f"Error evaluating models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-comparison-metrics")
def get_model_comparison_metrics():
    """Endpoint serving real-time model evaluation metrics."""
    return evaluate_models()
