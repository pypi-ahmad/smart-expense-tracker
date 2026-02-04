from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Expense(BaseModel):
    vendor_name: str
    date: str
    total_amount: float
    tax_amount: float = 0.0
    category: str
    items: List[str]

class AnalysisRequest(BaseModel):
    expenses: List[Dict[str, Any]]
    provider: str
    model: str
    api_key: Optional[str] = None