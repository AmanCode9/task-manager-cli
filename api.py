from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from tasks import TaskManager, Task
import uvicorn

# Create FastAPI app
app = FastAPI(title="Task Manager API", version="1.0.0")

# Add CORS middleware to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TaskManager
task_manager = TaskManager()

# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: str = ""
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: Optional[str]
    status: str
    created_at: str

    @classmethod
    def from_task(cls, task: Task):
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            created_at=task.created_at
        )

# API Routes

@app.get("/")
async def root():
    return {"message": "Task Manager API", "version": "1.0.0"}

@app.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks():
    """Get all tasks"""
    tasks = task_manager.get_all()
    return [TaskResponse.from_task(task) for task in tasks]

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task_data: TaskCreate):
    """Create a new task"""
    task = task_manager.add_task(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date
    )
    return TaskResponse.from_task(task)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = task_manager.find(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_task(task)

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_data: TaskUpdate):
    """Update a task"""
    task = task_manager.find(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the task
    success = task_manager.update(
        task_id=task_id,
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update task")
    
    # Return updated task
    updated_task = task_manager.find(task_id)
    return TaskResponse.from_task(updated_task)

@app.patch("/tasks/{task_id}/complete")
async def mark_task_complete(task_id: int):
    """Mark a task as complete"""
    success = task_manager.mark_complete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = task_manager.find(task_id)
    return TaskResponse.from_task(updated_task)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    success = task_manager.delete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": f"Task {task_id} deleted successfully"}

@app.get("/tasks/search/{keyword}", response_model=List[TaskResponse])
async def search_tasks(keyword: str):
    """Search tasks by keyword"""
    tasks = task_manager.search(keyword)
    return [TaskResponse.from_task(task) for task in tasks]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "total_tasks": len(task_manager.get_all()),
        "api_version": "1.0.0"
    }

# Run the server
if __name__ == "__main__":
    print("🚀 Starting Task Manager API...")
    print("📝 API Documentation: http://127.0.0.1:8000/docs")
    print("🔍 Health Check: http://127.0.0.1:8000/health")
    print("📋 All Tasks: http://127.0.0.1:8000/tasks")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",  # Changed to accept all interfaces
        port=8001,       # Changed port to 8001
        reload=True,     # Auto-reload on code changes
        log_level="info"
    )