# AI Prompt Generator Ultimate

**Sistem de Monitorizare și Promting Smart pentru Proiecte Software**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-107%2F107%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-93%25-success.svg)]()

## 📋 Descriere

AI Prompt Generator Ultimate este o aplicație desktop completă pentru generarea și optimizarea prompturilor AI pentru analiza și îmbunătățirea proiectelor software. Aplicația oferă:

- 🎯 **Multi-AI Orchestration** - Suport pentru Claude, OpenAI, Gemini cu fallback automat
- 📊 **Context Analysis** - Analiză automată a structurii proiectului
- 🔄 **Incremental Workflow** - Workflow incremental pentru îmbunătățiri pas cu pas
- 📸 **Backup Manager** - Snapshot-uri și restore pentru proiecte
- 📈 **Monitoring** - Monitorizare automată a modificărilor de fișiere
- 🛠️ **12 Quick Tasks** - Task-uri rapide pentru analiză și optimizare

## ✨ Caracteristici

### Core Features
- **Multi-AI Support**: Claude, OpenAI, Gemini cu fallback automat
- **Context Engine**: Analiză automată a proiectelor
- **Prompt Generation**: Generare inteligentă de prompturi pentru diferite task-uri
- **Change Detection**: Detecție automată a modificărilor în fișiere
- **Backup System**: Snapshot-uri și restore
- **Incremental Workflow**: Tracking pentru workflow incremental

### Quick Tasks
1. **Code Quality Analysis** - Analiză calitate cod
2. **Bug Detection** - Detectare bug-uri
3. **Performance Optimization** - Optimizare performanță
4. **Security Audit** - Audit de securitate
5. **Test Generation** - Generare teste
6. **Code Refactoring** - Sugestii de refactoring
7. **Documentation Generator** - Generare documentație
8. **Architecture Review** - Review arhitectură
9. **Dependency Check** - Verificare dependențe
10. **Migration Helper** - Asistent migrare
11. **Code Style Fix** - Corectare stil cod
12. **Performance Profiling** - Profiling performanță

## 🚀 Instalare

### Metoda 1: Executabil Standalone (Recomandat)
1. Descarcă `AIPromptGenerator_Setup_1.0.0.exe`
2. Rulează instalatorul
3. Urmează wizard-ul de instalare
4. Lansează din Start Menu sau shortcut Desktop

### Metoda 2: Din Sursă
```bash
# Clonează repository-ul
git clone <repository-url>
cd ai_prompt_generator_ultimate

# Instalează dependențe
pip install -r requirements.txt

# Configurează API keys în config_local.json
# Sau rulează:
python scripts/load_api_keys.py

# Rulează aplicația
python main.py
```

### Metoda 3: Build de la Sursă
```bash
# Build executabil
python build_exe.py

# Sau folosește script-ul de build
build.bat
```

## ⚙️ Configurare

### API Keys
Editează `config_local.json` sau folosește tab-ul Settings din GUI:

```json
{
  "ai_providers": {
    "claude": {
      "api_key": "your-claude-key",
      "model": "claude-sonnet-4-20250514",
      "priority": 1,
      "enabled": true
    },
    "openai": {
      "api_key": "your-openai-key",
      "model": "gpt-4-turbo-preview",
      "priority": 2,
      "enabled": true
    },
    "gemini": {
      "api_key": "your-gemini-key",
      "model": "gemini-1.5-pro",
      "priority": 3,
      "enabled": true
    }
  },
  "fallback_strategy": {
    "enabled": true,
    "retry_count": 3,
    "timeout": 30
  }
}
```

## 📖 Utilizare

### Prima Rulare
1. Lansează aplicația
2. Mergi la tab-ul **Settings**
3. Introdu API keys-urile tale
4. Selectează un proiect în tab-ul **Prompt Generator**
5. Începe să generezi prompturi!

### Generare Prompturi
1. Tab **Prompt Generator**
2. Selectează directorul proiectului
3. Alege tipul de task
4. Click **Generate Prompt**
5. Click **Send to AI** pentru răspuns

### Monitoring
1. Tab **Monitoring**
2. Selectează proiectul
3. Activează **Enable Monitoring**
4. Vezi modificările în timp real

### Backup
1. Tab **Backup**
2. Selectează proiectul
3. Click **Create Snapshot**
4. Restore când este nevoie

## 🏗️ Structură Proiect

```
ai_prompt_generator_ultimate/
├── core/                    # Module core
│   ├── ai_orchestrator.py   # Multi-AI orchestrator
│   ├── context_engine.py    # Context analysis
│   ├── database.py          # Database manager
│   └── ...
├── tasks/                   # Quick tasks
│   ├── analyze_code_quality.py
│   ├── find_bugs.py
│   └── ...
├── gui/                     # GUI components
│   ├── main_window.py       # Main window
│   └── tabs/               # Tab implementations
├── tests/                   # Test suite
├── scripts/                 # Utility scripts
├── main.py                  # Entry point
└── requirements.txt         # Dependencies
```

## 🧪 Testing

```bash
# Rulează toate testele
pytest tests/ -v

# Cu coverage
pytest tests/ --cov=core --cov=tasks --cov-report=html

# Teste specifice
pytest tests/test_ai_orchestrator.py -v
```

**Coverage**: 93% (Core: 86%, Tasks: 100%)

## 📊 Statistici Proiect

- **Module**: 28 implementate
- **Teste**: 107/107 passing (100%)
- **Coverage**: 93%
- **GUI Tabs**: 7 tab-uri complete
- **Quick Tasks**: 12 task-uri implementate

## 🔧 Build și Packaging

### PyInstaller
```bash
python build_exe.py
```

### NSIS Installer
```bash
makensis installer.nsi
```

## 📝 Documentație Suplimentară

- [INSTALLATION.md](INSTALLATION.md) - Ghid instalare detaliat
- [LICENSE](LICENSE) - Licență
- [IMPLEMENTATION_PROGRESS.md](IMPLEMENTATION_PROGRESS.md) - Progres implementare

## 🤝 Contribuții

Contribuțiile sunt binevenite! Te rugăm să:
1. Fork repository-ul
2. Creează un branch pentru feature (`git checkout -b feature/AmazingFeature`)
3. Commit schimbările (`git commit -m 'Add AmazingFeature'`)
4. Push la branch (`git push origin feature/AmazingFeature`)
5. Deschide un Pull Request

## 📄 Licență

Acest proiect este licențiat sub licența MIT - vezi [LICENSE](LICENSE) pentru detalii.

## 🙏 Mulțumiri

- PySide6 pentru GUI framework
- Anthropic, OpenAI, Google pentru AI APIs
- Comunitatea open-source pentru librării utile

## 📧 Contact

Pentru întrebări sau probleme, deschide un issue pe GitHub.

---

**Made with ❤️ for better software development**
