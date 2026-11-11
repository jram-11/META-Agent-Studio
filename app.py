import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Meta-Agent Studio")
templates = Jinja2Templates(directory="templates")

class TaskRequest(BaseModel):
    goal: str

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/create-agents")
async def create_and_run_agents(data: TaskRequest):
    try:
        # Step 1: Meta-Agent designs the specialized agent team
        architect = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI Meta-Architect. Analyze the user's goal and create 2 to 4 specialized AI agents to complete it. "
                        "Return ONLY valid JSON with a key 'agents' containing a list of objects. "
                        "Each object must have: 'name', 'role', 'system_prompt', and 'task'."
                    )
                },
                {"role": "user", "content": data.goal}
            ]
        )

        plan = json.loads(architect.choices[0].message.content)
        agents = plan.get("agents", [])
        
        results = []
        shared_memory = ""

        # Step 2: Python backend runs each newly created agent sequentially
        for agent in agents:
            worker = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": agent["system_prompt"]},
                    {
                        "role": "user",
                        "content": (
                            f"Overall User Goal: {data.goal}\n"
                            f"Work completed by previous agents:\n{shared_memory}\n\n"
                            f"Your Specific Task: {agent['task']}"
                        )
                    }
                ]
            )
            
            agent_output = worker.choices[0].message.content
            shared_memory += f"\n[{agent['name']} - {agent['role']}]:\n{agent_output}\n"
            
            results.append({
                "name": agent["name"],
                "role": agent["role"],
                "task": agent["task"],
                "output": agent_output
            })

        return JSONResponse({"status": "success", "team": results})

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
