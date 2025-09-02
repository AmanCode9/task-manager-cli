# Task Manager Pro

A full-featured task management application built with Python, featuring both GUI and API interfaces.

## 📋 Features

### Core Functionality
- ✅ **Add Tasks** - Create tasks with title, description, and due dates
- ✅ **Edit Tasks** - Modify existing tasks
- ✅ **Mark Complete** - Track task completion status
- ✅ **Delete Tasks** - Remove unwanted tasks
- ✅ **Search Tasks** - Find tasks by keywords
- ✅ **Persistent Storage** - Tasks saved to JSON file
- ✅ **Date Validation** - Proper date format handling

### User Interfaces
- 🖥️ **Desktop GUI** - Clean Tkinter interface
- 🌐 **REST API** - FastAPI backend for web integration
- 📖 **Interactive API Docs** - Swagger/OpenAPI documentation

## 🚀 Quick Start

### Prerequisites
```bash
pip install tkinter fastapi uvicorn
```

### Run the Desktop GUI
```bash
python gui.py
```

### Run the API Server
```bash
python api.py
```
- API Documentation: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

## 📁 Project Structure

```
task-manager/
├── tasks.py          # Core task management logic
├── gui.py            # Tkinter desktop interface
├── api.py            # FastAPI web interface
├── tasks.json        # Data storage (auto-created)
└── README.md         # Project documentation
```

## 🏗️ Architecture

### Data Layer (`tasks.py`)
- **Task Class** - Dataclass representing individual tasks
- **TaskManager Class** - Handles CRUD operations and data persistence
- **JSON Storage** - Lightweight file-based data storage

### GUI Layer (`gui.py`)
- **Tkinter Interface** - Native desktop application
- **Search Functionality** - Real-time task filtering
- **Edit Dialog** - Modal windows for task modification
- **Double-click Details** - Quick task information view

### API Layer (`api.py`)
- **FastAPI Framework** - Modern async web framework
- **RESTful Endpoints** - Standard HTTP methods for task operations
- **Pydantic Validation** - Request/response data validation
- **CORS Support** - Ready for frontend integration
- **Auto-documentation** - Swagger UI for API testing

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| POST | `/tasks` | Create new task |
| GET | `/tasks/{id}` | Get specific task |
| PUT | `/tasks/{id}` | Update task |
| PATCH | `/tasks/{id}/complete` | Mark task complete |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/search/{keyword}` | Search tasks |

### Example API Usage

```bash
# Create a new task
curl -X POST "http://127.0.0.1:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Complete project",
       "description": "Finish the task manager",
       "due_date": "2024-12-25"
     }'

# Get all tasks
curl "http://127.0.0.1:8000/tasks"

# Search tasks
curl "http://127.0.0.1:8000/tasks/search/project"
```

## 🔧 Technical Details

### Dependencies
- **Python 3.7+** - Core language
- **dataclasses** - Clean data structures
- **tkinter** - GUI framework (built-in)
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation

### Data Model
```python
@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    due_date: Optional[str] = None
    status: str = "Pending"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
```

### Storage Format
Tasks are stored in `tasks.json`:
```json
[
  {
    "id": 1,
    "title": "Sample Task",
    "description": "Task description",
    "due_date": "2024-12-25",
    "status": "Pending",
    "created_at": "2024-12-01T10:30:00.000000"
  }
]
```

## 🧪 Testing

### Test the Backend
```bash
python tasks.py
```

### Test the GUI
```bash
python gui.py
```

### Test the API
```bash
python api.py
# Visit http://127.0.0.1:8000/docs for interactive testing
```

## 🚀 Future Enhancements

### Planned Features
- [ ] **React Frontend** - Modern web interface
- [ ] **Cloud Deployment** - Deploy on Render/Heroku
- [ ] **Database Integration** - PostgreSQL/SQLite support
- [ ] **User Authentication** - Multi-user support
- [ ] **Task Categories** - Organize tasks by category
- [ ] **Due Date Alerts** - Notifications for upcoming deadlines
- [ ] **Task Priority** - High/Medium/Low priority levels
- [ ] **Export/Import** - CSV/Excel file support

### Technical Improvements
- [ ] **Unit Tests** - Comprehensive test coverage
- [ ] **Docker Support** - Containerized deployment
- [ ] **Database Migrations** - Schema version management
- [ ] **Logging** - Structured logging system
- [ ] **Configuration** - Environment-based config
- [ ] **API Versioning** - Backward compatibility

## 🛠️ Development

### Adding New Features
1. **Backend Logic** - Add methods to `TaskManager` class
2. **GUI Integration** - Add buttons/forms in `TaskManagerGUI`
3. **API Endpoints** - Create new routes in `api.py`
4. **Documentation** - Update README and API docs

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for better code clarity
- Document complex functions with docstrings
- Keep classes focused on single responsibilities

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**[Aman Patra]**
- GitHub: [@AmanCode9](https://github.com/AmanCode9)
- LinkedIn: [aman0910](https://linkedin.com/in/aman0910)
- Email: amanpatra9@gmail.com

## 🙏 Acknowledgments

- Built with Python and modern web frameworks
- Inspired by productivity and task management best practices
- Designed for scalability and maintainability

---

⭐ **Star this repository if you found it helpful!**
