from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json

app = FastAPI()

class TaskRequest(BaseModel):
    task: str  # User task input

def run_playwright_task(task: str):
    """Runs Playwright in a separate subprocess."""
    try:
        result = subprocess.run(
            ["python", "agent.py", json.dumps({"task": task})],
            capture_output=True, text=True
        )
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Subprocess execution failed: {str(e)}"

@app.post("/execute-task")
async def execute_task(request: TaskRequest):
    """Handles user task execution by calling Playwright subprocess."""
    try:
        response = run_playwright_task(request.task)
        return {"task": request.task, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    """Root endpoint to check API status."""
    return {"message": "Task Execution API is running!"}
