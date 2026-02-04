# 🧾 Smart Expense Tracker

A powerful, AI-driven expense tracking application that allows you to scan receipts, import bulk data, and receive personalized financial advice. Built with **FastAPI**, **Streamlit**, and supports multiple AI providers including **DeepSeek-OCR (Local via Ollama)**, **Gemini**, **OpenAI**, and **Claude**.

![Dashboard Screenshot](https://via.placeholder.com/800x400?text=Smart+Expense+Tracker+Dashboard)

## ✨ Key Features

*   **🤖 Multi-Model AI Scanning**:
    *   **Local Privacy**: Run completely offline using **Ollama** with models like `deepseek-ocr` or `llava`.
    *   **Cloud Power**: Connect to **Google Gemini**, **OpenAI (GPT-4o)**, or **Anthropic Claude** for enhanced accuracy.
*   **📸 Receipt Capture**:
    *   Upload images (JPG, PNG) or PDFs.
    *   **Live Camera Capture** support directly from the browser (mobile/desktop).
*   **📊 Bulk Data Import**:
    *   Import historical data from **CSV** or **Excel (.xlsx)** files.
    *   Auto-maps columns like `Date`, `Vendor`, `Amount`, `Category`.
*   **📈 Interactive Dashboard**:
    *   Visualize spending with **Plotly** charts (Pie & Bar charts).
    *   **Dynamic Time Filters**: Analyze "Last 7 Days", "Last 30 Days", or "All Time".
    *   **Download Reports**: Export filtered data to CSV.
*   **💡 AI Financial Advisor**:
    *   Get actionable tips on how to save money based on your actual spending history.
    *   Identifies "money drains" and unusual patterns.

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) - Interactive UI, Camera Input, Charts.
*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance API.
*   **Database**: SQLite - Lightweight, built-in storage.
*   **AI Engine**:
    *   [Ollama](https://ollama.com/) (Local)
    *   [Google Generative AI SDK](https://ai.google.dev/)
    *   [OpenAI SDK](https://platform.openai.com/)
    *   [Anthropic SDK](https://www.anthropic.com/)
*   **Data Processing**: Pandas, Regex (Robust JSON extraction).

## 🚀 Getting Started

### Prerequisites

*   **Python 3.10+**
*   **(Optional) Ollama**: If you want to use local models.
    *   Download from [ollama.com](https://ollama.com/).
    *   Pull a vision model: `ollama pull deepseek-ocr` (or `llava`).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/smart-expense-tracker.git
    cd smart-expense-tracker
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

You need to run the **Backend** and **Frontend** in separate terminals.

### 1. Start the Backend API
This handles the database, AI processing, and file uploads.
```bash
uvicorn backend.main:app --reload
```
*   Server runs at: `http://localhost:8000`
*   Docs available at: `http://localhost:8000/docs`

### 2. Start the Frontend UI
This launches the web interface in your browser.
```bash
streamlit run frontend/app.py
```
*   App opens at: `http://localhost:8501`

## 📂 Project Structure

```
smart-expense-tracker/
├── backend/
│   ├── uploads/            # Temporary storage for uploaded receipts
│   ├── ai_engine.py        # Logic for Ollama, Gemini, OpenAI, Claude
│   ├── database.py         # SQLite connection and CRUD operations
│   ├── main.py             # FastAPI endpoints (Scan, Analyze, List Models)
│   ├── models.py           # Pydantic data models
│   └── __init__.py
├── frontend/
│   └── app.py              # Streamlit UI (Sidebar, Tabs, Charts)
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

## ⚙️ Configuration

### using Local Models (Free & Private)
1.  Select **"Local (Ollama)"** in the sidebar.
2.  Ensure Ollama is running (`ollama serve`).
3.  Type the model name (e.g., `deepseek-ocr`) or let the app auto-detect available models.

### using Cloud Models
1.  Select **Gemini**, **OpenAI**, or **Claude** in the sidebar.
2.  Enter your **API Key** in the password field.
    *   Keys are sent securely to the backend for that session only and are not stored in the database.

## 🔮 Future Roadmap

*   [ ] User Authentication (Multi-user support).
*   [ ] Advanced Categorization Rules.
*   [ ] Budget Goals & Alerts.
*   [ ] PDF Bank Statement Parsing.
*   [ ] Mobile App (React Native/Flutter).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built with ❤️ by Ahmad*
