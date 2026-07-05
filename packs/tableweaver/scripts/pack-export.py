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

from tableweaver.export import export_csv, export_json, export_markdown, export_tsv


def _table(args):
    data = pack_common.read_json_arg(args, "table")
    if isinstance(data, list):
        data = data[int(args.get("table_index", 0))]
    return data


def main() -> int:
    args = pack_common.read_args()
    table = _table(args)
    format_name = args.get("format", "json")
    if format_name == "json":
        pack_common.write_or_print(export_json(table), args.get("output_path"))
        return 0
    if format_name == "markdown":
        pack_common.write_or_print(export_markdown(table), args.get("output_path"))
        return 0
    if format_name == "csv":
        text, report = export_csv(table)
    elif format_name == "tsv":
        text, report = export_tsv(table)
    else:
        print(f"Unknown export format: {format_name}", file=sys.stderr)
        return 2
    pack_common.write_or_print(text, args.get("output_path"))
    if args.get("loss_report_path"):
        Path(args["loss_report_path"]).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    else:
        print(json.dumps(report, indent=2, sort_keys=True), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
