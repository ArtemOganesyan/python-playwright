from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Record a Python pytest Playwright test.")
    parser.add_argument("url", nargs="?", default="https://nop-qa.portnov.com/")
    parser.add_argument("-o", "--output", default="tests/recorded_test.py")
    parser.add_argument("-b", "--browser", default="chromium", choices=["chromium", "firefox", "webkit"])
    parser.add_argument("--viewport-size", default="1440,1000")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "playwright",
        "codegen",
        "--target",
        "python-pytest",
        "--browser",
        args.browser,
        "--viewport-size",
        args.viewport_size,
        "--output",
        str(output),
        args.url,
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())

