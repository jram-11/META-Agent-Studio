# ⚡ Meta-Agent Studio

A full-stack AI agent factory built with **Python (FastAPI)** and **HTML/JS**. Give the system a complex goal, and the Meta-Agent dynamically creates specialized sub-agents, assigns their roles, and passes context between them to complete the mission.

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd meta-agent-studio
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API Key:**
   Create a `.env` file in the root folder and add your OpenAI key:
   ```env
   OPENAI_API_KEY=sk-your-api-key-here
   ```

4. **Run the application:**
   ```bash
   uvicorn app:app --reload
   ```
   Open your browser and go to `http://127.0.0.1:8000`
