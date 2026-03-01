from __future__ import annotations

import sys
import time
from pathlib import Path

from mac_clip.watcher import IncomingShotsWatcher


def main():
    if sys.platform != "darwin":
        raise RuntimeError("mac_clip은 macOS에서만 실행할 수 있습니다.")

    watcher = IncomingShotsWatcher(Path.home() / "IncomingShots")
    watcher.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watcher.stop()


if __name__ == "__main__":
    main()
