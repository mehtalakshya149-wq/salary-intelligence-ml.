from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

# Static Cost of Living Index Data (relative to New York City base = 100)
# This mimics global Numbeo or World Bank datasets
COST_OF_LIVING_INDICES = {
    "United States": 100.0,
    "United Kingdom": 82.5,
    "Canada": 88.2,
    "Australia": 95.5,
    "Germany": 85.0,
    "France": 84.1,
    "Singapore": 105.5,
    "Switzerland": 135.0,
    "India": 28.5,
    "Brazil": 40.0,
    "Mexico": 45.2,
    "Japan": 80.5,
    "United Arab Emirates": 78.5
}

class AdjustmentResponse(BaseModel):
    base_salary: float
    base_country: str
    target_country: str
    target_salary_required: float
    purchasing_power_ratio: float

class ComparisonResponse(BaseModel):
    base_salary: float
    base_country: str
    comparisons: List[AdjustmentResponse]

def get_cost_of_living_adjusted_salary(base_salary: float, base_country: str) -> ComparisonResponse:
    if base_country not in COST_OF_LIVING_INDICES:
        raise HTTPException(status_code=400, detail=f"Base country '{base_country}' not found in dataset.")
    
    base_idx = COST_OF_LIVING_INDICES[base_country]
    comparisons = []
    
    for target_country, target_idx in COST_OF_LIVING_INDICES.items():
        if target_country == base_country:
            continue
            
        # How much money you need in Target Country to have the same lifestyle as base_salary in Base Country
        target_salary_required = (base_salary / base_idx) * target_idx
        
        # Purchasing power ratio (Base Country vs Target Country)
        ppp_ratio = base_idx / target_idx
        
        comparisons.append(AdjustmentResponse(
            base_salary=base_salary,
            base_country=base_country,
            target_country=target_country,
            target_salary_required=round(target_salary_required, 2),
            purchasing_power_ratio=round(ppp_ratio, 2)
        ))
        
    # Sort automatically by the highest equivalent salary required
    comparisons.sort(key=lambda x: x.target_salary_required, reverse=True)
    
    return ComparisonResponse(
        base_salary=base_salary,
        base_country=base_country,
        comparisons=comparisons
    )

@router.get("/cost-of-living-adjusted-salary", response_model=ComparisonResponse)
def api_get_cost_of_living_adjusted_salary(base_salary: float = Query(...), base_country: str = Query(...)):
    """
    Computes the PPP adjusted salary for all countries in the dataset based on the user's current salary and location.
    """
    return get_cost_of_living_adjusted_salary(base_salary, base_country)
