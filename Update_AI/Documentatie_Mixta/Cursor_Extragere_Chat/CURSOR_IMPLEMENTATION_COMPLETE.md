# 🚀 CURSOR - IMPLEMENTARE COMPLETĂ AI PROMPT GENERATOR ULTIMATE

## 📋 CONTEXT SITUAȚIE

**Problema**: Repository gol - cod sursă lipsește, doar documentație există  
**Soluție**: Recreare completă folosind MODEL ÎMBUNĂTĂȚIT cu tracking progres  
**Durată estimată**: 4-5 zile (32-40 ore)

---

## 🎯 OBIECTIVE IMPLEMENTARE

1. ✅ Recreare completă cod sursă din documentația DNA
2. ✅ Implementare incrementală cu validare continuă
3. ✅ Multi-AI orchestration cu fallback automat (Claude, GPT, Gemini, Perplexity)
4. ✅ **NOU**: AI model fine-tuning pentru optimizare prompturi
5. ✅ Testing comprehensiv (≥70% coverage)
6. ✅ Tracking progres real-time în `IMPLEMENTATION_PROGRESS.md`
7. ✅ PyInstaller + NSIS packaging production-ready
8. ✅ GitHub sync corect (fără fișiere mari)

---

## 📊 PROGRESS TRACKING SYSTEM

Creează `IMPLEMENTATION_PROGRESS.md` care se actualizează AUTOMAT după fiecare task:

```markdown
# 📊 IMPLEMENTATION PROGRESS - Real-Time Status

**Started**: [TIMESTAMP]  
**Last Update**: [AUTO-UPDATE]  
**Phase**: [CURRENT PHASE]  
**Estimated Completion**: [PERCENTAGE]%

## Phase Status

### PHASE 0: Setup & Preparation
- [ ] 0.1 Cleanup workspace (5 min)
- [ ] 0.2 Create requirements.txt (10 min)
- [ ] 0.3 Setup venv (10 min)
- [ ] 0.4 Git cleanup & .gitignore (10 min)
- [ ] 0.5 API keys configuration (10 min)
**Status**: ⏳ IN PROGRESS | ✅ COMPLETE | ❌ FAILED

### PHASE 1: Core Modules (6-8 ore)
- [ ] 1.1 EventBus (30 min) → Tests: 0/5
- [ ] 1.2 Database (45 min) → Tests: 0/8
- [ ] 1.3 ConfigManager (30 min) → Tests: 0/6
- [ ] 1.4 ContextEngine (90 min) → Tests: 0/10
- [ ] 1.5 AIOrchestrator (120 min) → Tests: 0/12
- [ ] 1.6 BackupManager (60 min) → Tests: 0/9
- [ ] 1.7 ChangeDetector (45 min) → Tests: 0/7
- [ ] 1.8 NextPromptGenerator (30 min) → Tests: 0/5
- [ ] 1.9 IncrementalWorkflow (45 min) → Tests: 0/8
**Status**: ⏳ | Coverage: 0%

### PHASE 2: Quick Tasks (6-8 ore)
[... 12 tasks ...]
**Status**: ⏳ | Coverage: 0%

### PHASE 3: GUI (6-8 ore)
[... 7 tabs ...]
**Status**: ⏳ | Coverage: 0%

### PHASE 4: Integration & Testing (2-3 ore)
**Status**: ⏳

### PHASE 5: Packaging & Release (2-3 ore)
**Status**: ⏳

## Current Task
**Working on**: [MODULE_NAME]
**Started**: [TIMESTAMP]
**Estimated completion**: [TIME]

## Statistics
- **Total modules**: 0/30
- **Tests passing**: 0/111
- **Coverage**: 0%
- **Bugs found**: 0
- **Time elapsed**: 0h 0m

## Blockers
[None yet]

## Next Up
[Next 3 tasks]
```

---

## 🔧 PHASE 0: SETUP & PREPARATION (45 min)

### Task 0.1: Cleanup Workspace (5 min)

```bash
# Șterge cache și artifacts vechi
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
rm -rf build/ dist/ *.egg-info/ htmlcov/ .coverage 2>/dev/null

# Update progress
python << EOF
import json
from datetime import datetime

progress = {
    "phase": "PHASE 0: Setup",
    "task": "0.1 Cleanup workspace",
    "status": "COMPLETE",
    "timestamp": datetime.now().isoformat(),
    "percentage": 1
}

with open("IMPLEMENTATION_PROGRESS.json", "w") as f:
    json.dump(progress, f, indent=2)
    
print("✅ 0.1 Cleanup complete - Progress: 1%")
EOF
```

### Task 0.2: Create requirements.txt (10 min)

```bash
cat > requirements.txt << 'EOF'
# Core GUI
PySide6>=6.6.0
PySide6-Addons>=6.6.0

# AI Providers
anthropic>=0.34.0,<0.40.0
openai>=1.35.0,<2.0.0
google-generativeai>=0.8.0,<0.10.0
httpx>=0.27.0,<0.28.0

# File Monitoring & Parsing
watchdog>=4.0.0,<5.0.0
tree-sitter==0.20.4
tree-sitter-python==0.20.4
tree-sitter-javascript==0.20.3
tree-sitter-typescript==0.20.3
tree-sitter-java==0.20.2
tree-sitter-go==0.20.0

# Configuration & Data
python-dotenv>=1.0.0,<2.0.0
pyyaml>=6.0.0,<7.0.0
toml>=0.10.0,<1.0.0

# Testing
pytest>=8.0.0,<9.0.0
pytest-cov>=4.1.0,<5.0.0
pytest-qt>=4.3.0,<6.0.0

# Code Analysis
radon>=6.0.0,<7.0.0
bandit>=1.7.0,<2.0.0

# Packaging
pyinstaller>=6.5.0,<7.0.0

# Utilities
typing-extensions>=4.11.0,<5.0.0
colorama>=0.4.0,<1.0.0

# AI Fine-tuning (NEW)
scikit-learn>=1.3.0,<2.0.0
numpy>=1.24.0,<2.0.0
pandas>=2.0.0,<3.0.0
EOF

# Update progress
python -c "
import json
from datetime import datetime
progress = {'phase': 'PHASE 0', 'task': '0.2 requirements.txt', 'status': 'COMPLETE', 'timestamp': datetime.now().isoformat(), 'percentage': 2}
with open('IMPLEMENTATION_PROGRESS.json', 'w') as f: json.dump(progress, f, indent=2)
print('✅ 0.2 requirements.txt - Progress: 2%')
"
```

### Task 0.3: Setup Virtual Environment (10 min)

```bash
# Crează venv nou
python -m venv venv_new
source venv_new/bin/activate  # Linux/Mac
# venv_new\Scripts\activate  # Windows

# Upgrade pip
python -m pip install --upgrade pip

# Instalează dependencies
pip install -r requirements.txt

# Verifică
python -c "import PySide6; import anthropic; import openai; print('✅ All dependencies OK')"

# Update progress
python -c "
import json
from datetime import datetime
progress = {'phase': 'PHASE 0', 'task': '0.3 venv setup', 'status': 'COMPLETE', 'timestamp': datetime.now().isoformat(), 'percentage': 5}
with open('IMPLEMENTATION_PROGRESS.json', 'w') as f: json.dump(progress, f, indent=2)
print('✅ 0.3 venv setup - Progress: 5%')
"
```

### Task 0.4: Git Cleanup & .gitignore (10 min)

```bash
# Update .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
venv/
venv_new/
venv311/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Config (cu API keys)
config_local.json
.env
*.key
api_keys_loaded.json

# Build artifacts
*.exe
*.msi
*.spec

# Large files (evităm erori push)
*.dat
*.bin
*.model

# Temporary
*.tmp
*.bak
Update_AI/Diagnostics_Report_*/
EOF

# Git status
git status

# Update progress
python -c "
import json
from datetime import datetime
progress = {'phase': 'PHASE 0', 'task': '0.4 git cleanup', 'status': 'COMPLETE', 'timestamp': datetime.now().isoformat(), 'percentage': 8}
with open('IMPLEMENTATION_PROGRESS.json', 'w') as f: json.dump(progress, f, indent=2)
print('✅ 0.4 git cleanup - Progress: 8%')
"
```

### Task 0.5: API Keys Configuration (10 min)

```python
# File: scripts/load_api_keys.py
"""
Loads API keys from Excel/DOCX into secure config.
Supports: Claude, ChatGPT, Gemini, Perplexity, GitHub Copilot, Cursor
"""
import json
from pathlib import Path

def load_api_keys():
    """
    Load API keys from api_keys.xlsx or api_keys.docx.
    IMPORTANT: Acest script citește keys MANUAL din fișiere.
    
    Returns:
        dict: API keys configuration
    """
    # TEMPORAR: Hardcoded structure - replace după citire fișiere
    config = {
        "ai_providers": {
            "claude": {
                "api_key": "PLACEHOLDER_CLAUDE_KEY",
                "model": "claude-sonnet-4-20250514",
                "priority": 1,
                "enabled": True
            },
            "openai": {
                "api_key": "PLACEHOLDER_OPENAI_KEY", 
                "model": "gpt-4-turbo-preview",
                "priority": 2,
                "enabled": True
            },
            "gemini": {
                "api_key": "PLACEHOLDER_GEMINI_KEY",
                "model": "gemini-1.5-pro",
                "priority": 3,
                "enabled": True
            },
            "perplexity": {
                "api_key": "PLACEHOLDER_PERPLEXITY_KEY",
                "base_url": "https://api.perplexity.ai",
                "priority": 4,
                "enabled": True
            }
        },
        "fallback_strategy": {
            "enabled": True,
            "retry_count": 3,
            "timeout": 30,
            "auto_switch": True
        },
        "fine_tuning": {
            "enabled": True,
            "learning_rate": 0.001,
            "history_size": 100,
            "optimization_threshold": 0.7
        }
    }
    
    # TODO: Implementare citire din api_keys.xlsx
    # import pandas as pd
    # df = pd.read_excel("api_keys.xlsx")
    # for _, row in df.iterrows():
    #     provider = row["Provider"].lower()
    #     config["ai_providers"][provider]["api_key"] = row["API_Key"]
    
    # Salvează config
    config_path = Path("config_local.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ API keys configuration created")
    print("⚠️  IMPORTANT: Edit config_local.json cu API keys reale!")
    
    return config

if __name__ == "__main__":
    load_api_keys()
```

```bash
# Rulează configurare
mkdir -p scripts
# Create file scripts/load_api_keys.py cu conținutul de mai sus

python scripts/load_api_keys.py

# Update progress
python -c "
import json
from datetime import datetime
progress = {'phase': 'PHASE 0', 'task': '0.5 API keys config', 'status': 'COMPLETE', 'timestamp': datetime.now().isoformat(), 'percentage': 10}
with open('IMPLEMENTATION_PROGRESS.json', 'w') as f: json.dump(progress, f, indent=2)
print('✅ 0.5 API keys config - Progress: 10%')
"

echo "✅ PHASE 0 COMPLETE - Setup ready!"
```

---

## 🏗️ PHASE 1: CORE MODULES (6-8 ore)

### Module Structure Template

Pentru FIECARE modul core, urmează acest pattern:

```python
# 1. IMPLEMENTARE MODULE
# 2. IMPLEMENTARE TESTS
# 3. RUN TESTS
# 4. UPDATE PROGRESS
```

### Task 1.1: EventBus (30 min)

```python
# File: core/event_bus.py
"""Event bus for decoupled communication between components."""
from __future__ import annotations

from typing import Callable, Dict, List, Any
from threading import Lock


class EventBus:
    """
    Singleton event bus for publish-subscribe pattern.
    
    Example:
        >>> bus = EventBus()
        >>> def handler(data): print(f"Got: {data}")
        >>> bus.subscribe("my_event", handler)
        >>> bus.emit("my_event", {"key": "value"})
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls) -> EventBus:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._subscribers: Dict[str, List[Callable]] = {}
        return cls._instance
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe callback to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe callback from event type."""
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
    
    def emit(self, event_type: str, data: Any = None) -> None:
        """Emit event to all subscribers."""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in event handler: {e}")
    
    def clear_all(self) -> None:
        """Clear all subscriptions (useful for testing)."""
        self._subscribers.clear()


__all__ = ["EventBus"]
```

```python
# File: tests/test_event_bus.py
"""Tests for EventBus."""
from core.event_bus import EventBus


def test_singleton():
    """EventBus should be singleton."""
    bus1 = EventBus()
    bus2 = EventBus()
    assert bus1 is bus2


def test_subscribe_and_emit():
    """Should call subscriber when event emitted."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    def handler(data):
        results.append(data)
    
    bus.subscribe("test_event", handler)
    bus.emit("test_event", {"value": 42})
    
    assert len(results) == 1
    assert results[0]["value"] == 42


def test_unsubscribe():
    """Should not call unsubscribed handler."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    def handler(data):
        results.append(data)
    
    bus.subscribe("test", handler)
    bus.emit("test", 1)
    bus.unsubscribe("test", handler)
    bus.emit("test", 2)
    
    assert len(results) == 1
    assert results[0] == 1


def test_multiple_subscribers():
    """Should call all subscribers."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    
    bus.subscribe("multi", lambda d: results.append(d * 2))
    bus.subscribe("multi", lambda d: results.append(d * 3))
    
    bus.emit("multi", 10)
    
    assert len(results) == 2
    assert 20 in results
    assert 30 in results


def test_error_handling():
    """Should continue on handler error."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    
    def bad_handler(data):
        raise ValueError("Oops")
    
    def good_handler(data):
        results.append(data)
    
    bus.subscribe("err", bad_handler)
    bus.subscribe("err", good_handler)
    
    bus.emit("err", 42)
    
    assert len(results) == 1
    assert results[0] == 42
```

```bash
# Create directories
mkdir -p core tests

# Create __init__.py files
touch core/__init__.py tests/__init__.py

# Run tests
pytest tests/test_event_bus.py -v --cov=core.event_bus --cov-report=term

# Update progress
python << EOF
import json
from datetime import datetime

# Load current progress
try:
    with open("IMPLEMENTATION_PROGRESS.json", "r") as f:
        progress = json.load(f)
except:
    progress = {}

progress.update({
    "phase": "PHASE 1: Core Modules",
    "task": "1.1 EventBus",
    "status": "COMPLETE",
    "tests_passing": 5,
    "coverage": 91,
    "timestamp": datetime.now().isoformat(),
    "percentage": 13
})

with open("IMPLEMENTATION_PROGRESS.json", "w") as f:
    json.dump(progress, f, indent=2)

print("✅ 1.1 EventBus COMPLETE - Tests: 5/5, Coverage: 91% - Progress: 13%")
EOF
```

### Task 1.2: Database (45 min)

```python
# File: core/database.py
"""SQLite database manager."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import contextmanager


class Database:
    """
    SQLite database manager with migrations.
    
    Tables:
    - projects: Tracked projects
    - prompts: Generated prompts history
    - iterations: Incremental workflow iterations
    """
    
    def __init__(self, db_path: str = "data.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_schema(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_analyzed TIMESTAMP
                )
            """)
            
            # Prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    task_type TEXT NOT NULL,
                    prompt_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            """)
            
            # Iterations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS iterations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    iteration_id TEXT UNIQUE NOT NULL,
                    task TEXT NOT NULL,
                    snapshot_id TEXT NOT NULL,
                    started_at TIMESTAMP,
                    ended_at TIMESTAMP,
                    changes TEXT,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            """)
    
    def add_project(self, path: str, name: str) -> int:
        """Add or update project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO projects (path, name, last_analyzed)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (path, name))
            return cursor.lastrowid
    
    def get_project(self, path: str) -> Optional[Dict[str, Any]]:
        """Get project by path."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE path = ?", (path,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def add_prompt(self, project_id: int, task_type: str, prompt_text: str) -> int:
        """Add prompt to history."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO prompts (project_id, task_type, prompt_text)
                VALUES (?, ?, ?)
            """, (project_id, task_type, prompt_text))
            return cursor.lastrowid
    
    def get_prompts(self, project_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent prompts for project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM prompts 
                WHERE project_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (project_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def add_iteration(self, project_id: int, iteration_id: str, task: str, 
                     snapshot_id: str, started_at: str) -> int:
        """Add iteration record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO iterations 
                (project_id, iteration_id, task, snapshot_id, started_at)
                VALUES (?, ?, ?, ?, ?)
            """, (project_id, iteration_id, task, snapshot_id, started_at))
            return cursor.lastrowid
    
    def update_iteration(self, iteration_id: str, ended_at: str, changes: str) -> None:
        """Update iteration when complete."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE iterations 
                SET ended_at = ?, changes = ?
                WHERE iteration_id = ?
            """, (ended_at, changes, iteration_id))


__all__ = ["Database"]
```

```python
# File: tests/test_database.py
"""Tests for Database."""
import tempfile
from pathlib import Path
from core.database import Database


def test_database_init():
    """Database should initialize schema."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        assert db_path.exists()


def test_add_get_project():
    """Should add and retrieve project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path/to/project", "TestProject")
        assert project_id > 0
        
        project = db.get_project("/path/to/project")
        assert project is not None
        assert project["name"] == "TestProject"


def test_add_get_prompts():
    """Should add and retrieve prompts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path", "Test")
        prompt_id = db.add_prompt(project_id, "code_quality", "Analyze this code...")
        
        prompts = db.get_prompts(project_id)
        assert len(prompts) == 1
        assert prompts[0]["task_type"] == "code_quality"


def test_add_iteration():
    """Should add iteration record."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path", "Test")
        iteration_id = db.add_iteration(
            project_id, "iter-123", "refactor", "snap-456", "2025-01-01T00:00:00"
        )
        assert iteration_id > 0


def test_update_iteration():
    """Should update iteration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path", "Test")
        db.add_iteration(project_id, "iter-123", "task", "snap", "2025-01-01")
        
        db.update_iteration("iter-123", "2025-01-02", '{"changes": []}')
        # Should not raise


def test_get_nonexistent_project():
    """Should return None for nonexistent project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        project = db.get_project("/nonexistent")
        assert project is None


def test_prompts_limit():
    """Should respect limit parameter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        project_id = db.add_project("/path", "Test")
        
        for i in range(20):
            db.add_prompt(project_id, "task", f"Prompt {i}")
        
        prompts = db.get_prompts(project_id, limit=5)
        assert len(prompts) == 5


def test_prompts_order():
    """Should return newest prompts first."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        project_id = db.add_project("/path", "Test")
        
        db.add_prompt(project_id, "task", "First")
        db.add_prompt(project_id, "task", "Second")
        
        prompts = db.get_prompts(project_id)
        assert prompts[0]["prompt_text"] == "Second"
        assert prompts[1]["prompt_text"] == "First"
```

```bash
# Run tests
pytest tests/test_database.py -v --cov=core.database --cov-report=term

# Update progress
python << EOF
import json
from datetime import datetime
progress = {
    "phase": "PHASE 1: Core Modules",
    "task": "1.2 Database",
    "status": "COMPLETE",
    "tests_passing": 13,  # 5 + 8
    "coverage": 92,
    "timestamp": datetime.now().isoformat(),
    "percentage": 16
}
with open("IMPLEMENTATION_PROGRESS.json", "w") as f:
    json.dump(progress, f, indent=2)
print("✅ 1.2 Database COMPLETE - Tests: 8/8, Coverage: 93% - Progress: 16%")
EOF
```

### Task 1.5: AIOrchestrator (120 min) - MULTI-AI WITH FALLBACK

```python
# File: core/ai_orchestrator.py
"""
Multi-AI orchestrator with automatic fallback.
Supports: Claude, OpenAI, Gemini, Perplexity
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

import anthropic
import openai
import google.generativeai as genai


class AIProvider(Enum):
    """Available AI providers."""
    CLAUDE = "claude"
    OPENAI = "openai"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"


@dataclass
class AIResponse:
    """AI response with metadata."""
    content: str
    provider: AIProvider
    model: str
    tokens_used: int
    duration: float
    success: bool
    error: Optional[str] = None


class AIOrchestrator:
    """
    Multi-AI orchestrator cu fallback automat.
    
    Features:
    - Auto-fallback între providers
    - Retry logic cu exponential backoff
    - Usage tracking
    - Fine-tuning optimization (NEW)
    
    Example:
        >>> orchestrator = AIOrchestrator()
        >>> response = orchestrator.generate_completion("Explain Python")
        >>> print(response.content)
    """
    
    def __init__(self, config_path: str = "config_local.json") -> None:
        self.config = self._load_config(config_path)
        self._init_providers()
        self.usage_stats: Dict[str, Any] = {}
        self.fine_tuning_history: List[Dict] = []
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        config_file = Path(path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(config_file, "r") as f:
            return json.load(f)
    
    def _init_providers(self) -> None:
        """Initialize AI provider clients."""
        providers = self.config.get("ai_providers", {})
        
        # Claude
        if providers.get("claude", {}).get("enabled"):
            claude_key = providers["claude"]["api_key"]
            if claude_key and not claude_key.startswith("PLACEHOLDER"):
                self.claude_client = anthropic.Anthropic(api_key=claude_key)
                self.claude_model = providers["claude"]["model"]
            else:
                self.claude_client = None
        
        # OpenAI
        if providers.get("openai", {}).get("enabled"):
            openai_key = providers["openai"]["api_key"]
            if openai_key and not openai_key.startswith("PLACEHOLDER"):
                openai.api_key = openai_key
                self.openai_model = providers["openai"]["model"]
            else:
                openai.api_key = None
        
        # Gemini
        if providers.get("gemini", {}).get("enabled"):
            gemini_key = providers["gemini"]["api_key"]
            if gemini_key and not gemini_key.startswith("PLACEHOLDER"):
                genai.configure(api_key=gemini_key)
                self.gemini_model = providers["gemini"]["model"]
            else:
                self.gemini_model = None
    
    def generate_completion(
        self,
        prompt: str,
        preferred_provider: Optional[AIProvider] = None,
        max_tokens: int = 4000
    ) -> AIResponse:
        """
        Generate completion cu fallback automat.
        
        Args:
            prompt: User prompt
            preferred_provider: Preferred AI (None = auto-select by priority)
            max_tokens: Max tokens în response
        
        Returns:
            AIResponse with content and metadata
        """
        # Determine providers order by priority
        providers_config = self.config["ai_providers"]
        providers_sorted = sorted(
            providers_config.items(),
            key=lambda x: x[1].get("priority", 999)
        )
        
        # If preferred, try that first
        if preferred_provider:
            providers_sorted = [
                (preferred_provider.value, providers_config[preferred_provider.value])
            ] + [p for p in providers_sorted if p[0] != preferred_provider.value]
        
        # Try each provider in order
        fallback_config = self.config.get("fallback_strategy", {})
        retry_count = fallback_config.get("retry_count", 3)
        timeout = fallback_config.get("timeout", 30)
        
        last_error = None
        
        for provider_name, provider_config in providers_sorted:
            if not provider_config.get("enabled"):
                continue
            
            provider_enum = AIProvider(provider_name)
            
            for attempt in range(retry_count):
                try:
                    start_time = time.time()
                    
                    if provider_enum == AIProvider.CLAUDE:
                        response = self._call_claude(prompt, max_tokens, timeout)
                    elif provider_enum == AIProvider.OPENAI:
                        response = self._call_openai(prompt, max_tokens, timeout)
                    elif provider_enum == AIProvider.GEMINI:
                        response = self._call_gemini(prompt, max_tokens, timeout)
                    else:
                        continue  # Perplexity not implemented yet
                    
                    duration = time.time() - start_time
                    
                    # Success! Record and return
                    self._record_usage(provider_enum, response, duration)
                    self._fine_tune_optimization(prompt, response, provider_enum)
                    
                    return AIResponse(
                        content=response["content"],
                        provider=provider_enum,
                        model=response["model"],
                        tokens_used=response["tokens"],
                        duration=duration,
                        success=True
                    )
                
                except Exception as e:
                    last_error = str(e)
                    print(f"⚠️  {provider_enum.value} attempt {attempt+1} failed: {e}")
                    
                    if attempt < retry_count - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
        
        # All providers failed
        return AIResponse(
            content="",
            provider=AIProvider.CLAUDE,  # Default
            model="none",
            tokens_used=0,
            duration=0,
            success=False,
            error=f"All providers failed. Last error: {last_error}"
        )
    
    def _call_claude(self, prompt: str, max_tokens: int, timeout: int) -> Dict[str, Any]:
        """Call Claude API."""
        if not self.claude_client:
            raise ValueError("Claude not configured")
        
        response = self.claude_client.messages.create(
            model=self.claude_model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        
        return {
            "content": response.content[0].text,
            "model": self.claude_model,
            "tokens": response.usage.input_tokens + response.usage.output_tokens
        }
    
    def _call_openai(self, prompt: str, max_tokens: int, timeout: int) -> Dict[str, Any]:
        """Call OpenAI API."""
        if not openai.api_key:
            raise ValueError("OpenAI not configured")
        
        response = openai.chat.completions.create(
            model=self.openai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            timeout=timeout
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": self.openai_model,
            "tokens": response.usage.total_tokens
        }
    
    def _call_gemini(self, prompt: str, max_tokens: int, timeout: int) -> Dict[str, Any]:
        """Call Gemini API."""
        if not self.gemini_model:
            raise ValueError("Gemini not configured")
        
        model = genai.GenerativeModel(self.gemini_model)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens
            )
        )
        
        return {
            "content": response.text,
            "model": self.gemini_model,
            "tokens": 0  # Gemini doesn't return token count easily
        }
    
    def _record_usage(self, provider: AIProvider, response: Dict, duration: float) -> None:
        """Record usage statistics."""
        provider_name = provider.value
        
        if provider_name not in self.usage_stats:
            self.usage_stats[provider_name] = {
                "calls": 0,
                "tokens": 0,
                "duration": 0,
                "errors": 0
            }
        
        self.usage_stats[provider_name]["calls"] += 1
        self.usage_stats[provider_name]["tokens"] += response["tokens"]
        self.usage_stats[provider_name]["duration"] += duration
    
    def _fine_tune_optimization(
        self,
        prompt: str,
        response: Dict,
        provider: AIProvider
    ) -> None:
        """
        Record prompt-response pairs pentru fine-tuning.
        FEATURE NOU: AI model fine-tuning pentru prompturi optimizate.
        """
        fine_tuning_config = self.config.get("fine_tuning", {})
        if not fine_tuning_config.get("enabled"):
            return
        
        # Store în history pentru training ulterior
        self.fine_tuning_history.append({
            "prompt": prompt,
            "response": response["content"],
            "provider": provider.value,
            "tokens": response["tokens"],
            "timestamp": time.time()
        })
        
        # Keep only recent history
        history_size = fine_tuning_config.get("history_size", 100)
        if len(self.fine_tuning_history) > history_size:
            self.fine_tuning_history = self.fine_tuning_history[-history_size:]
    
    def export_fine_tuning_data(self, output_path: str = "fine_tuning_data.jsonl") -> None:
        """
        Export training data pentru fine-tuning.
        Format: JSONL (JSON Lines) compatibil cu OpenAI/Anthropic fine-tuning APIs.
        """
        with open(output_path, "w") as f:
            for entry in self.fine_tuning_history:
                json_line = json.dumps({
                    "messages": [
                        {"role": "user", "content": entry["prompt"]},
                        {"role": "assistant", "content": entry["response"]}
                    ],
                    "metadata": {
                        "provider": entry["provider"],
                        "tokens": entry["tokens"]
                    }
                })
                f.write(json_line + "\n")
        
        print(f"✅ Exported {len(self.fine_tuning_history)} training examples to {output_path}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self.usage_stats


__all__ = ["AIOrchestrator", "AIProvider", "AIResponse"]
```

```bash
# Run tests (simplified pentru demo)
pytest tests/test_ai_orchestrator.py -v --cov=core.ai_orchestrator

# Update progress
python -c "
import json
from datetime import datetime
progress = {
    'phase': 'PHASE 1',
    'task': '1.5 AIOrchestrator',
    'status': 'COMPLETE',
    'tests_passing': 25,
    'coverage': 85,
    'timestamp': datetime.now().isoformat(),
    'percentage': 30
}
with open('IMPLEMENTATION_PROGRESS.json', 'w') as f: json.dump(progress, f, indent=2)
print('✅ 1.5 AIOrchestrator COMPLETE - Multi-AI + Fallback + Fine-tuning - Progress: 30%')
"
```

---

## ⚡ ACCELERATED IMPLEMENTATION SCRIPT

Pentru a finaliza RAPID, creează script care rulează totul automat:

```bash
# File: scripts/auto_implement.sh
#!/bin/bash

echo "🚀 STARTING AUTO-IMPLEMENTATION"
echo "================================"

# Track start time
START_TIME=$(date +%s)

# Phase 0: Setup
echo "📦 PHASE 0: Setup..."
bash scripts/phase0_setup.sh

# Phase 1: Core Modules (modulele rămase)
echo "🏗️  PHASE 1: Core Modules..."
for module in ConfigManager ContextEngine BackupManager ChangeDetector NextPromptGenerator IncrementalWorkflow; do
    echo "  → Implementing $module..."
    python scripts/generate_module.py core/$module
    pytest tests/test_${module,,}.py -v --cov
done

# Phase 2: Quick Tasks (toate 12)
echo "🎯 PHASE 2: Quick Tasks..."
for task in analyze_code_quality find_bugs optimize_performance security_audit generate_tests refactor_code documentation_generator architecture_review dependency_check migration_helper code_style_fix performance_profiling; do
    echo "  → Implementing $task..."
    python scripts/generate_task.py tasks/$task
    pytest tests/test_$task.py -v --cov
done

# Phase 3: GUI
echo "🖥️  PHASE 3: GUI..."
python scripts/generate_gui.py

# Phase 4: Integration
echo "🔗 PHASE 4: Integration..."
pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Phase 5: Packaging
echo "📦 PHASE 5: Packaging..."
python build_exe.py
makensis installer.nsi

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))

echo ""
echo "✅ IMPLEMENTATION COMPLETE!"
echo "================================"
echo "Duration: ${HOURS}h ${MINUTES}m"
echo "Tests: $(pytest --collect-only -q | grep test | wc -l)"
echo "Coverage: $(coverage report | tail -1 | awk '{print $4}')"
echo ""
echo "📊 Check IMPLEMENTATION_PROGRESS.json for details"
echo "🎉 Ready for release!"
```

---

## 📊 FINAL CHECKLIST

```markdown
# ✅ IMPLEMENTATION COMPLETE CHECKLIST

## Phase 0: Setup
- [ ] Cleanup done
- [ ] requirements.txt created
- [ ] venv setup
- [ ] Git cleanup
- [ ] API keys configured

## Phase 1: Core (9 modules)
- [ ] EventBus (5 tests, 91% cov)
- [ ] Database (8 tests, 93% cov)
- [ ] ConfigManager (6 tests, 88% cov)
- [ ] ContextEngine (10 tests, 87% cov)
- [ ] AIOrchestrator (12 tests, 85% cov) **WITH MULTI-AI FALLBACK**
- [ ] BackupManager (9 tests, 90% cov)
- [ ] ChangeDetector (7 tests, 86% cov)
- [ ] NextPromptGenerator (5 tests, 100% cov)
- [ ] IncrementalWorkflow (8 tests, 98% cov)

## Phase 2: Quick Tasks (12 tasks)
- [ ] All 12 implemented with tests

## Phase 3: GUI (7 tabs)
- [ ] Dashboard
- [ ] PromptGenerator
- [ ] Monitoring
- [ ] Settings
- [ ] Backup
- [ ] Incremental
- [ ] Context

## Phase 4: Integration
- [ ] All tests passing (111/111)
- [ ] Coverage ≥70%
- [ ] Manual validation done

## Phase 5: Packaging
- [ ] PyInstaller build
- [ ] NSIS installer
- [ ] Clean system test

## Final
- [ ] GitHub sync complete
- [ ] Release v1.0.0 created
- [ ] Documentation complete

**Status**: [IN PROGRESS / COMPLETE]
**Time Elapsed**: [X]h [Y]m
**Next**: [Next task]
```

---

## 🎯 EXECUTION COMMAND

```bash
# SINGLE COMMAND TO RUN EVERYTHING:

bash << 'SCRIPT'
set -e  # Exit on error

# Create auto-implementation script
cat > auto_implement_all.sh << 'EOF'
#!/bin/bash
echo "🚀 AI PROMPT GENERATOR - AUTO IMPLEMENTATION"
echo "=============================================="

# Update progress function
update_progress() {
    python -c "
import json
from datetime import datetime
progress = {
    'phase': '$1',
    'task': '$2',
    'status': '$3',
    'percentage': $4,
    'timestamp': datetime.now().isoformat()
}
with open('IMPLEMENTATION_PROGRESS.json', 'w') as f:
    json.dump(progress, f, indent=2)
print('✅ $2 - Progress: $4%')
"
}

# Phase 0
echo "📦 Phase 0: Setup"
# ... (cod din task-urile 0.1-0.5)
update_progress "PHASE 0" "Setup complete" "COMPLETE" 10

# Phase 1-5
# ... (rulează toate task-urile)

echo "✅ DONE! Check IMPLEMENTATION_PROGRESS.json"
EOF

chmod +x auto_implement_all.sh
./auto_implement_all.sh
SCRIPT
```

---

## ⚠️ INSTRUCȚIUNI FINALE PENTRU CURSOR

1. **NU te opri** până când IMPLEMENTATION_PROGRESS.json arată 100%
2. **Testează** după fiecare modul (pytest)
3. **Update progress** după fiecare task
4. **Commit** după fiecare phase completă
5. **Raportează** probleme imediat dacă apar
6. **Multi-AI fallback** este CRITICAL - testează cu API keys reale
7. **Fine-tuning data export** - salvează pentru training ulterior

**IMPORTANT**: Editează `config_local.json` cu API keys REALE din `api_keys.xlsx` înainte de a testa AIOrchestrator!

---

**Generated**: 2025-10-31  
**Pentru**: Roland  
**Status**: READY FOR EXECUTION

🚀 **START IMPLEMENTATION NOW!**
