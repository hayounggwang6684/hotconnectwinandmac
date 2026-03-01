from __future__ import annotations

import io
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageGrab
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)

if sys.platform == "win32":
    import win32clipboard
else:
    raise RuntimeError("win_push는 Windows에서만 실행할 수 있습니다.")


class PreviewDialog(QDialog):
    def __init__(self, image: Image.Image, parent=None):
        super().__init__(parent)
        self.setWindowTitle("클립보드 이미지 미리보기")
        self._image = image

        label = QLabel("새 클립보드 이미지가 감지되었습니다. 저장할까요?")
        preview = QLabel()
        preview.setPixmap(self._pil_to_pixmap(image))
        preview.setScaledContents(True)
        preview.setMinimumSize(400, 300)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(preview)
        layout.addWidget(buttons)
        self.setLayout(layout)

    @staticmethod
    def _pil_to_pixmap(image: Image.Image) -> QPixmap:
        buffer = io.BytesIO()
        image.convert("RGB").save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue(), "PNG")
        return pixmap


class ClipboardWatcher:
    def __init__(self, save_dir: Path):
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)
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
            self._save_as_jpeg(image)

    def _save_as_jpeg(self, image: Image.Image):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = self.save_dir / f"shot_{ts}.jpg"
        image.convert("RGB").save(target, format="JPEG", quality=92)
        print(f"[win_push] 저장 완료: {target}")


def main():
    app = QApplication(sys.argv)
    watcher = ClipboardWatcher(Path("Z:\\"))
    watcher.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
