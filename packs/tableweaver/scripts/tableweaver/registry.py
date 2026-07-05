from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .model import cell_to_text, path_label
from .validate import validate_table_model


INDEX_NAME = "_index.json"
HUMAN_INDEX_NAME = "_INDEX-registry.md"
TABLES_DIR = "tables"
REGISTRY_DOC_TYPE = "tableweaver.tablemodel"


def _json_line(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _parse_json_line(value: str) -> Any:
    return json.loads(value.strip())


def _column_records(table: dict[str, Any]) -> list[dict[str, Any]]:
    paths = table["schema_fingerprint"]["leaf_column_paths"]
    types = table["schema_fingerprint"]["types"]
    return [
        {
            "name": path_label(path),
            "path": path,
            "type": types[index] if index < len(types) else "unknown",
        }
        for index, path in enumerate(paths)
    ]


def _normalise_tags(tags: list[str] | str | None) -> list[str]:
    if tags is None:
        return []
    if isinstance(tags, str):
        return [tags]
    return [str(tag) for tag in tags]


def _frontmatter(table: dict[str, Any], tags: list[str] | str | None) -> dict[str, Any]:
    columns = _column_records(table)
    return {
        "type": REGISTRY_DOC_TYPE,
        "title": table["title"],
        "id": table["id"],
        "provenance": table["provenance"],
        "schema_fingerprint": table["schema_fingerprint"]["value"],
        "tags": sorted(dict.fromkeys(_normalise_tags(tags))),
        "column_leaf_paths": [column["name"] for column in columns],
        "column_leaf_path_vectors": [column["path"] for column in columns],
        "column_types": columns,
    }


def _encode_frontmatter(frontmatter: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in frontmatter.items():
        lines.append(f"{key}: {_json_line(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _decode_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("Registry document is missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Registry document frontmatter is not closed")
    frontmatter_text = text[4:end]
    body = text[end + len("\n---\n") :]
    frontmatter: dict[str, Any] = {}
    for line in frontmatter_text.splitlines():
        if not line.strip():
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = _parse_json_line(value)
    return frontmatter, body


def _registry_doc(frontmatter: dict[str, Any], table: dict[str, Any]) -> str:
    return _encode_frontmatter(frontmatter) + json.dumps(table, indent=2, sort_keys=True) + "\n"


def read_registry_document(path: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    frontmatter, body = _decode_frontmatter(Path(path).read_text())
    return frontmatter, json.loads(body)


def _empty_index() -> dict[str, Any]:
    return {"version": 1, "tables": {}}


def _load_index(registry_dir: str | Path) -> dict[str, Any]:
    index_path = Path(registry_dir) / INDEX_NAME
    if not index_path.exists():
        return _empty_index()
    index = json.loads(index_path.read_text())
    index.setdefault("version", 1)
    index.setdefault("tables", {})
    return index


def _write_index(registry_dir: Path, index: dict[str, Any]) -> None:
    ordered = {
        "version": index.get("version", 1),
        "tables": {
            table_id: index["tables"][table_id]
            for table_id in sorted(index.get("tables", {}))
        },
    }
    (registry_dir / INDEX_NAME).write_text(json.dumps(ordered, indent=2, sort_keys=True) + "\n")
    _write_human_index(registry_dir, ordered)


def _write_human_index(registry_dir: Path, index: dict[str, Any]) -> None:
    lines = [
        "# Tableweaver Registry Index",
        "",
        f"Tables: {len(index.get('tables', {}))}",
        "",
    ]
    for table_id, entry in index.get("tables", {}).items():
        frontmatter = entry["frontmatter"]
        lines.extend(
            [
                f"## {frontmatter['title']}",
                "",
                f"- id: `{table_id}`",
                f"- path: `{entry['path']}`",
                f"- schema_fingerprint: `{frontmatter['schema_fingerprint']}`",
                f"- provenance: `{frontmatter['provenance'].get('source', '')}`",
                f"- tags: {', '.join(frontmatter.get('tags', [])) or '(none)'}",
                f"- columns: {', '.join(frontmatter.get('column_leaf_paths', [])) or '(none)'}",
                "",
            ]
        )
    (registry_dir / HUMAN_INDEX_NAME).write_text("\n".join(lines).rstrip() + "\n")


def register(registry_dir: str | Path, table_model: dict[str, Any], tags: list[str] | str | None = None) -> dict[str, Any]:
    validate_table_model(table_model)
    registry_path = Path(registry_dir)
    tables_path = registry_path / TABLES_DIR
    tables_path.mkdir(parents=True, exist_ok=True)

    frontmatter = _frontmatter(table_model, tags)
    relative_path = Path(TABLES_DIR) / f"{table_model['id']}.md"
    document_path = registry_path / relative_path
    document_path.write_text(_registry_doc(frontmatter, table_model))

    index = _load_index(registry_path)
    index["tables"][table_model["id"]] = {
        "frontmatter": frontmatter,
        "path": relative_path.as_posix(),
    }
    _write_index(registry_path, index)
    return {"id": table_model["id"], "path": relative_path.as_posix(), "frontmatter": frontmatter}


def _normalise_column_name(value: str) -> str:
    return value.strip().casefold()


def _schema_filter_paths(value: Any) -> set[tuple[str, ...]]:
    if not isinstance(value, list):
        return set()
    paths: set[tuple[str, ...]] = set()
    for item in value:
        if isinstance(item, list):
            paths.add(tuple(str(part) for part in item))
        elif isinstance(item, str):
            paths.add(tuple(part.strip() for part in item.split("/") if part.strip()))
    return paths


def _has_column(frontmatter: dict[str, Any], name: str | None = None, type_name: str | None = None) -> bool:
    wanted_name = _normalise_column_name(name) if name else None
    wanted_type = type_name.strip().casefold() if type_name else None
    for column in frontmatter.get("column_types", []):
        name_matches = wanted_name is None or _normalise_column_name(column["name"]) == wanted_name
        type_matches = wanted_type is None or str(column["type"]).casefold() == wanted_type
        if name_matches and type_matches:
            return True
    return False


def _entry_matches_frontmatter(entry: dict[str, Any], filters: dict[str, Any]) -> bool:
    frontmatter = entry["frontmatter"]
    schema_filter = filters.get("schema_fingerprint")
    if schema_filter is not None:
        schema_match = filters.get("schema_match", "exact")
        if schema_match == "overlap":
            wanted_paths = _schema_filter_paths(schema_filter)
            if not wanted_paths:
                wanted_paths = _schema_filter_paths(frontmatter.get("column_leaf_path_vectors", []))
            available = set(tuple(path) for path in frontmatter.get("column_leaf_path_vectors", []))
            if not wanted_paths.intersection(available):
                return False
        elif frontmatter.get("schema_fingerprint") != schema_filter:
            return False

    if filters.get("column_name") and not _has_column(frontmatter, name=str(filters["column_name"])):
        return False
    if filters.get("column_type") and not _has_column(frontmatter, type_name=str(filters["column_type"])):
        return False
    if isinstance(filters.get("column"), dict):
        column = filters["column"]
        if not _has_column(frontmatter, name=column.get("name"), type_name=column.get("type")):
            return False

    provenance_source = filters.get("provenance_source")
    if provenance_source and str(provenance_source) not in frontmatter.get("provenance", {}).get("source", ""):
        return False

    tag = filters.get("tag")
    if tag and str(tag) not in frontmatter.get("tags", []):
        return False

    return True


def _content_text(table: dict[str, Any]) -> str:
    chunks = [table.get("title", ""), json.dumps(table.get("provenance", {}), ensure_ascii=True, sort_keys=True)]
    for row in table.get("rows", []):
        chunks.extend(cell_to_text(label) for label in row.get("labels", []))
        chunks.extend(cell_to_text(cell) for cell in row.get("cells", []))
    return "\n".join(chunks)


def query(registry_dir: str | Path, filters: dict[str, Any] | None = None) -> dict[str, Any]:
    filters = filters or {}
    registry_path = Path(registry_dir)
    index = _load_index(registry_path)
    matches: list[dict[str, Any]] = []
    content_filter = filters.get("content")

    for table_id in sorted(index.get("tables", {})):
        entry = index["tables"][table_id]
        if not _entry_matches_frontmatter(entry, filters):
            continue
        if content_filter:
            _frontmatter, table = read_registry_document(registry_path / entry["path"])
            if str(content_filter).casefold() not in _content_text(table).casefold():
                continue
        matches.append({"id": table_id, "frontmatter": entry["frontmatter"], "path": entry["path"]})

    return {"count": len(matches), "matches": matches, "filter": filters}


def _column_index(table: dict[str, Any], column: str) -> int | None:
    wanted = _normalise_column_name(column)
    for index, path in enumerate(table["schema_fingerprint"]["leaf_column_paths"]):
        if _normalise_column_name(path_label(path)) == wanted:
            return index
    return None


def _connected_overlap_groups(table_columns: dict[str, set[str]]) -> list[dict[str, Any]]:
    remaining = set(table_columns)
    groups: list[dict[str, Any]] = []
    while remaining:
        seed = remaining.pop()
        component = {seed}
        changed = True
        while changed:
            changed = False
            for table_id in list(remaining):
                if any(table_columns[table_id].intersection(table_columns[known]) for known in component):
                    remaining.remove(table_id)
                    component.add(table_id)
                    changed = True
        if len(component) > 1:
            shared = set.intersection(*(table_columns[table_id] for table_id in component))
            groups.append(
                {
                    "table_ids": sorted(component),
                    "shared_columns": sorted(shared),
                }
            )
    return sorted(groups, key=lambda group: (len(group["table_ids"]), group["table_ids"]), reverse=True)


def analyse(registry_dir: str | Path, column: str | None = None) -> dict[str, Any]:
    registry_path = Path(registry_dir)
    index = _load_index(registry_path)
    tables: dict[str, dict[str, Any]] = {}
    for table_id, entry in index.get("tables", {}).items():
        _frontmatter, tables[table_id] = read_registry_document(registry_path / entry["path"])

    by_fingerprint: dict[str, list[str]] = defaultdict(list)
    table_columns: dict[str, set[str]] = {}
    column_frequency: dict[str, dict[str, Any]] = {}
    provenance_breakdown: Counter[str] = Counter()

    for table_id, entry in index.get("tables", {}).items():
        frontmatter = entry["frontmatter"]
        by_fingerprint[frontmatter["schema_fingerprint"]].append(table_id)
        table_columns[table_id] = set(frontmatter.get("column_leaf_paths", []))
        provenance_breakdown[frontmatter.get("provenance", {}).get("capture_method", "unknown")] += 1
        for column_name in frontmatter.get("column_leaf_paths", []):
            column_frequency.setdefault(column_name, {"table_count": 0, "table_ids": []})
            column_frequency[column_name]["table_count"] += 1
            column_frequency[column_name]["table_ids"].append(table_id)

    for value in column_frequency.values():
        value["table_ids"].sort()

    value_distribution: dict[str, Any] = {}
    if column:
        values: dict[str, dict[str, Any]] = {}
        for table_id, table in tables.items():
            index_for_column = _column_index(table, column)
            if index_for_column is None:
                continue
            for row in table.get("rows", []):
                if index_for_column >= len(row.get("cells", [])):
                    continue
                text = cell_to_text(row["cells"][index_for_column])
                values.setdefault(text, {"count": 0, "table_ids": []})
                values[text]["count"] += 1
                if table_id not in values[text]["table_ids"]:
                    values[text]["table_ids"].append(table_id)
        for value in values.values():
            value["table_ids"].sort()
        value_distribution[column] = {"values": dict(sorted(values.items()))}

    duplicate_ids = [
        table_id
        for table_id, count in Counter(entry["frontmatter"]["id"] for entry in index.get("tables", {}).values()).items()
        if count > 1
    ]
    same_fingerprint_groups = [
        {"schema_fingerprint": fingerprint, "table_ids": sorted(table_ids)}
        for fingerprint, table_ids in by_fingerprint.items()
        if len(table_ids) > 1
    ]

    return {
        "schema_overlap": {
            "same_fingerprint": sorted(same_fingerprint_groups, key=lambda group: group["schema_fingerprint"]),
            "overlapping_columns": _connected_overlap_groups(table_columns),
        },
        "column_frequency": dict(sorted(column_frequency.items())),
        "value_distribution": value_distribution,
        "corpus_stats": {
            "table_count": len(index.get("tables", {})),
            "total_leaf_columns": sum(len(columns) for columns in table_columns.values()),
            "unique_leaf_columns": len(set().union(*table_columns.values())) if table_columns else 0,
            "provenance_breakdown": dict(sorted(provenance_breakdown.items())),
            "duplicate_ids": sorted(duplicate_ids),
            "near_duplicate_fingerprints": same_fingerprint_groups,
        },
    }
