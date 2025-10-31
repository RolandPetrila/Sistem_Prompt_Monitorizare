"""Main entry point for AI Prompt Generator Ultimate."""
from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main() -> int:
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("AI Prompt Generator Ultimate")
    app.setOrganizationName("AI Tools")
    
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

