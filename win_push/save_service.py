from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image


class SaveService:
    def __init__(self, save_dir: Path):
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def save_jpeg(self, image: Image.Image) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = self.save_dir / f"{ts}.jpg"
        image.convert("RGB").save(target, format="JPEG", quality=92)
        print(f"[win_push] 저장 완료: {target}")
        return target
