from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any

from .model import cell_to_text, clone_table, make_table, path_label, scalar
from .validate import validate_table_model


def _leaf_labels(table: dict[str, Any]) -> list[str]:
    return [path_label(path) for path in table["schema_fingerprint"]["leaf_column_paths"]]


def _label_labels(table: dict[str, Any]) -> list[str]:
    return [path_label(column["path"]) for column in table["row_header_columns"]]


def _data_index(table: dict[str, Any], column: str) -> int:
    labels = _leaf_labels(table)
    if column in labels:
        return labels.index(column)
    for index, label in enumerate(labels):
        if label.split(" / ")[-1] == column:
            return index
    raise ValueError(f"Unknown data column: {column}")


def _row_label_values(table: dict[str, Any], row: dict[str, Any], column: str) -> list[str]:
    labels = _label_labels(table)
    values = [cell_to_text(label) for label in row["labels"]]
    if column in labels:
        return [value for label, value in zip(labels, values) if label == column]
    if column in {label.split(" / ")[-1] for label in labels}:
        return [value for label, value in zip(labels, values) if label.split(" / ")[-1] == column]
    return values if column in labels or column == "Archive labels" else []


def _column_value(table: dict[str, Any], row: dict[str, Any], column: str) -> str:
    label_values = _row_label_values(table, row, column)
    if label_values:
        return label_values[0]
    return cell_to_text(row["cells"][_data_index(table, column)])


def _numbers(rows: list[dict[str, Any]], index: int) -> list[float]:
    values = []
    for row in rows:
        cell = row["cells"][index]
        if isinstance(cell, dict) and cell.get("kind") == "scalar" and cell.get("data_type") in {"integer", "number"}:
            values.append(float(cell["value"]))
    return values


def _aggregate(function: str, values: list[float]) -> int | float:
    if function == "sum":
        result = sum(values)
    elif function == "avg":
        result = mean(values) if values else 0
    elif function == "count":
        result = len(values)
    elif function == "min":
        result = min(values) if values else 0
    elif function == "max":
        result = max(values) if values else 0
    else:
        raise ValueError(f"Unknown aggregate function: {function}")
    return int(result) if isinstance(result, float) and result.is_integer() else result


def _derived(table: dict[str, Any], op: str, row_header_paths: list[list[str]], leaf_paths: list[list[str]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    return make_table(
        title=f"{table['title']} ({op})",
        source=table["id"],
        capture_method=f"transform:{op}",
        row_header_paths=row_header_paths,
        leaf_column_paths=leaf_paths,
        rows=rows,
        spans=[],
    )


def _transpose(table: dict[str, Any]) -> dict[str, Any]:
    leaf_labels = _leaf_labels(table)
    new_leaf_paths = [
        [" / ".join(cell_to_text(label) for label in row["labels"] if cell_to_text(label)) or f"Row {row['index'] + 1}"]
        for row in table["rows"]
    ]
    rows = []
    for index, leaf in enumerate(leaf_labels):
        rows.append({
            "index": index,
            "labels": [scalar(leaf)],
            "cells": [row["cells"][index] for row in table["rows"]],
        })
    return _derived(table, "transpose", [["Column"]], new_leaf_paths, rows)


def _group_by(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    by = spec["by"]
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in table["rows"]:
        groups[_column_value(table, row, by)].append(row)
    aggregations = spec.get("aggregations", [])
    leaf_paths = [[item.get("as") or f"{item['function']} {item['column']}"] for item in aggregations]
    rows = []
    for index, (key, group_rows) in enumerate(groups.items()):
        cells = []
        for item in aggregations:
            values = _numbers(group_rows, _data_index(table, item["column"]))
            cells.append(scalar(_aggregate(item["function"], values)))
        rows.append({"index": index, "labels": [scalar(key)], "cells": cells})
    return _derived(table, "group-by", [[by]], leaf_paths, rows)


def _aggregate_table(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    cells = []
    leaf_paths = []
    for item in spec.get("aggregations", []):
        values = _numbers(table["rows"], _data_index(table, item["column"]))
        cells.append(scalar(_aggregate(item["function"], values)))
        leaf_paths.append([item.get("as") or f"{item['function']} {item['column']}"])
    return _derived(table, "aggregate", [], leaf_paths, [{"index": 0, "labels": [], "cells": cells}])


def _filter(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    column = spec["column"]
    rows = []
    for row in table["rows"]:
        candidates = _row_label_values(table, row, column) or [_column_value(table, row, column)]
        keep = True
        if "equals" in spec:
            keep = any(value == str(spec["equals"]) for value in candidates)
        if "contains" in spec:
            keep = any(str(spec["contains"]) in value for value in candidates)
        if keep:
            new_row = dict(row)
            new_row["index"] = len(rows)
            rows.append(new_row)
    return _derived(table, "filter", [column["path"] for column in table["row_header_columns"]], table["schema_fingerprint"]["leaf_column_paths"], rows)


def _sort(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    reverse = spec.get("direction", "asc") == "desc"
    rows = sorted(table["rows"], key=lambda row: _column_value(table, row, spec["column"]), reverse=reverse)
    for index, row in enumerate(rows):
        row["index"] = index
    return _derived(table, "sort", [column["path"] for column in table["row_header_columns"]], table["schema_fingerprint"]["leaf_column_paths"], rows)


def _reorder_rename(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    rows = []
    leaf_paths = []
    selections = []
    for item in spec["columns"]:
        index = _data_index(table, item["from"])
        selections.append(index)
        leaf_paths.append([item.get("to") or item["from"]])
    for row in table["rows"]:
        rows.append({"index": len(rows), "labels": row["labels"], "cells": [row["cells"][index] for index in selections]})
    return _derived(table, "reorder-rename", [column["path"] for column in table["row_header_columns"]], leaf_paths, rows)


def _split_list_cell(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    output = clone_table(table)
    index = _data_index(output, spec["column"])
    delimiter = spec.get("delimiter", ";")
    for row in output["rows"]:
        cell = row["cells"][index]
        if isinstance(cell, dict) and cell.get("kind") == "scalar":
            parts = [part.strip() for part in str(cell.get("value", "")).split(delimiter) if part.strip()]
            row["cells"][index] = {"kind": "list", "ordered": False, "items": [scalar(part) for part in parts]}
    return output


def _promote(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    level = int(spec.get("level", 0))
    output = clone_table(table)
    output["schema_fingerprint"]["leaf_column_paths"] = [
        path[level:] if len(path) > level else path for path in output["schema_fingerprint"]["leaf_column_paths"]
    ]
    from .model import rebuild_schema

    return rebuild_schema(output)


def _demote(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    label = spec["label"]
    output = clone_table(table)
    output["schema_fingerprint"]["leaf_column_paths"] = [[label, *path] for path in output["schema_fingerprint"]["leaf_column_paths"]]
    from .model import rebuild_schema

    return rebuild_schema(output)


def _flatten_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, dict) and value.get("kind") in {"list", "rich_text", "table"}:
        return scalar(cell_to_text(value))
    return value


def _flatten(table: dict[str, Any], op: str) -> dict[str, Any]:
    output = clone_table(table)
    for row in output["rows"]:
        row["labels"] = [_flatten_value(label) for label in row["labels"]]
        row["cells"] = [_flatten_value(cell) for cell in row["cells"]]
    output["spans"] = [] if op == "flatten" else output["spans"]
    return output


def transform_table(table: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    validate_table_model(table)
    op = spec["op"]
    if op == "transpose":
        return _transpose(table)
    if op == "group-by":
        return _group_by(table, spec)
    if op == "aggregate":
        return _aggregate_table(table, spec)
    if op == "filter":
        return _filter(table, spec)
    if op == "sort":
        return _sort(clone_table(table), spec)
    if op == "reorder-rename":
        return _reorder_rename(table, spec)
    if op == "split-list-cell":
        return _split_list_cell(table, spec)
    if op == "promote-header-level":
        return _promote(table, spec)
    if op == "demote-header-level":
        return _demote(table, spec)
    if op in {"flatten", "unnest"}:
        return _flatten(table, op)
    raise ValueError(f"Unknown transform op: {op}")
