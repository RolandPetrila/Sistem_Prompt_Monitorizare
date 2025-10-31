#!/usr/bin/env python3
"""
AI Prompt Generator - Aplicație Desktop
Generează prompturi perfecte pentru AI din proiectul tău + monitoring real-time
"""
import os
import sys
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProjectWatcher(FileSystemEventHandler):
    """Monitor schimbări în folder proiect."""
    
    def __init__(self, callback):
        self.callback = callback
        self.last_modified = {}
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Ignoră fișiere temporare
        if any(x in event.src_path for x in ['.git', '__pycache__', '.pyc', 'node_modules']):
            return
        
        # Debounce - evită multiple events pentru același fișier
        now = time.time()
        if event.src_path in self.last_modified:
            if now - self.last_modified[event.src_path] < 2:
                return
        
        self.last_modified[event.src_path] = now
        self.callback('modified', event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            self.callback('created', event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.callback('deleted', event.src_path)


class AIPromptGenerator:
    """Aplicația principală."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Prompt Generator Pro")
        self.root.geometry("1400x900")
        
        # State
        self.project_path = tk.StringVar()
        self.export_folder = tk.StringVar(value="Update_AI/DNA_Export")
        self.project_name = tk.StringVar()
        self.project_type = tk.StringVar(value="fullstack")
        self.current_status = tk.StringVar()
        self.prompt_type = tk.StringVar(value="initial")
        self.watching = False
        self.observer = None
        self.file_changes: List[Dict] = []
        self.auto_generate = tk.BooleanVar(value=False)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Creează interfața."""
        # Stil
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Container principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            header,
            text="🤖 AI Prompt Generator Pro",
            style='Title.TLabel'
        ).pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(header, text="● Ready", foreground="green")
        self.status_label.pack(side=tk.RIGHT)
        
        # Layout cu 2 coloane
        content = ttk.Frame(main_frame)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Coloana stânga - Configurare
        left_panel = ttk.Frame(content)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_config_section(left_panel)
        self.create_prompt_type_section(left_panel)
        self.create_monitoring_section(left_panel)
        
        # Coloana dreapta - Prompt
        right_panel = ttk.Frame(content)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_prompt_section(right_panel)
        
    def create_config_section