from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import pandas as pd
from backend.database import init_db, save_expense, get_expenses
from backend.ai_engine import scan_receipt, get_available_models, analyze_spending
from backend.models import AnalysisRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("backend/uploads", exist_ok=True)
init_db()

@app.post("/scan")
async def scan_invoice(
    file: UploadFile = File(...), 
    provider: str = Form(...),
    model: str = Form(...),
    api_key: str = Form(None)
):
    file_location = f"backend/uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # --- Check File Type ---
    ext = file.filename.split('.')[-1].lower()
    
    # 1. Handle Bulk Data (CSV/Excel)
    if ext in ['csv', 'xlsx', 'xls']:
        try:
            if ext == 'csv':
                df = pd.read_csv(file_location)
            else:
                df = pd.read_excel(file_location)
            
            # Normalize headers (basic mapping)
            # Expects columns like: vendor, date, total, category
            saved_count = 0
            for _, row in df.iterrows():
                # Simple fallback mapping
                data = {
                    "vendor_name": row.get('vendor', row.get('Vendor', 'Unknown')),
                    "date": str(row.get('date', row.get('Date', '2024-01-01'))),
                    "total_amount": float(row.get('total', row.get('Amount', 0.0))),
                    "category": row.get('category', row.get('Category', 'Other')),
                    "items": []
                }
                save_expense(data)
                saved_count += 1
            
            return {"message": f"Successfully imported {saved_count} records", "type": "bulk_import"}
            
        except Exception as e:
             raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")

    # 2. Handle PDF (Placeholder/Basic text)
    elif ext == 'pdf':
        # For now, treat PDF as an error or specialized flow. 
        # Real PDF OCR requires 'pdf2image' or specialized AI models.
        # We will attempt to pass it to AI, but Local Ollama might fail if not multimodal.
        pass 

    # 3. Handle Images (Normal AI Scan)
    data = scan_receipt(file_location, provider, model, api_key)
    
    if "error" not in data:
        save_expense(data)
    else:
        # Pass the raw output back so you can debug "Expecting value" errors
        error_msg = data.get("error")
        raw_out = data.get("raw_output", "")
        raise HTTPException(status_code=500, detail=f"{error_msg}. Raw AI Output: {raw_out}")
        
    return data

@app.get("/expenses")
def read_expenses():
    return get_expenses()

@app.post("/models")
def list_models(provider: str = Form(...), api_key: str = Form(None)):
    return {"models": get_available_models(provider, api_key)}

@app.post("/analyze")
def analyze(request: AnalysisRequest):
    return {"advice": analyze_spending(request.expenses, request.provider, request.model, request.api_key)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)