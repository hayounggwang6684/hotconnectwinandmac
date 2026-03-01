from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from win_push.clipboard_watcher import ClipboardWatcher


def main():
    app = QApplication(sys.argv)
    watcher = ClipboardWatcher(Path("Z:\\"))
    watcher.start()
    app.exec()


if __name__ == "__main__":
    main()
