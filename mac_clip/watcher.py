from __future__ import annotations

import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from mac_clip.clipboard_setter import set_clipboard_from_jpeg


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

        set_clipboard_from_jpeg(path)


class IncomingShotsWatcher:
    def __init__(self, watch_dir: Path):
        self.watch_dir = watch_dir
        self.watch_dir.mkdir(parents=True, exist_ok=True)
        self.observer = Observer()
        self.event_handler = IncomingJpegHandler()

    def start(self):
        self.observer.schedule(self.event_handler, str(self.watch_dir), recursive=False)
        self.observer.start()
        print(f"[mac_clip] 감시 시작: {self.watch_dir}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
