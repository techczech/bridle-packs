from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from typing import Any


MODEL_KIND = "tablemodel"
MODEL_VERSION = "1.0"


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_id(*parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, ensure_ascii=True, default=str)
    return "tbl_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def scalar(value: Any) -> dict[str, Any]:
    if value is None:
        return {"kind": "scalar", "value": "", "data_type": "empty"}
    if isinstance(value, bool):
        return {"kind": "scalar", "value": value, "data_type": "boolean"}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"kind": "scalar", "value": value, "data_type": "integer"}
    if isinstance(value, float):
        return {"kind": "scalar", "value": value, "data_type": "number"}

    text = str(value).strip()
    if text == "":
        return {"kind": "scalar", "value": "", "data_type": "empty"}
    try:
        number = float(text.replace(",", ""))
        if text.replace(",", "").isdigit():
            return {"kind": "scalar", "value": int(number), "data_type": "integer"}
        return {"kind": "scalar", "value": number, "data_type": "number"}
    except ValueError:
        return {"kind": "scalar", "value": text, "data_type": "string"}


def cell_to_text(value: Any) -> str:
    if value is None:
        return ""
    kind = value.get("kind") if isinstance(value, dict) else None
    if kind == "scalar":
        return str(value.get("value", ""))
    if kind == "list":
        return "; ".join(cell_to_text(item) for item in value.get("items", []))
    if kind == "rich_text":
        chunks: list[str] = []
        for block in value.get("blocks", []):
            if "text" in block:
                chunks.append(str(block["text"]))
            elif "items" in block:
                chunks.append("; ".join(str(item) for item in block["items"]))
        return "; ".join(chunk for chunk in chunks if chunk)
    if kind == "table":
        nested = value.get("table", {})
        rows = []
        for row in nested.get("rows", []):
            rows.append(" | ".join(cell_to_text(cell) for cell in row.get("cells", [])))
        return "[nested table: " + "; ".join(row for row in rows if row) + "]"
    return str(value)


def cell_type(value: Any) -> str:
    if value is None:
        return "empty"
    if not isinstance(value, dict):
        return "unknown"
    if value.get("kind") == "scalar":
        return str(value.get("data_type", "string"))
    return str(value.get("kind"))


def path_label(path: list[str]) -> str:
    return " / ".join(path)


def clone_table(table: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(table)


def rebuild_schema(table: dict[str, Any]) -> dict[str, Any]:
    leaf_paths = table.get("schema_fingerprint", {}).get("leaf_column_paths", [])
    types: list[str] = []
    for index, _path in enumerate(leaf_paths):
        seen = [cell_type(row.get("cells", [])[index]) for row in table.get("rows", []) if index < len(row.get("cells", []))]
        useful = [value for value in seen if value not in {"empty", "unknown"}]
        types.append(useful[0] if useful else "empty")
    fingerprint_value = hashlib.sha256(json.dumps({"paths": leaf_paths, "types": types}, ensure_ascii=True).encode("utf-8")).hexdigest()
    table["schema_fingerprint"] = {
        "leaf_column_paths": leaf_paths,
        "types": types,
        "value": fingerprint_value,
    }
    return table


def make_table(
    *,
    title: str,
    source: str,
    capture_method: str,
    row_header_paths: list[list[str]],
    leaf_column_paths: list[list[str]],
    rows: list[dict[str, Any]],
    spans: list[dict[str, Any]] | None = None,
    captured_at: str | None = None,
    table_id: str | None = None,
    columns: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    table = {
        "kind": MODEL_KIND,
        "model_version": MODEL_VERSION,
        "id": table_id or stable_id(source, title, row_header_paths, leaf_column_paths, rows),
        "title": title,
        "provenance": {
            "source": source,
            "capture_method": capture_method,
            "captured_at": captured_at or utc_timestamp(),
        },
        "schema_fingerprint": {
            "leaf_column_paths": leaf_column_paths,
            "types": [],
            "value": "",
        },
        "columns": columns or [],
        "row_header_columns": [{"index": index, "path": path} for index, path in enumerate(row_header_paths)],
        "rows": rows,
        "spans": spans or [],
    }
    return rebuild_schema(table)
