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

from tableweaver.validate import TABLEMODEL_SCHEMA, TableModelValidationError, validate_table_model


def main() -> int:
    args = pack_common.read_args()
    if args.get("print_schema"):
        pack_common.write_or_print(json.dumps(TABLEMODEL_SCHEMA, indent=2, sort_keys=True) + "\n", args.get("output_path"))
        return 0
    data = pack_common.read_json_arg(args, "table")
    tables = data if isinstance(data, list) else [data]
    try:
        for table in tables:
            validate_table_model(table)
    except TableModelValidationError as error:
        print(str(error), file=sys.stderr)
        return 1
    pack_common.write_or_print(json.dumps({"valid": True, "count": len(tables)}, indent=2) + "\n", args.get("output_path"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
