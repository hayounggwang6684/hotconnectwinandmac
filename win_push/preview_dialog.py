from __future__ import annotations

import io

from PIL import Image
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class PreviewDialog(QDialog):
    def __init__(self, image: Image.Image, parent=None):
        super().__init__(parent)
        self.setWindowTitle("클립보드 이미지 미리보기")

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
