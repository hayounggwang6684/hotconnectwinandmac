from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class IncomingJpegHandler(FileSystemEventHandler):
    def __init__(self):
        self._recent: dict[Path, float] = {}

    def on_created(self, event: FileSystemEvent):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in {".jpg", ".jpeg"}:
            return

        now = time.time()
        if path in self._recent and now - self._recent[path] < 1.0:
            return
        self._recent[path] = now

        self._set_clipboard_from_file(path)

    @staticmethod
    def _set_clipboard_from_file(path: Path):
        script = (
            'set the clipboard to (read (POSIX file "{}") as JPEG picture)'.format(
                str(path)
            )
        )
        subprocess.run(["osascript", "-e", script], check=True)
        print(f"[mac_clip] 클립보드 업데이트: {path}")


def main():
    if sys.platform != "darwin":
        raise RuntimeError("mac_clip은 macOS에서만 실행할 수 있습니다.")

    watch_dir = Path.home() / "IncomingShots"
    watch_dir.mkdir(parents=True, exist_ok=True)

    event_handler = IncomingJpegHandler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=False)
    observer.start()

    print(f"[mac_clip] 감시 시작: {watch_dir}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
