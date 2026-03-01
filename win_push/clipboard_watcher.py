from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageGrab
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog

from .preview_dialog import PreviewDialog
from .save_service import SaveService

if sys.platform == "win32":
    import win32clipboard
else:
    raise RuntimeError("win_push는 Windows에서만 실행할 수 있습니다.")


class ClipboardWatcher:
    def __init__(self, save_dir: Path):
        self.save_service = SaveService(save_dir)
        self.last_seq = win32clipboard.GetClipboardSequenceNumber()

        self.timer = QTimer()
        self.timer.setInterval(800)
        self.timer.timeout.connect(self.check_clipboard)

    def start(self):
        self.timer.start()

    def check_clipboard(self):
        seq = win32clipboard.GetClipboardSequenceNumber()
        if seq == self.last_seq:
            return

        self.last_seq = seq
        image = ImageGrab.grabclipboard()
        if not isinstance(image, Image.Image):
            return

        dialog = PreviewDialog(image)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.save_service.save_jpeg(image)
