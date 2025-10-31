# Technical Specifications

## Tech Stack

### Language & Runtime
- **Python**: 3.10+ (tested on 3.13.7)
- **Type System**: Type hints cu `typing` module
- **Compatibility**: Windows 10/11

### GUI Framework
- **PySide6**: 6.10.0 (Qt for Python)
- **PySide6_Addons**: 6.10.0
- **PySide6_Essentials**: 6.10.0
- **Qt Version**: 6.x

### Database
- **SQLite**: Built-in Python sqlite3
- **Database Path**: `data.db` (configurable)
- **Schema**: 3 tables (projects, prompts, iterations)
- **Migrations**: Manual (schema in code)

### AI Providers
- **Anthropic Claude**: `anthropic==0.39.0`
  - Model: `claude-sonnet-4-20250514`
  - Priority: 1 (highest)
- **OpenAI**: `openai==1.109.1`
  - Model: `gpt-4-turbo-preview`
  - Priority: 2
- **Google Gemini**: `google-generativeai==0.8.5`
  - Model: `gemini-1.5-pro`
  - Priority: 3
- **Perplexity**: `perplexity==0.0.1`
  - Priority: 4 (optional)

### Testing
- **pytest**: 8.3.3
- **pytest-cov**: 4.1.0 (coverage reporting)
- **pytest-qt**: 4.0.0 (Qt testing)

### Build & Packaging
- **PyInstaller**: 6.15.0
- **NSIS**: 3.x (for installer)
- **Target**: Windows executable (.exe)

### Utilities
- **watchdog**: 4.0.2 (file monitoring)
- **python-dotenv**: 1.0.1 (environment variables)
- **pyyaml**: 6.0.2 (YAML parsing)
- **toml**: 0.10.2 (TOML parsing)
- **colorama**: 0.4.6 (Windows terminal colors)

### Dependencies Summary
- **Total dependencies**: ~268 packages (including transitive)
- **Critical dependencies**: PySide6, anthropic, openai, google-generativeai, watchdog, pytest
- **Development dependencies**: pytest-cov, pytest-qt, coverage

## Architecture Components

### Core Modules

#### 1. `core/ai_orchestrator.py`
**Purpose**: Multi-AI orchestration cu fallback automat și fine-tuning optimization

**Key Functions**:
- `__init__(config_path: str = "config_local.json") -> None`
- `generate_completion(prompt: str, max_tokens: int = 4000) -> AIResponse`
- `_call_claude(prompt: str, max_tokens: int) -> AIResponse`
- `_call_openai(prompt: str, max_tokens: int) -> AIResponse`
- `_call_gemini(prompt: str, max_tokens: int) -> AIResponse`
- `_record_usage(provider: AIProvider, tokens: int, duration: float) -> None`
- `_fine_tune_optimization(prompt: str, response: AIResponse) -> None`
- `export_fine_tuning_data() -> Dict[str, Any]`
- `get_usage_stats() -> Dict[str, Any]`

**Dependencies**: 
- `anthropic` (optional)
- `openai` (optional)
- `google.generativeai` (optional)
- `json`, `time`, `pathlib`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 77% (115/150 statements)  
**Tests**: `test_ai_orchestrator.py` - 12/12 passing

#### 2. `core/database.py`
**Purpose**: SQLite database manager cu schema management și migrations

**Key Functions**:
- `__init__(db_path: str = "data.db") -> None`
- `_get_connection() -> contextmanager` (context manager)
- `_init_schema() -> None`
- `add_project(path: str, name: str) -> int`
- `get_project(path: str) -> Optional[Dict[str, Any]]`
- `add_prompt(project_id: int, task_type: str, prompt_text: str) -> int`
- `get_prompts(project_id: int) -> List[Dict[str, Any]]`
- `add_iteration(project_id: int, iteration_id: str, task: str, snapshot_id: str) -> int`
- `update_iteration(iteration_id: str, changes: str, ended_at: str) -> None`

**Dependencies**: 
- `sqlite3` (built-in)
- `datetime`, `pathlib`, `contextlib`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 95% (57/60 statements)  
**Tests**: `test_database.py` - 8/8 passing

**Database Schema**:
```sql
-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_analyzed TIMESTAMP
);

-- Prompts table
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    task_type TEXT NOT NULL,
    prompt_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Iterations table
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
);
```

#### 3. `core/event_bus.py`
**Purpose**: Singleton event bus pentru decoupled communication (pub/sub pattern)

**Key Functions**:
- `__new__(cls) -> EventBus` (singleton)
- `subscribe(event_type: str, callback: Callable) -> None`
- `unsubscribe(event_type: str, callback: Callable) -> None`
- `emit(event_type: str, data: Any = None) -> None`
- `clear_all() -> None`

**Dependencies**: 
- `typing` (Callable, Dict, List, Any)
- `threading` (Lock)

**Status**: ✅ IMPLEMENTED  
**Coverage**: 100% (32/32 statements)  
**Tests**: `test_event_bus.py` - 5/5 passing

#### 4. `core/config_manager.py`
**Purpose**: Configuration management cu JSON persistence

**Key Functions**:
- `__init__(config_path: str = "config_local.json") -> None`
- `_load_config(path: str) -> Dict[str, Any]`
- `_default_config() -> Dict[str, Any]`
- `_save_config() -> None`
- `get(key: str, default: Any = None) -> Any`
- `set(key: str, value: Any) -> None`
- `get_all() -> Dict[str, Any]`
- `update(updates: Dict[str, Any]) -> None`

**Dependencies**: 
- `json`, `pathlib`, `typing`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 93% (40/43 statements)  
**Tests**: `test_config_manager.py` - 6/6 passing

**Config Structure** (`config_local.json`):
```json
{
  "ai_providers": {
    "claude": {
      "api_key": "...",
      "model": "claude-sonnet-4-20250514",
      "priority": 1,
      "enabled": true
    },
    "openai": {
      "api_key": "...",
      "model": "gpt-4-turbo-preview",
      "priority": 2,
      "enabled": true
    },
    "gemini": {
      "api_key": "...",
      "model": "gemini-1.5-pro",
      "priority": 3,
      "enabled": true
    },
    "perplexity": {
      "api_key": "...",
      "base_url": "https://api.perplexity.ai",
      "priority": 4,
      "enabled": true
    }
  },
  "fallback_strategy": {
    "enabled": true,
    "retry_count": 3,
    "timeout": 30,
    "auto_switch": true
  },
  "fine_tuning": {
    "enabled": true,
    "learning_rate": 0.001,
    "history_size": 100,
    "optimization_threshold": 0.7
  }
}
```

#### 5. `core/context_engine.py`
**Purpose**: Analiză structură proiect și generare context pentru AI

**Key Functions**:
- `__init__(project_path: str) -> None`
- `analyze_project_structure() -> Dict[str, Any]`
- `get_code_summary(file_path: str, max_lines: int = 50) -> Dict[str, Any]`
- `generate_context_prompt(task_type: str = "general") -> str`
- `get_recent_changes(days: int = 7) -> List[Dict[str, Any]]`

**Dependencies**: 
- `os`, `pathlib`, `json`, `typing`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 93% (68/73 statements)  
**Tests**: `test_context_engine.py` - 10/10 passing

#### 6. `core/backup_manager.py`
**Purpose**: Snapshot management și restore pentru proiecte

**Key Functions**:
- `__init__(backup_dir: str = "backups") -> None`
- `create_snapshot(project_path: str, name: Optional[str] = None) -> str`
- `list_snapshots(project_path: str) -> List[Dict[str, Any]]`
- `get_snapshot(snapshot_id: str) -> Optional[Dict[str, Any]]`
- `restore_snapshot(snapshot_id: str, target_path: str) -> bool`
- `delete_snapshot(snapshot_id: str) -> bool`
- `cleanup_old_snapshots(project_path: str, keep_count: int = 10) -> int`

**Dependencies**: 
- `shutil`, `zipfile`, `pathlib`, `datetime`, `json`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 97% (83/86 statements)  
**Tests**: `test_backup_manager.py` - 9/9 passing

**Snapshot Structure**:
```
backups/
  {project_name}/
    {snapshot_id}.zip
    {snapshot_id}.json (metadata)
```

#### 7. `core/change_detector.py`
**Purpose**: Detecție modificări fișiere cu hash tracking

**Key Functions**:
- `__init__(state_file: str = ".change_state.json") -> None`
- `_load_state() -> None`
- `_save_state() -> None`
- `_calculate_hash(file_path: Path) -> str`
- `detect_changes(project_path: str) -> List[Dict[str, Any]]`
- `get_modified_files() -> List[str]`
- `has_changes() -> bool`
- `reset_state() -> None`

**Dependencies**: 
- `hashlib`, `json`, `pathlib`, `typing`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 94% (63/67 statements)  
**Tests**: `test_change_detector.py` - 7/7 passing

#### 8. `core/next_prompt_generator.py`
**Purpose**: Generare prompturi pentru diferite task-uri

**Key Functions**:
- `__init__() -> None`
- `_load_templates() -> None`
- `generate_suggestions(project_path: str, task_type: TaskType) -> List[PromptSuggestion]`
- `_get_description(task_type: TaskType) -> str`
- `generate_custom_prompt(task_type: TaskType, context: str) -> str`

**Dependencies**: 
- `enum` (TaskType enum)
- `dataclasses` (PromptSuggestion)
- `pathlib`, `typing`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 100% (47/47 statements)  
**Tests**: `test_next_prompt_generator.py` - 5/5 passing

#### 9. `core/incremental_workflow.py`
**Purpose**: Workflow incremental pentru îmbunătățiri pas cu pas

**Key Functions**:
- `__init__(project_path: str, workflow_file: str = ".workflow.json") -> None`
- `_load_workflow() -> None`
- `_save_workflow() -> None`
- `create_iteration(task: str, snapshot_id: Optional[str] = None) -> str`
- `complete_iteration(iteration_id: str, changes: Dict[str, Any], result: Optional[str] = None) -> bool`
- `fail_iteration(iteration_id: str, error: str) -> bool`
- `get_iteration(iteration_id: str) -> Optional[Iteration]`
- `list_iterations(status: Optional[str] = None) -> List[Iteration]`
- `get_current_iteration() -> Optional[Iteration]`
- `get_progress() -> Dict[str, Any]`

**Dependencies**: 
- `json`, `uuid`, `datetime`, `pathlib`, `dataclasses`

**Status**: ✅ IMPLEMENTED  
**Coverage**: 93% (82/88 statements)  
**Tests**: `test_incremental_workflow.py` - 8/8 passing

### GUI Modules

#### `gui/main_window.py`
**Purpose**: Main application window cu tabbed interface

**Key Components**:
- QMainWindow cu QTabWidget
- 7 tabs: Dashboard, Prompt Generator, Monitoring, Context, Backup, Incremental, Settings

**Status**: ✅ IMPLEMENTED  
**Module**: `gui/main_window.py`

#### `gui/tabs/dashboard_tab.py`
**Purpose**: Dashboard cu overview și statistici

**Widgets**:
- QLabel pentru title
- QLabel pentru statistici (Projects, Prompts, AI Calls)
- QTextEdit pentru recent activity
- QPushButton pentru refresh

**Status**: ✅ IMPLEMENTED  
**Tests**: `test_dashboard_tab.py` - Basic tests

#### `gui/tabs/prompt_generator_tab.py`
**Purpose**: Generare prompturi AI cu selecție proiect și task type

**Widgets**:
- QLineEdit pentru project path
- QPushButton pentru browse
- QComboBox pentru task type selection
- QTextEdit pentru context display
- QPushButton pentru generate prompt
- QTextEdit pentru generated prompt
- QPushButton pentru send to AI
- QTextEdit pentru AI response

**Status**: ✅ IMPLEMENTED

#### `gui/tabs/monitoring_tab.py`
**Purpose**: File monitoring cu watchdog integration

**Widgets**:
- QCheckBox pentru enable monitoring
- QLineEdit pentru project path
- QTextEdit pentru change log
- QPushButton pentru refresh

**Status**: ✅ IMPLEMENTED  
**Tests**: `test_monitoring_tab.py` - Basic tests

#### `gui/tabs/context_tab.py`
**Purpose**: Project context analysis și display

**Status**: ✅ IMPLEMENTED

#### `gui/tabs/backup_tab.py`
**Purpose**: Snapshot management și restore

**Status**: ✅ IMPLEMENTED

#### `gui/tabs/incremental_tab.py`
**Purpose**: Incremental workflow management

**Status**: ✅ IMPLEMENTED

#### `gui/tabs/settings_tab.py`
**Purpose**: Configuration management pentru API keys și settings

**Widgets**:
- QTabWidget pentru categorii settings
- QLineEdit pentru API keys
- QCheckBox pentru enable/disable providers
- QSpinBox pentru retry count, timeout
- QPushButton pentru save

**Status**: ✅ IMPLEMENTED  
**Tests**: `test_settings_tab.py` - Basic tests

### Tasks Modules (12 Quick Tasks)

Toate task-urile au aceeași structură de bază:
- `__init__(orchestrator: Optional[AIOrchestrator] = None) -> None`
- `analyze/generate/find/... (project_path: str, ...) -> AIResponse`
- `get_<result_type>(project_path: str) -> Dict[str, Any]`

#### 1. `tasks/analyze_code_quality.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_analyze_code_quality.py` - 3/3 passing

#### 2. `tasks/find_bugs.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_find_bugs.py` - 2/2 passing

#### 3. `tasks/optimize_performance.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_optimize_performance.py` - 2/2 passing

#### 4. `tasks/security_audit.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_security_audit.py` - 2/2 passing

#### 5. `tasks/generate_tests.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_generate_tests.py` - 2/2 passing

#### 6. `tasks/refactor_code.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_refactor_code.py` - 2/2 passing

#### 7. `tasks/documentation_generator.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_documentation_generator.py` - 2/2 passing

#### 8. `tasks/architecture_review.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_architecture_review.py` - 2/2 passing

#### 9. `tasks/dependency_check.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_dependency_check.py` - 3/3 passing

#### 10. `tasks/migration_helper.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_migration_helper.py` - 3/3 passing

#### 11. `tasks/code_style_fix.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_code_style_fix.py` - 2/2 passing

#### 12. `tasks/performance_profiling.py`
**Status**: ✅ IMPLEMENTED  
**Coverage**: 100%  
**Tests**: `test_performance_profiling.py` - 2/2 passing

## API Interfaces

### Multi-AI Orchestration (`core/ai_orchestrator.py`)

**Providers Supported**:
1. Claude (Anthropic) - Priority 1
2. OpenAI - Priority 2
3. Google Gemini - Priority 3
4. Perplexity - Priority 4 (optional)

**Fallback Mechanism**:
- Automatic fallback când un provider eșuează
- Retry cu exponential backoff
- Priority-based provider selection
- Configurable retry count și timeout

**Retry Logic**:
- Maximum retry count: 3 (configurable)
- Exponential backoff: 1s, 2s, 4s
- Timeout: 30 seconds (configurable)
- Auto-switch între providers dacă enabled

**Error Handling**:
- Graceful degradation
- Error messages clare
- Usage tracking pentru debugging

### Context Analysis (`core/context_engine.py`)

**Supported File Types**:
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- Go (.go)
- And other text-based files

**Parsing Strategies**:
- File structure analysis (tree walk)
- Code summary (first N lines)
- File type detection (extension-based)
- Ignore patterns: `.git`, `venv`, `__pycache__`, `build`, `dist`, etc.

**Output Format**:
- Dictionary cu structure information
- Markdown format pentru context prompts
- Cached pentru performanță

### File Monitoring (`core/change_detector.py`)

**Watch Patterns**:
- All files în project path (configurable)
- Exclude patterns: `.git`, `venv`, `__pycache__`, etc.
- Recursive directory watching

**Event Handling**:
- File creation
- File modification
- File deletion
- Directory changes

**Debouncing**:
- State persistence între sesiuni
- Hash-based change detection
- Reset functionality

### Backup System (`core/backup_manager.py`)

**Snapshot Mechanism**:
- Zip-based snapshots
- Metadata în JSON
- Timestamp și size tracking
- Automatic naming sau custom name

**Restore Logic**:
- Unzip snapshot la target path
- Validation înainte de restore
- Error handling pentru corrupted snapshots

**Storage Structure**:
```
backups/
  {project_name}/
    {snapshot_id}.zip
    {snapshot_id}.json
```

**Metadata Format**:
```json
{
  "snapshot_id": "...",
  "project_path": "...",
  "created_at": "ISO timestamp",
  "size": 123456,
  "file_count": 42
}
```

---

**Generated**: 2025-10-31  
**Source**: Code analysis, coverage.json, MASTER_DNA files

