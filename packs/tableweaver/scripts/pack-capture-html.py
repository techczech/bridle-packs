from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
spec = importlib.util.spec_from_file_location("pack_common", Path(__file__).resolve().parent / "pack-common.py")
pack_common = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(pack_common)

from tableweaver.capture_html import capture_html


def main() -> int:
    args = pack_common.read_args()
    html = args.get("html")
    input_html = args.get("input_html")
    source = args.get("source")
    if not isinstance(html, str) and not isinstance(input_html, str):
        print("html or input_html is required", file=sys.stderr)
        return 2
    tables = capture_html(input_html or html, source=source, captured_at=args.get("captured_at"))
    pack_common.write_or_print(json.dumps(tables, indent=2, sort_keys=True) + "\n", args.get("output_json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
