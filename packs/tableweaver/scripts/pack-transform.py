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

from tableweaver.transform import transform_table


def main() -> int:
    args = pack_common.read_args()
    table = pack_common.read_json_arg(args, "table")
    if isinstance(table, list):
        table = table[int(args.get("table_index", 0))]
    spec_arg = args.get("transform") or args.get("spec")
    if not isinstance(spec_arg, dict):
        print("transform/spec is required", file=sys.stderr)
        return 2
    transformed = transform_table(table, spec_arg)
    pack_common.write_or_print(json.dumps(transformed, indent=2, sort_keys=True) + "\n", args.get("output_json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
