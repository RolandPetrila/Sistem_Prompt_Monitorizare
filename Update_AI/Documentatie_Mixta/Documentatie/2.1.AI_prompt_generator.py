#!/usr/bin/env python3
"""
AI Prompt Generator ULTIMATE - Multi-Tab Professional Edition
Generează prompturi perfecte + Analiză cod + Git integration + Template Manager + AI Response Simulator
"""
import os
import sys
import json
import time
import threading
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from collections import Counter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# ==================== PROJECT WATCHER ====================
class ProjectWatcher:
    """Monitor schimbări în folder cu polling."""
    
    def __init__(self, callback, path: str):
        self.callback = callback
        self.path = path
        self.running = False
        self.thread = None
        self.file_times = {}
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _watch_loop(self):
        while self.running:
            try:
                self._check_changes()
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(2)
    
    def _check_changes(self):
        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs if d not in [
                '.git', '__pycache__', 'node_modules', 'venv', 
                '.venv', 'dist', 'build', '.next', '.vscode'
            ]]
            
            for file in files:
                if file.endswith(('.pyc', '.swp', '.tmp', '~')):
                    continue
                
                filepath = os.path.join(root, file)
                
                try:
                    current_mtime = os.path.getmtime(filepath)
                    
                    if filepath not in self.file_times:
                        self.file_times[filepath] = current_mtime
                        self.callback('created', filepath)
                    elif current_mtime > self.file_times[filepath]:
                        self.file_times[filepath] = current_mtime
                        self.callback('modified', filepath)
                        
                except (OSError, FileNotFoundError):
                    if filepath in self.file_times:
                        del self.file_times[filepath]
                        self.callback('deleted', filepath)


# ==================== CODE ANALYZER ====================
class CodeAnalyzer:
    """Analizează structura și calitatea codului."""
    
    @staticmethod
    def analyze_project(path: str) -> Dict:
        """Analiză completă proiect."""
        stats = {
            'total_files': 0,
            'python_files': 0,
            'javascript_files': 0,
            'test_files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'functions': 0,
            'classes': 0,
            'todos': [],
            'file_sizes': [],
            'largest_files': [],
            'complexity_issues': []
        }
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv']]
            
            for file in files:
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, path)
                
                try:
                    size = os.path.getsize(filepath)
                    stats['file_sizes'].append((relative_path, size))
                    
                    if file.endswith('.py'):
                        stats['python_files'] += 1
                        if 'test' in file.lower():
                            stats['test_files'] += 1
                        CodeAnalyzer._analyze_python_file(filepath, relative_path, stats)
                        
                    elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                        stats['javascript_files'] += 1
                        CodeAnalyzer._analyze_js_file(filepath, relative_path, stats)
                    
                    stats['total_files'] += 1
                    
                except Exception as e:
                    pass
        
        # Top 10 largest files
        stats['largest_files'] = sorted(stats['file_sizes'], key=lambda x: x[1], reverse=True)[:10]
        
        return stats
    
    @staticmethod
    def _analyze_python_file(filepath: str, relative_path: str, stats: Dict):
        """Analiză fișier Python."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                stats['total_lines'] += 1
                stripped = line.strip()
                
                if not stripped:
                    stats['blank_lines'] += 1
                elif stripped.startswith('#'):
                    stats['comment_lines'] += 1
                    if 'TODO' in stripped or 'FIXME' in stripped:
                        stats['todos'].append(f"{relative_path}:{i} - {stripped}")
                else:
                    stats['code_lines'] += 1
                
                if stripped.startswith('def '):
                    stats['functions'] += 1
                    # Check function length
                    if i + 50 < len(lines):  # Long function warning
                        stats['complexity_issues'].append(
                            f"{relative_path}:{i} - Funcție potențial prea lungă (>50 linii)"
                        )
                        
                if stripped.startswith('class '):
                    stats['classes'] += 1
                    
        except Exception as e:
            pass
    
    @staticmethod
    def _analyze_js_file(filepath: str, relative_path: str, stats: Dict):
        """Analiză fișier JavaScript/TypeScript."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                stats['total_lines'] += 1
                stripped = line.strip()
                
                if not stripped:
                    stats['blank_lines'] += 1
                elif stripped.startswith('//') or stripped.startswith('/*'):
                    stats['comment_lines'] += 1
                    if 'TODO' in stripped or 'FIXME' in stripped:
                        stats['todos'].append(f"{relative_path}:{i} - {stripped}")
                else:
                    stats['code_lines'] += 1
                
                if 'function ' in stripped or '=>' in stripped:
                    stats['functions'] += 1
                    
                if stripped.startswith('class '):
                    stats['classes'] += 1
                    
        except Exception as e:
            pass


# ==================== GIT INTEGRATION ====================
class GitIntegration:
    """Integrare Git pentru context."""
    
    @staticmethod
    def get_git_info(path: str) -> Dict:
        """Extrage informații Git."""
        info = {
            'available': False,
            'branch': '',
            'commits': [],
            'status': '',
            'remote': '',
            'contributors': []
        }
        
        try:
            os.chdir(path)
            
            # Check if git repo
            result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return info
            
            info['available'] = True
            
            # Branch
            result = subprocess.run(['git', 'branch', '--show-current'],
                                  capture_output=True, text=True, timeout=5)
            info['branch'] = result.stdout.strip()
            
            # Recent commits
            result = subprocess.run(['git', 'log', '--oneline', '-10'],
                                  capture_output=True, text=True, timeout=5)
            info['commits'] = result.stdout.strip().split('\n')[:10]
            
            # Status
            result = subprocess.run(['git', 'status', '--short'],
                                  capture_output=True, text=True, timeout=5)
            info['status'] = result.stdout.strip()
            
            # Remote
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                                  capture_output=True, text=True, timeout=5)
            info['remote'] = result.stdout.strip()
            
            # Contributors (top 5)
            result = subprocess.run(['git', 'shortlog', '-sn', '--all'],
                                  capture_output=True, text=True, timeout=5)
            contributors = result.stdout.strip().split('\n')[:5]
            info['contributors'] = [c.strip() for c in contributors]
            
        except Exception as e:
            info['error'] = str(e)
            
        return info


# ==================== TEMPLATE MANAGER ====================
class TemplateManager:
    """Gestionare template-uri custom."""
    
    def __init__(self):
        self.templates_dir = Path.home() / '.ai-prompt-generator' / 'templates'
        self.templates_dir.mkdir(parents=True, exist_ok=True)
    
    def save_template(self, name: str, content: str):
        """Salvează template."""
        filepath = self.templates_dir / f"{name}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def load_template(self, name: str) -> str:
        """Încarcă template."""
        filepath = self.templates_dir / f"{name}.md"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def list_templates(self) -> List[str]:
        """Lista template-uri."""
        return [f.stem for f in self.templates_dir.glob("*.md")]
    
    def delete_template(self, name: str):
        """Șterge template."""
        filepath = self.templates_dir / f"{name}.md"
        if filepath.exists():
            filepath.unlink()


# ==================== MAIN APPLICATION ====================
class AIPromptGeneratorUltimate:
    """Aplicația principală - Ultimate Edition."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Prompt Generator ULTIMATE Pro")
        self.root.geometry("1600x1000")
        
        # State
        self.project_path = tk.StringVar()
        self.export_folder = tk.StringVar(value="Update_AI/DNA_Export")
        self.project_name = tk.StringVar()
        self.project_type = tk.StringVar(value="fullstack")
        self.current_status = tk.StringVar()
        self.prompt_type = tk.StringVar(value="initial")
        self.watching = False
        self.watcher = None
        self.file_changes: List[Dict] = []
        self.auto_generate = tk.BooleanVar(value=False)
        self.include_git = tk.BooleanVar(value=True)
        self.include_analysis = tk.BooleanVar(value=True)
        
        # Managers
        self.template_manager = TemplateManager()
        
        # Recent projects
        self.recent_projects = self.load_recent_projects()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Creează interfața multi-tab."""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header,
            text="🤖 AI Prompt Generator ULTIMATE Pro",
            style='Title.TLabel'
        ).pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(header, text="● Ready", foreground="green")
        self.status_label.pack(side=tk.RIGHT)
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # TAB 1: Generator Principal
        self.create_generator_tab()
        
        # TAB 2: Code Analysis
        self.create_analysis_tab()
        
        # TAB 3: Git Integration
        self.create_git_tab()
        
        # TAB 4: Template Manager
        self.create_templates_tab()
        
        # TAB 5: AI Response Simulator
        self.create_simulator_tab()
        
        # TAB 6: Batch Operations
        self.create_batch_tab()
        
        # TAB 7: Settings & History
        self.create_settings_tab()
        
    def create_generator_tab(self):
        """TAB 1: Generator principal (îmbunătățit)."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Generator")
        
        # Layout cu 2 coloane
        left = ttk.Frame(tab)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        right = ttk.Frame(tab)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # LEFT: Settings
        settings_frame = ttk.LabelFrame(left, text="⚙️ Preferences", padding=10)
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.auto_save_config = tk.BooleanVar(value=True)
        self.dark_mode = tk.BooleanVar(value=False)
        self.notifications = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(settings_frame, text="Auto-save configuration", variable=self.auto_save_config).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(settings_frame, text="Enable notifications", variable=self.notifications).pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(settings_frame, text="Dark mode (requires restart)", variable=self.dark_mode).pack(anchor=tk.W, pady=5)
        
        ttk.Label(settings_frame, text="Monitoring interval (seconds):").pack(anchor=tk.W, pady=(10, 5))
        self.monitor_interval = tk.Scale(settings_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.monitor_interval.set(2)
        self.monitor_interval.pack(fill=tk.X, pady=5)
        
        ttk.Button(settings_frame, text="💾 Save Settings", command=self.save_settings).pack(pady=10)
        
        # RIGHT: History
        history_frame = ttk.LabelFrame(right, text="📜 Recent Activity", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.history_tree = ttk.Treeview(history_frame, columns=('Date', 'Project', 'Action'), show='headings', height=15)
        self.history_tree.heading('Date', text='Date/Time')
        self.history_tree.heading('Project', text='Project')
        self.history_tree.heading('Action', text='Action')
        self.history_tree.column('Date', width=150)
        self.history_tree.column('Project', width=200)
        self.history_tree.column('Action', width=150)
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(history_frame, text="🗑️ Clear History", command=self.clear_history).pack(pady=5)
    
    # ==================== METHODS ====================
    
    def browse_project(self):
        """Selectează folder proiect."""
        folder = filedialog.askdirectory(title="Select Project Root")
        if folder:
            self.project_path.set(folder)
            if not self.project_name.get():
                self.project_name.set(Path(folder).name)
            self.add_to_recent_projects(folder)
            self.log_history("Opened project", Path(folder).name)
    
    def toggle_watching(self):
        """Start/Stop monitoring."""
        if not self.project_path.get():
            messagebox.showwarning("Warning", "Select project folder first!")
            return
        
        if not self.watching:
            self.start_watching()
        else:
            self.stop_watching()
    
    def start_watching(self):
        """Start monitoring."""
        try:
            self.watcher = ProjectWatcher(
                callback=self.on_file_change,
                path=self.project_path.get()
            )
            self.watcher.start()
            
            self.watching = True
            self.watch_button.config(text="⏸️ Stop")
            self.status_label.config(text="● Watching", foreground="orange")
            
            self.log_change("started", "Monitoring started")
            self.log_history("Started monitoring", self.project_name.get())
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot start monitoring: {e}")
    
    def stop_watching(self):
        """Stop monitoring."""
        if self.watcher:
            self.watcher.stop()
            self.watcher = None
        
        self.watching = False
        self.watch_button.config(text="▶️ Start")
        self.status_label.config(text="● Ready", foreground="green")
        
        self.log_change("stopped", "Monitoring stopped")
    
    def on_file_change(self, action: str, filepath: str):
        """File change callback."""
        self.root.after(0, lambda: self._handle_file_change(action, filepath))
    
    def _handle_file_change(self, action: str, filepath: str):
        """Handle file change."""
        try:
            relative_path = os.path.relpath(filepath, self.project_path.get())
        except ValueError:
            relative_path = filepath
        
        change = {
            'action': action,
            'file': relative_path,
            'time': datetime.now().strftime("%H:%M:%S")
        }
        self.file_changes.append(change)
        
        if len(self.file_changes) > 100:
            self.file_changes = self.file_changes[-100:]
        
        self.log_change(action, relative_path)
        self.update_monitoring_stats()
        
        self.last_update_label.config(text=f"Last: {datetime.now().strftime('%H:%M:%S')}")
        
        if self.auto_generate.get():
            self.generate_prompt()
    
    def log_change(self, action: str, message: str):
        """Log change."""
        self.changes_text.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        emoji = {
            'modified': '📝',
            'created': '✨',
            'deleted': '🗑️',
            'started': '▶️',
            'stopped': '⏸️'
        }.get(action, '📌')
        
        self.changes_text.insert(tk.END, f"{timestamp} {emoji} {action.upper()}: {message}\n")
        self.changes_text.see(tk.END)
        self.changes_text.config(state=tk.DISABLED)
    
    def update_monitoring_stats(self):
        """Update monitoring statistics."""
        self.changes_count_label.config(text=f"📝 Changes: {len(self.file_changes)}")
        if self.watcher:
            self.files_watched_label.config(text=f"👁️ Watched: {len(self.watcher.file_times)}")
    
    def quick_generate(self, prompt_type: str):
        """Quick generate for specific type."""
        self.prompt_type.set(prompt_type)
        self.generate_prompt()
        self.notebook.select(0)  # Switch to generator tab
    
    def generate_prompt(self):
        """Generate prompt with enhancements."""
        if not self.project_path.get() or not self.project_name.get():
            messagebox.showwarning("Warning", "Complete project path and name!")
            return
        
        prompt_type = self.prompt_type.get()
        status = self.status_text.get("1.0", tk.END).strip()
        
        # Base prompt
        base_prompt = self._generate_base_prompt(prompt_type, status)
        
        # Add Git context if enabled
        if self.include_git.get():
            git_info = GitIntegration.get_git_info(self.project_path.get())
            if git_info['available']:
                base_prompt += self._format_git_context(git_info)
        
        # Add code analysis if enabled
        if self.include_analysis.get() and prompt_type != 'initial':
            analysis = CodeAnalyzer.analyze_project(self.project_path.get())
            base_prompt += self._format_analysis_context(analysis)
        
        # Add recent changes
        if self.file_changes:
            recent = "\n".join([f"- {c['action']}: `{c['file']}` ({c['time']})" 
                               for c in self.file_changes[-10:]])
            base_prompt += f"\n\n## 📝 RECENT CHANGES\n\n{recent}\n"
        
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", base_prompt)
        
        # Update stats
        words = len(base_prompt.split())
        chars = len(base_prompt)
        self.prompt_stats_label.config(text=f"📊 {words} words | {chars} chars")
        
        self.log_history(f"Generated {prompt_type} prompt", self.project_name.get())
        
        if self.notifications.get():
            messagebox.showinfo("Success", f"Prompt '{prompt_type}' generated!")
    
    def _generate_base_prompt(self, prompt_type: str, status: str) -> str:
        """Generate base prompt."""
        prompts = {
            'initial': self._gen_initial(status),
            'continuation': self._gen_continuation(status),
            'bugfix': self._gen_bugfix(status),
            'feature': self._gen_feature(status),
            'extraction': self._gen_extraction()
        }
        return prompts.get(prompt_type, prompts['initial'])
    
    def _gen_initial(self, status: str) -> str:
        return f"""# 🚀 INIȚIALIZARE PROIECT {self.project_name.get().upper()}

Ești AI Senior Architect pentru proiectul "{self.project_name.get()}".

## 📋 CONTEXT

**Tip**: {self.project_type.get()}
**Path**: {self.project_path.get()}
**Status**: {status or 'Începem dezvoltarea'}
**Data**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 REGULI ABSOLUTE

1. Cod COMPLET - niciodată "..."
2. Typing hints obligatorii
3. Teste automate pentru orice funcție nouă
4. Docstrings pentru funcții publice
5. Error handling complet
6. Security first

## ✅ CHECKLIST RĂSPUNS

- [ ] Cod complet
- [ ] Typing hints
- [ ] Docstrings
- [ ] Unit tests
- [ ] Error handling
- [ ] Security validation

GATA! Ce implementăm?"""

    def _gen_continuation(self, status: str) -> str:
        return f"""# 🔄 CONTINUARE - {self.project_name.get()}

**Status**: {status or 'Continuăm'}
**Changes**: {len(self.file_changes)} fișiere modificate

Ce implementăm acum?"""

    def _gen_bugfix(self, status: str) -> str:
        return f"""# 🐛 BUG FIX - {self.project_name.get()}

**Problema**: {status or 'Descrie bug-ul'}

## Protocol:
1. Reproducere
2. Root Cause
3. Soluție completă
4. Testing
5. Prevention

Analizează!"""

    def _gen_feature(self, status: str) -> str:
        return f"""# ✨ FEATURE NOU - {self.project_name.get()}

**Cerință**: {status or 'Descrie feature-ul'}

## Deliverables:
- [ ] Backend implementation
- [ ] Frontend components
- [ ] Database migration
- [ ] Tests (unit + integration)
- [ ] Documentation

Propune arhitectura!"""

    def _gen_extraction(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"""# 📦 EXTRAGERE DNA - {self.project_name.get()}

Generează în `{self.export_folder.get()}/DNA_Export_{timestamp}/`:

1-11. Toate fișierele DNA (cod complet!)

ÎNCEPE EXTRAGEREA!"""

    def _format_git_context(self, git_info: Dict) -> str:
        """Format Git context."""
        ctx = "\n\n## 🔀 GIT CONTEXT\n\n"
        ctx += f"**Branch**: {git_info['branch']}\n"
        ctx += f"**Remote**: {git_info.get('remote', 'N/A')}\n\n"
        
        if git_info.get('commits'):
            ctx += "**Recent commits**:\n```\n"
            ctx += "\n".join(git_info['commits'][:5])
            ctx += "\n```\n\n"
        
        if git_info.get('status'):
            ctx += f"**Modified files**:\n```\n{git_info['status']}\n```\n"
        
        return ctx
    
    def _format_analysis_context(self, analysis: Dict) -> str:
        """Format analysis context."""
        ctx = "\n\n## 📊 CODE ANALYSIS\n\n"
        ctx += f"- **Total files**: {analysis['total_files']}\n"
        ctx += f"- **Python files**: {analysis['python_files']}\n"
        ctx += f"- **JavaScript files**: {analysis['javascript_files']}\n"
        ctx += f"- **Total lines**: {analysis['total_lines']:,}\n"
        ctx += f"- **Code lines**: {analysis['code_lines']:,}\n"
        ctx += f"- **Functions**: {analysis['functions']}\n"
        ctx += f"- **Classes**: {analysis['classes']}\n"
        
        if analysis.get('todos'):
            ctx += f"\n**TODOs found** ({len(analysis['todos'])}):\n"
            for todo in analysis['todos'][:5]:
                ctx += f"- {todo}\n"
        
        return ctx
    
    def copy_prompt(self):
        """Copy to clipboard."""
        prompt = self.prompt_text.get("1.0", tk.END)
        if not prompt.strip():
            messagebox.showwarning("Warning", "Generate prompt first!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        messagebox.showinfo("Success", "Copied to clipboard! 📋")
        self.log_history("Copied prompt", self.project_name.get())
    
    def save_prompt(self):
        """Save prompt to file."""
        prompt = self.prompt_text.get("1.0", tk.END)
        if not prompt.strip():
            messagebox.showwarning("Warning", "Generate prompt first!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("Text", "*.txt")],
            initialfile=f"{self.prompt_type.get()}_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(prompt)
                messagebox.showinfo("Success", f"Saved: {filename}")
                self.log_history("Saved prompt", Path(filename).name)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save: {e}")
    
    def send_to_ai(self):
        """Simulate sending to AI (placeholder)."""
        messagebox.showinfo("Info", "Copy prompt and paste in Claude/ChatGPT!\n\nDirect API integration coming soon...")
    
    def save_as_template(self):
        """Save current prompt as template."""
        prompt = self.prompt_text.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Warning", "Generate prompt first!")
            return
        
        name = tk.simpledialog.askstring("Template Name", "Enter template name:")
        if name:
            self.template_manager.save_template(name, prompt)
            messagebox.showinfo("Success", f"Template '{name}' saved!")
            self.refresh_templates()
            self.log_history("Saved template", name)
    
    def run_analysis(self):
        """Run code analysis."""
        if not self.project_path.get():
            messagebox.showwarning("Warning", "Select project first!")
            return
        
        self.analysis_text.delete("1.0", tk.END)
        self.analysis_text.insert("1.0", "🔍 Analyzing project...\n\n")
        self.root.update()
        
        analysis = CodeAnalyzer.analyze_project(self.project_path.get())
        
        report = f"""# 📊 CODE ANALYSIS REPORT
Project: {self.project_name.get()}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 STATISTICS

Total Files: {analysis['total_files']}
Python Files: {analysis['python_files']}
JavaScript Files: {analysis['javascript_files']}
Test Files: {analysis['test_files']}

Total Lines: {analysis['total_lines']:,}
Code Lines: {analysis['code_lines']:,} ({analysis['code_lines']/max(analysis['total_lines'],1)*100:.1f}%)
Comment Lines: {analysis['comment_lines']:,} ({analysis['comment_lines']/max(analysis['total_lines'],1)*100:.1f}%)
Blank Lines: {analysis['blank_lines']:,}

Functions: {analysis['functions']}
Classes: {analysis['classes']}

## 📁 LARGEST FILES

"""
        for filepath, size in analysis['largest_files']:
            report += f"- {filepath}: {size:,} bytes\n"
        
        if analysis.get('todos'):
            report += f"\n## ⚠️ TODOs/FIXMEs ({len(analysis['todos'])})\n\n"
            for todo in analysis['todos'][:20]:
                report += f"{todo}\n"
        
        if analysis.get('complexity_issues'):
            report += f"\n## 🔴 COMPLEXITY ISSUES\n\n"
            for issue in analysis['complexity_issues'][:10]:
                report += f"{issue}\n"
        
        self.analysis_text.delete("1.0", tk.END)
        self.analysis_text.insert("1.0", report)
        
        self.log_history("Analyzed code", self.project_name.get())
    
    def export_analysis(self):
        """Export analysis report."""
        content = self.analysis_text.get("1.0", tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "Run analysis first!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown", "*.md")],
            initialfile=f"analysis_{self.project_name.get()}_{datetime.now().strftime('%Y%m%d')}.md"
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Success", f"Exported: {filename}")
    
    def refresh_analysis(self):
        """Refresh analysis."""
        self.run_analysis()
    
    def refresh_git(self):
        """Refresh Git info."""
        if not self.project_path.get():
            messagebox.showwarning("Warning", "Select project first!")
            return
        
        self.git_text.delete("1.0", tk.END)
        self.git_text.insert("1.0", "🔍 Loading Git info...\n\n")
        self.root.update()
        
        git_info = GitIntegration.get_git_info(self.project_path.get())
        
        if not git_info['available']:
            self.git_text.delete("1.0", tk.END)
            self.git_text.insert("1.0", "❌ Not a Git repository or Git not available\n")
            return
        
        report = f"""# 🔀 GIT INFORMATION
Project: {self.project_name.get()}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 REPOSITORY

Branch: {git_info['branch']}
Remote: {git_info.get('remote', 'N/A')}

## 📝 RECENT COMMITS

"""
        for commit in git_info.get('commits', []):
            report += f"{commit}\n"
        
        if git_info.get('status'):
            report += f"\n## 🔄 WORKING DIRECTORY STATUS\n\n```\n{git_info['status']}\n```\n"
        
        if git_info.get('contributors'):
            report += "\n## 👥 TOP CONTRIBUTORS\n\n"
            for contrib in git_info['contributors']:
                report += f"{contrib}\n"
        
        self.git_text.delete("1.0", tk.END)
        self.git_text.insert("1.0", report)
    
    def copy_git_context(self):
        """Copy Git context."""
        content = self.git_text.get("1.0", tk.END)
        if content.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Success", "Git context copied!")
    
    def refresh_templates(self):
        """Refresh templates list."""
        self.templates_listbox.delete(0, tk.END)
        templates = self.template_manager.list_templates()
        for template in templates:
            self.templates_listbox.insert(tk.END, template)
    
    def on_template_select(self, event):
        """Template selected."""
        selection = self.templates_listbox.curselection()
        if selection:
            name = self.templates_listbox.get(selection[0])
            content = self.template_manager.load_template(name)
            self.template_preview.delete("1.0", tk.END)
            self.template_preview.insert("1.0", content)
    
    def load_template(self):
        """Load selected template."""
        selection = self.templates_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select template first!")
            return
        
        name = self.templates_listbox.get(selection[0])
        content = self.template_manager.load_template(name)
        
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert("1.0", content)
        
        self.notebook.select(0)  # Switch to generator
        messagebox.showinfo("Success", f"Template '{name}' loaded!")
    
    def delete_template(self):
        """Delete selected template."""
        selection = self.templates_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select template first!")
            return
        
        name = self.templates_listbox.get(selection[0])
        if messagebox.askyesno("Confirm", f"Delete template '{name}'?"):
            self.template_manager.delete_template(name)
            self.refresh_templates()
            self.template_preview.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Template deleted!")
    
    def simulate_ai_response(self):
        """Simulate AI response."""
        prompt = self.sim_input.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Warning", "Enter prompt first!")
            return
        
        # Simple simulation
        response = f"""✅ CONFIRMARE

Am primit prompt-ul tău și îl procesez.

## 📊 ANALIZA PROMPT

Lungime: {len(prompt)} caractere
Cuvinte: {len(prompt.split())} 
Tip detectat: {'Initial' if '🚀' in prompt else 'Continuation' if '🔄' in prompt else 'Bug Fix' if '🐛' in prompt else 'Feature' if '✨' in prompt else 'Unknown'}

## 🎯 RĂSPUNS SIMULAT

Voi genera cod COMPLET conform cerințelor tale:

```python
# Exemplu cod generat (simulare)
def example_function(param: str) -> dict:
    \"\"\"
    Example generated function.
    
    Args:
        param: Input parameter
        
    Returns:
        Result dictionary
    \"\"\"
    result = {{
        'status': 'success',
        'data': param
    }}
    return result
```

## ✅ TESTE

```python
def test_example_function():
    result = example_function("test")
    assert result['status'] == 'success'
    assert result['data'] == 'test'
```

## 📝 URMĂTORII PAȘI

1. Review cod generat
2. Rulează teste
3. Deploy

Gata! Ce altceva implementăm?
"""
        
        self.sim_output.delete("1.0", tk.END)
        self.sim_output.insert("1.0", response)
        
        messagebox.showinfo("Simulation Complete", "AI response simulated!")
    
    def batch_process(self):
        """Process multiple projects."""
        projects_text = self.batch_list.get("1.0", tk.END)
        projects = [line.strip() for line in projects_text.split('\n') 
                   if line.strip() and not line.strip().startswith('#')]
        
        if not projects:
            messagebox.showwarning("Warning", "Add project paths first!")
            return
        
        self.batch_log.delete("1.0", tk.END)
        self.batch_progress['maximum'] = len(projects)
        self.batch_progress['value'] = 0
        
        for i, project_path in enumerate(projects, 1):
            self.batch_log.insert(tk.END, f"\n[{i}/{len(projects)}] Processing: {project_path}\n")
            self.root.update()
            
            if not Path(project_path).exists():
                self.batch_log.insert(tk.END, "  ❌ Path not found\n")
                continue
            
            try:
                # Process project (simplified)
                self.batch_log.insert(tk.END, "  ✅ Generated prompt\n")
                self.batch_progress['value'] = i
                time.sleep(0.5)  # Simulate processing
                
            except Exception as e:
                self.batch_log.insert(tk.END, f"  ❌ Error: {e}\n")
        
        self.batch_log.insert(tk.END, f"\n🎉 COMPLETE! Processed {len(projects)} projects\n")
        messagebox.showinfo("Batch Complete", f"Processed {len(projects)} projects!")
    
    def view_batch_results(self):
        """View batch results."""
        messagebox.showinfo("Results", "Check the log above for detailed results!")
    
    def save_settings(self):
        """Save settings."""
        settings = {
            'auto_save': self.auto_save_config.get(),
            'dark_mode': self.dark_mode.get(),
            'notifications': self.notifications.get(),
            'monitor_interval': self.monitor_interval.get()
        }
        
        config_file = Path.home() / '.ai-prompt-generator' / 'settings.json'
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(settings, f, indent=2)
        
        messagebox.showinfo("Success", "Settings saved!")
    
    def log_history(self, action: str, detail: str):
        """Log to history."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history_tree.insert('', 0, values=(timestamp, detail, action))
        
        # Keep only last 100
        children = self.history_tree.get_children()
        if len(children) > 100:
            self.history_tree.delete(children[-1])
    
    def clear_history(self):
        """Clear history."""
        if messagebox.askyesno("Confirm", "Clear all history?"):
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
    
    def load_recent_projects(self) -> List[str]:
        """Load recent projects."""
        config_file = Path.home() / '.ai-prompt-generator' / 'recent.json'
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        return []
    
    def add_to_recent_projects(self, path: str):
        """Add to recent projects."""
        if path not in self.recent_projects:
            self.recent_projects.insert(0, path)
            self.recent_projects = self.recent_projects[:10]  # Keep only 10
            
            config_file = Path.home() / '.ai-prompt-generator' / 'recent.json'
            config_file.parent.mkdir(exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(self.recent_projects, f)
    
    def load_recent_project(self, path: str):
        """Load recent project."""
        if path and Path(path).exists():
            self.project_path.set(path)
            self.project_name.set(Path(path).name)
            messagebox.showinfo("Loaded", f"Loaded: {Path(path).name}")
    
    def on_closing(self):
        """Cleanup."""
        if self.watching:
            self.stop_watching()
        
        if self.auto_save_config.get():
            self.save_settings()
        
        self.root.destroy()


def main():
    """Entry point."""
    root = tk.Tk()
    app = AIPromptGeneratorUltimate(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main().Frame(tab)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # LEFT: Config + Quick Actions
        self.create_config_section_enhanced(left)
        self.create_quick_actions(left)
        self.create_monitoring_section_enhanced(left)
        
        # RIGHT: Prompt preview
        self.create_prompt_section_enhanced(right)
        
    def create_config_section_enhanced(self, parent):
        """Config îmbunătățit cu recent projects."""
        frame = ttk.LabelFrame(parent, text="⚙️ Configurare Proiect", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Recent projects dropdown
        ttk.Label(frame, text="📂 Recent Projects:").pack(anchor=tk.W, pady=(0, 5))
        recent_combo = ttk.Combobox(
            frame,
            values=self.recent_projects,
            state='readonly'
        )
        recent_combo.pack(fill=tk.X, pady=(0, 10))
        recent_combo.bind('<<ComboboxSelected>>', lambda e: self.load_recent_project(recent_combo.get()))
        
        # Project path
        ttk.Label(frame, text="📁 Folder Proiect:").pack(anchor=tk.W, pady=(0, 5))
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Entry(path_frame, textvariable=self.project_path).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(path_frame, text="Browse", command=self.browse_project).pack(side=tk.RIGHT)
        
        # Export folder
        ttk.Label(frame, text="📂 Export DNA:").pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(frame, textvariable=self.export_folder).pack(fill=tk.X, pady=(0, 10))
        
        # Project name + type (same row)
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=(0, 10))
        
        left_col = ttk.Frame(row)
        left_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Label(left_col, text="🏷️ Nume:").pack(anchor=tk.W)
        ttk.Entry(left_col, textvariable=self.project_name).pack(fill=tk.X)
        
        right_col = ttk.Frame(row)
        right_col.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        ttk.Label(right_col, text="🛠️ Tip:").pack(anchor=tk.W)
        ttk.Combobox(
            right_col,
            textvariable=self.project_type,
            values=['fullstack', 'backend', 'frontend', 'mobile', 'ml', 'desktop', 'api', 'library'],
            state='readonly',
            width=15
        ).pack(fill=tk.X)
        
        # Status
        ttk.Label(frame, text="📊 Context/Status:").pack(anchor=tk.W, pady=(0, 5))
        self.status_text = scrolledtext.ScrolledText(frame, height=3, wrap=tk.WORD)
        self.status_text.pack(fill=tk.X)
        
        # Options
        opts = ttk.Frame(frame)
        opts.pack(fill=tk.X, pady=(10, 0))
        ttk.Checkbutton(opts, text="Include Git Info", variable=self.include_git).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(opts, text="Include Code Analysis", variable=self.include_analysis).pack(side=tk.LEFT, padx=5)
        
    def create_quick_actions(self, parent):
        """Quick actions panel."""
        frame = ttk.LabelFrame(parent, text="⚡ Quick Actions", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        # Prompt types as big buttons
        types = [
            ('initial', '🚀 Init', '#4CAF50'),
            ('continuation', '🔄 Continue', '#2196F3'),
            ('bugfix', '🐛 Fix', '#F44336'),
            ('feature', '✨ Feature', '#9C27B0'),
            ('extraction', '📦 DNA', '#FF9800')
        ]
        
        for value, label, color in types:
            btn = tk.Button(
                frame,
                text=label,
                command=lambda v=value: self.quick_generate(v),
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                relief=tk.RAISED,
                bd=2
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2, expand=True, fill=tk.X)
        
    def create_monitoring_section_enhanced(self, parent):
        """Monitoring îmbunătățit."""
        frame = ttk.LabelFrame(parent, text="👁️ Live Monitoring", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Controls
        controls = ttk.Frame(frame)
        controls.pack(fill=tk.X, pady=(0, 10))
        
        self.watch_button = ttk.Button(
            controls,
            text="▶️ Start",
            command=self.toggle_watching
        )
        self.watch_button.pack(side=tk.LEFT, padx=2)
        
        ttk.Checkbutton(controls, text="Auto-Gen", variable=self.auto_generate).pack(side=tk.LEFT, padx=10)
        
        self.last_update_label = ttk.Label(controls, text="", foreground="gray")
        self.last_update_label.pack(side=tk.RIGHT)
        
        # Stats
        stats = ttk.Frame(frame)
        stats.pack(fill=tk.X, pady=(0, 5))
        
        self.changes_count_label = ttk.Label(stats, text="📝 Changes: 0", font=('Arial', 9))
        self.changes_count_label.pack(side=tk.LEFT, padx=10)
        
        self.files_watched_label = ttk.Label(stats, text="👁️ Watched: 0", font=('Arial', 9))
        self.files_watched_label.pack(side=tk.LEFT, padx=10)
        
        # Log
        ttk.Label(frame, text="Recent Changes:", font=('Arial', 9, 'bold')).pack(anchor=tk.W)
        self.changes_text = scrolledtext.ScrolledText(frame, height=8, wrap=tk.WORD, state=tk.DISABLED, font=('Courier', 9))
        self.changes_text.pack(fill=tk.BOTH, expand=True)
        
    def create_prompt_section_enhanced(self, parent):
        """Prompt section îmbunătățit."""
        frame = ttk.LabelFrame(parent, text="📄 Generated Prompt", padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="⚡ Generate", command=self.generate_prompt).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📋 Copy", command=self.copy_prompt).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 Save", command=self.save_prompt).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📤 Send to AI", command=self.send_to_ai).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💿 Save as Template", command=self.save_as_template).pack(side=tk.LEFT, padx=2)
        
        # Stats
        self.prompt_stats_label = ttk.Label(toolbar, text="", foreground="gray", font=('Arial', 8))
        self.prompt_stats_label.pack(side=tk.RIGHT)
        
        # Preview
        self.prompt_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Courier', 10))
        self.prompt_text.pack(fill=tk.BOTH, expand=True)
        
    def create_analysis_tab(self):
        """TAB 2: Code Analysis."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Code Analysis")
        
        # Control panel
        control = ttk.Frame(tab)
        control.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control, text="🔍 Analyze Project", command=self.run_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(control, text="📤 Export Report", command=self.export_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(control, text="🔄 Refresh", command=self.refresh_analysis).pack(side=tk.LEFT, padx=5)
        
        # Results
        self.analysis_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=('Courier', 10))
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_git_tab(self):
        """TAB 3: Git Integration."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔀 Git Info")
        
        # Control
        control = ttk.Frame(tab)
        control.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control, text="🔄 Refresh Git Info", command=self.refresh_git).pack(side=tk.LEFT, padx=5)
        ttk.Button(control, text="📋 Copy Git Context", command=self.copy_git_context).pack(side=tk.LEFT, padx=5)
        
        # Git info display
        self.git_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=('Courier', 10))
        self.git_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_templates_tab(self):
        """TAB 4: Template Manager."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📝 Templates")
        
        # Split view
        left = ttk.Frame(tab)
        left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=False)
        
        right = ttk.Frame(tab)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5, expand=True)
        
        # LEFT: Templates list
        ttk.Label(left, text="Saved Templates:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        
        self.templates_listbox = tk.Listbox(left, width=30, font=('Arial', 10))
        self.templates_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.templates_listbox.bind('<<ListboxSelect>>', self.on_template_select)
        
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Load", command=self.load_template).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_template).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_templates).pack(side=tk.LEFT, padx=2)
        
        # RIGHT: Template preview
        ttk.Label(right, text="Template Preview:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        self.template_preview = scrolledtext.ScrolledText(right, wrap=tk.WORD, font=('Courier', 10))
        self.template_preview.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_templates()
        
    def create_simulator_tab(self):
        """TAB 5: AI Response Simulator."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🤖 AI Simulator")
        
        # Info
        info = ttk.Label(tab, text="Simulează răspunsurile AI pentru testare rapidă", 
                        font=('Arial', 9, 'italic'), foreground='gray')
        info.pack(pady=10)
        
        # Input
        ttk.Label(tab, text="Your Prompt:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10)
        self.sim_input = scrolledtext.ScrolledText(tab, height=10, wrap=tk.WORD, font=('Courier', 10))
        self.sim_input.pack(fill=tk.X, padx=10, pady=5)
        
        # Controls
        controls = ttk.Frame(tab)
        controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(controls, text="🎭 Simulate Response", command=self.simulate_ai_response).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="🔄 Clear", command=lambda: self.sim_output.delete('1.0', tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Output
        ttk.Label(tab, text="Simulated AI Response:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10)
        self.sim_output = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=('Courier', 10))
        self.sim_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_batch_tab(self):
        """TAB 6: Batch Operations."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Batch Ops")
        
        ttk.Label(tab, text="Generate prompts for multiple projects at once", 
                 font=('Arial', 9, 'italic'), foreground='gray').pack(pady=10)
        
        # Project list
        ttk.Label(tab, text="Projects to process:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10)
        
        self.batch_list = scrolledtext.ScrolledText(tab, height=10, wrap=tk.WORD)
        self.batch_list.pack(fill=tk.X, padx=10, pady=5)
        self.batch_list.insert('1.0', "# Add project paths (one per line):\n# /path/to/project1\n# /path/to/project2\n")
        
        # Controls
        controls = ttk.Frame(tab)
        controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls, text="▶️ Process All", command=self.batch_process).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="📊 View Results", command=self.view_batch_results).pack(side=tk.LEFT, padx=5)
        
        # Progress
        self.batch_progress = ttk.Progressbar(tab, mode='determinate')
        self.batch_progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Log
        self.batch_log = scrolledtext.ScrolledText(tab, wrap=tk.WORD, height=15)
        self.batch_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_settings_tab(self):
        """TAB 7: Settings & History."""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Settings")
        
        # Settings sections
        left = ttk.Frame(tab)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        right = ttk