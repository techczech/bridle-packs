from __future__ import annotations

from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, Tag

from .model import make_table, scalar, stable_id


def _direct_rows(parent: Tag) -> list[Tag]:
    return [row for row in parent.find_all("tr", recursive=False)]


def _direct_cells(row: Tag) -> list[Tag]:
    return [cell for cell in row.find_all(["th", "td"], recursive=False)]


def _cell_text(cell: Tag) -> str:
    clone = BeautifulSoup(str(cell), "lxml")
    for nested in clone.find_all("table"):
        nested.decompose()
    return " ".join(clone.get_text(" ", strip=True).split())


def _cell_value(cell: Tag, source: str, captured_at: str | None) -> dict[str, Any]:
    nested = cell.find("table")
    if isinstance(nested, Tag):
        return {"kind": "table", "table": _capture_table(nested, source=source, captured_at=captured_at, ordinal=0)}

    direct_lists = [child for child in cell.find_all(["ul", "ol"], recursive=False)]
    text_without_lists = BeautifulSoup(str(cell), "lxml")
    for list_tag in text_without_lists.find_all(["ul", "ol"]):
        list_tag.decompose()
    remaining_text = " ".join(text_without_lists.get_text(" ", strip=True).split())
    if len(direct_lists) == 1 and not remaining_text:
        list_tag = direct_lists[0]
        return {
            "kind": "list",
            "ordered": list_tag.name == "ol",
            "items": [scalar(_cell_text(item)) for item in list_tag.find_all("li", recursive=False)],
        }
    if direct_lists:
        blocks: list[dict[str, Any]] = []
        if remaining_text:
            blocks.append({"type": "paragraph", "text": remaining_text})
        for list_tag in direct_lists:
            blocks.append({
                "type": "numbered_list" if list_tag.name == "ol" else "bullet_list",
                "items": [_cell_text(item) for item in list_tag.find_all("li", recursive=False)],
            })
        return {"kind": "rich_text", "blocks": blocks}

    return scalar(_cell_text(cell))


def _leading_th_count(row: Tag) -> int:
    count = 0
    for cell in _direct_cells(row):
        if cell.name != "th":
            break
        count += int(cell.get("colspan", 1))
    return count


def _parse_grid(rows: list[Tag], section: str, source: str, captured_at: str | None) -> tuple[list[list[dict[str, Any] | None]], list[dict[str, Any]]]:
    grid: list[list[dict[str, Any] | None]] = []
    spans: list[dict[str, Any]] = []
    occupied: dict[tuple[int, int], dict[str, Any]] = {}
    for row_index, row in enumerate(rows):
        grid_row: list[dict[str, Any] | None] = []
        col_index = 0
        for cell in _direct_cells(row):
            while (row_index, col_index) in occupied:
                grid_row.append(occupied[(row_index, col_index)])
                col_index += 1
            rowspan = int(cell.get("rowspan", 1))
            colspan = int(cell.get("colspan", 1))
            text = _cell_text(cell)
            entry = {
                "id": stable_id(section, row_index, col_index, text),
                "tag": cell.name,
                "text": text,
                "value": _cell_value(cell, source, captured_at),
                "row": row_index,
                "col": col_index,
                "rowspan": rowspan,
                "colspan": colspan,
            }
            for delta_col in range(colspan):
                grid_row.append(entry)
                if delta_col > 0:
                    occupied[(row_index, col_index + delta_col)] = entry
            for delta_row in range(1, rowspan):
                for delta_col in range(colspan):
                    occupied[(row_index + delta_row, col_index + delta_col)] = entry
            if rowspan > 1 or colspan > 1:
                spans.append({
                    "id": entry["id"],
                    "section": section,
                    "row_start": row_index,
                    "col_start": col_index,
                    "rowspan": rowspan,
                    "colspan": colspan,
                    "text": text,
                })
            col_index += colspan
        while (row_index, col_index) in occupied:
            grid_row.append(occupied[(row_index, col_index)])
            col_index += 1
        grid.append(grid_row)
    width = max((len(row) for row in grid), default=0)
    for row in grid:
        row.extend([None] * (width - len(row)))
    return grid, spans


def _header_and_body_rows(table: Tag) -> tuple[list[Tag], list[Tag]]:
    thead = table.find("thead", recursive=False)
    if isinstance(thead, Tag):
        header_rows = _direct_rows(thead)
        body_rows: list[Tag] = []
        tbodies = table.find_all("tbody", recursive=False)
        for tbody in tbodies:
            body_rows.extend(_direct_rows(tbody))
        if not body_rows:
            body_rows = [row for row in _direct_rows(table) if row not in header_rows]
        return header_rows, body_rows

    direct = _direct_rows(table)
    header_rows = []
    for row in direct:
        cells = _direct_cells(row)
        if cells and all(cell.name == "th" for cell in cells):
            header_rows.append(row)
        else:
            break
    return header_rows, direct[len(header_rows):]


def _paths_for_columns(header_grid: list[list[dict[str, Any] | None]], start: int, width: int) -> list[list[str]]:
    paths: list[list[str]] = []
    for col in range(start, width):
        path: list[str] = []
        seen: set[str] = set()
        for row in header_grid:
            entry = row[col] if col < len(row) else None
            if not entry or not entry["text"] or entry["id"] in seen:
                continue
            seen.add(entry["id"])
            path.append(entry["text"])
        paths.append(path or [f"Column {col - start + 1}"])
    return paths


def _column_levels(header_grid: list[list[dict[str, Any] | None]], leaf_paths: list[list[str]], row_header_count: int) -> list[dict[str, Any]]:
    levels: list[dict[str, Any]] = []
    for level, row in enumerate(header_grid):
        cells = []
        seen: set[str] = set()
        for entry in row:
            if not entry or entry["id"] in seen:
                continue
            seen.add(entry["id"])
            if entry["col"] < row_header_count:
                scope = "row_header"
            elif entry["colspan"] > 1 or entry["rowspan"] > 1:
                scope = "column_group"
            else:
                scope = "column"
            cells.append({
                "id": entry["id"],
                "text": entry["text"],
                "row": entry["row"],
                "col_start": entry["col"],
                "rowspan": entry["rowspan"],
                "colspan": entry["colspan"],
                "scope": scope,
            })
        levels.append({"level": level, "cells": cells})
    return levels


def _capture_table(table: Tag, source: str, captured_at: str | None, ordinal: int) -> dict[str, Any]:
    header_rows, body_rows = _header_and_body_rows(table)
    header_grid, header_spans = _parse_grid(header_rows, "header", source, captured_at)
    body_grid, body_spans = _parse_grid(body_rows, "body", source, captured_at)
    row_header_count = max((_leading_th_count(row) for row in body_rows), default=0)
    width = max([row_header_count, *(len(row) for row in header_grid), *(len(row) for row in body_grid)], default=0)

    row_header_paths = _paths_for_columns(header_grid, 0, row_header_count)
    leaf_paths = _paths_for_columns(header_grid, row_header_count, width)
    columns = _column_levels(header_grid, leaf_paths, row_header_count)
    rows: list[dict[str, Any]] = []
    for row_index, grid_row in enumerate(body_grid):
        labels = []
        cells = []
        for col in range(row_header_count):
            entry = grid_row[col] if col < len(grid_row) else None
            labels.append(entry["value"] if entry else scalar(""))
        for col in range(row_header_count, width):
            entry = grid_row[col] if col < len(grid_row) else None
            if entry is None:
                cells.append(None)
            elif entry["row"] == row_index and entry["col"] == col:
                cells.append(entry["value"])
            else:
                cells.append(None)
        rows.append({"index": row_index, "labels": labels, "cells": cells})

    caption = table.find("caption", recursive=False)
    title = _cell_text(caption) if isinstance(caption, Tag) else str(table.get("data-title", f"Table {ordinal + 1}"))
    return make_table(
        title=title,
        source=source,
        capture_method="capture-html",
        row_header_paths=row_header_paths,
        leaf_column_paths=leaf_paths,
        rows=rows,
        spans=header_spans + body_spans,
        captured_at=captured_at,
        columns=columns,
    )


def capture_html(html_or_path: str | Path, *, source: str | None = None, captured_at: str | None = None) -> list[dict[str, Any]]:
    candidate = str(html_or_path)
    looks_like_html = "<table" in candidate.lower() or "<html" in candidate.lower()
    html_path = Path(candidate)
    if not looks_like_html and html_path.exists():
        html = html_path.read_text()
        source = source or str(html_path)
    else:
        html = candidate
        source = source or "inline-html"
    soup = BeautifulSoup(html, "lxml")
    tables = [table for table in soup.find_all("table") if not table.find_parent("table")]
    return [_capture_table(table, source=source, captured_at=captured_at, ordinal=index) for index, table in enumerate(tables)]
