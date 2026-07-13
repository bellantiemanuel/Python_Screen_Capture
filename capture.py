#!/usr/bin/env python3
"""CLI tool for screen capture with mouse click loop."""

import argparse
import sys
import threading
from datetime import datetime
from pathlib import Path

import mss
import mss.tools
from pynput.mouse import Listener as MouseListener


class CaptureSession:
    def __init__(self, sct: mss.MSS, monitor_index: int | None, fmt: str, output_dir: Path):
        self.sct = sct
        self.monitor_index = monitor_index
        self.fmt = fmt
        self.output_dir = output_dir
        self.counter = 0
        self._lock = threading.Lock()

    def grab(self) -> Path:
        with self._lock:
            monitor = self.sct.monitors[self.monitor_index] if self.monitor_index else self.sct.monitors[0]
            screenshot = self.sct.grab(monitor)
            raw = mss.tools.to_png(screenshot.rgb, screenshot.size)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = self.output_dir / f"capture_{ts}_{self.counter:04d}.{self.fmt}"
            path.write_bytes(raw)
            self.counter += 1
            return path


def get_output_path(output: str | None, fmt: str) -> Path:
    if output:
        path = Path(output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path(f"capture_{timestamp}.{fmt}")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def capture_full(sct: mss.MSS, monitor_index: int | None, fmt: str, output: Path) -> Path:
    monitor = sct.monitors[monitor_index] if monitor_index else sct.monitors[0]
    screenshot = sct.grab(monitor)
    raw = mss.tools.to_png(screenshot.rgb, screenshot.size)
    output.write_bytes(raw)
    return output


def list_monitors(sct: mss.MSS) -> None:
    for i, mon in enumerate(sct.monitors):
        label = "All" if i == 0 else f"Monitor {i}"
        print(f"  [{i}] {label}: {mon['width']}x{mon['height']} at ({mon['left']}, {mon['top']})")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture screenshots from the command line."
    )
    parser.add_argument("-o", "--output", help="Output file path (single capture) or directory (loop mode).")
    parser.add_argument("-f", "--format", choices=["png", "jpg", "bmp", "gif", "tiff"], default="png", help="Image format (default: png)")
    parser.add_argument("-m", "--monitor", type=int, default=None, help="Monitor index to capture.")
    parser.add_argument("-l", "--list", action="store_true", help="List available monitors and exit.")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay in seconds before capture.")
    parser.add_argument("--loop", action="store_true", help="Click-to-capture mode: each mouse click saves a screenshot.")

    args = parser.parse_args()

    with mss.MSS() as sct:
        if args.list:
            list_monitors(sct)
            return 0

        if args.delay > 0:
            import time
            print(f"Capturing in {args.delay}s...")
            time.sleep(args.delay)

        if not args.loop:
            output = get_output_path(args.output, args.format)
            result = capture_full(sct, args.monitor, args.format, output)
            print(f"Saved: {result}")
            return 0

        output_dir = Path(args.output) if args.output else Path(".")
        output_dir.mkdir(parents=True, exist_ok=True)

        session = CaptureSession(sct, args.monitor, args.format, output_dir)

        def on_click(x, y, button, pressed):
            if pressed:
                path = session.grab()
                print(f"[{session.counter}] Saved: {path}")

        print("Click-to-capture active. Each click saves a screenshot.")
        print("Press Ctrl+C to stop.")

        with MouseListener(on_click=on_click) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                listener.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
