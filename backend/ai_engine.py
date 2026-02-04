import ollama
import json
import re
from openai import OpenAI
import anthropic
import google.generativeai as genai

SYSTEM_PROMPT = """
You are a receipt scanner. Extract the following fields from the image text:
- vendor_name (string)
- date (YYYY-MM-DD)
- total_amount (float)
- tax_amount (float)
- category (Food, Travel, Utilities, Office, Other)
- items (list of strings)

Return ONLY valid JSON. Do not include markdown formatting like ```json.
"""

def clean_json(text):
    """Extracts JSON object from text using regex if standard parsing fails."""
    try:
        # Try finding the first { and last }
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            return match.group(1)
        return text
    except:
        return text

def scan_receipt(file_path: str, provider: str, model_id: str, api_key: str = None):
    try:
        content = ""
        print(f"DEBUG: Processing {file_path} with {model_id}...")

        if provider == "Local (Ollama)":
            response = ollama.chat(
                model=model_id,
                messages=[{
                    'role': 'user',
                    'content': SYSTEM_PROMPT + "\\nAnalyze this image.",
                    'images': [file_path]
                }]
            )
            content = response['message']['content']

        elif provider == "Gemini":
            genai.configure(api_key=api_key)
            # Gemini handles PDFs and Images natively via File API, 
            # but for simple images, we can use the Vision model directly.
            # (Simplified for image-only in this snippet, PDF requires File API)
            model = genai.GenerativeModel(model_id)
            
            # Load image data
            with open(file_path, "rb") as f:
                image_data = f.read()
                
            response = model.generate_content([
                SYSTEM_PROMPT,
                {"mime_type": "image/jpeg", "data": image_data}
            ])
            content = response.text

        elif provider == "OpenAI":
            # Placeholder for OpenAI Vision
            return {"error": "OpenAI Vision implementation pending"}

        # --- Debugging & Cleaning ---
        print(f"DEBUG: Raw AI Response: {content}") 
        
        # Remove Markdown
        cleaned_content = content.replace("```json", "").replace("```", "").strip()
        cleaned_content = clean_json(cleaned_content)

        return json.loads(cleaned_content)

    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_output": content}
    except Exception as e:
        return {"error": str(e)}

def get_available_models(provider: str, api_key: str = None):
    # ... (Same as previous version) ...
    models = []
    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=api_key)
            models = [m.id for m in client.models.list() if "gpt" in m.id]
        elif provider == "Gemini":
            genai.configure(api_key=api_key)
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    models.append(m.name.replace("models/", ""))
        elif provider == "Claude":
            client = anthropic.Anthropic(api_key=api_key)
            try:
                models = [m.id for m in client.models.list()]
            except:
                models = ["claude-3-5-sonnet-20240620"]
        elif provider == "Local (Ollama)":
            ollama_models = ollama.list()
            if 'models' in ollama_models:
                models = [m['name'] for m in ollama_models['models']]
            else:
                models = [m['name'] for m in ollama_models]
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []
    return sorted(models)

def analyze_spending(expenses: list, provider: str, model_id: str, api_key: str):
    prompt = f"Analyze this expense history: {json.dumps(expenses)}"
    try:
        if provider == "Local (Ollama)":
            response = ollama.chat(model=model_id, messages=[{'role': 'user', 'content': prompt}])
            return response['message']['content']
        # Add other providers here as in previous turn
        return "Analysis placeholder"
    except Exception as e:
        return str(e)