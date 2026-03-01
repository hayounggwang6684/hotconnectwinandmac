from __future__ import annotations

import subprocess
from pathlib import Path


def set_clipboard_from_jpeg(path: Path):
    script = 'set the clipboard to (read (POSIX file "{}") as JPEG picture)'.format(
        str(path)
    )
    subprocess.run(["osascript", "-e", script], check=True)
    print(f"[mac_clip] 클립보드 업데이트: {path}")
