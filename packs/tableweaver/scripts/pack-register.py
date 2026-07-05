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

from tableweaver.registry import register


def _table(args):
    data = pack_common.read_json_arg(args, "table")
    if isinstance(data, list):
        data = data[int(args.get("table_index", 0))]
    return data


def main() -> int:
    args = pack_common.read_args()
    if not args.get("registry_dir"):
        print("registry_dir is required", file=sys.stderr)
        return 2
    result = register(args["registry_dir"], _table(args), tags=args.get("tags"))
    pack_common.write_or_print(json.dumps(result, indent=2, sort_keys=True) + "\n", args.get("output_path"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
