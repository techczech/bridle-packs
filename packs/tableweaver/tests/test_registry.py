import json

from fixtures import COMPLEX_HTML
from tableweaver.capture_html import capture_html
from tableweaver.model import make_table, scalar
from tableweaver.registry import analyse, query, read_registry_document, register


def complex_table():
    return capture_html(COMPLEX_HTML, source="inline://registry/complex")[0]


def simple_table():
    return make_table(
        title="Simple Archive Metrics",
        source="inline://registry/simple",
        capture_method="manual-test",
        row_header_paths=[["Archive labels"]],
        leaf_column_paths=[["Metrics", "Count"], ["Status"]],
        rows=[
            {
                "index": 0,
                "labels": [scalar("Collection B")],
                "cells": [scalar(7), scalar("catalogued")],
            },
            {
                "index": 1,
                "labels": [scalar("Collection C")],
                "cells": [scalar(5), scalar("needs review")],
            },
        ],
        captured_at="2026-07-05T00:00:00Z",
        table_id="tbl_simple_registry",
    )


def test_register_creates_okf_document_and_idempotently_updates_indexes(tmp_path):
    table = complex_table()

    first = register(tmp_path, table, tags=["archive", "phase2"])
    updated_table = {**table, "title": "Updated Synthetic Archive Table"}
    second = register(tmp_path, updated_table, tags=["archive", "updated"])

    assert first["id"] == second["id"] == table["id"]
    assert first["path"] == second["path"]
    assert len(list((tmp_path / "tables").glob("*.md"))) == 1

    index = json.loads((tmp_path / "_index.json").read_text())
    entry = index["tables"][table["id"]]
    assert entry["frontmatter"]["title"] == "Updated Synthetic Archive Table"
    assert entry["frontmatter"]["tags"] == ["archive", "updated"]
    assert entry["frontmatter"]["schema_fingerprint"] == table["schema_fingerprint"]["value"]
    assert entry["path"] == f"tables/{table['id']}.md"

    frontmatter, payload = read_registry_document(tmp_path / entry["path"])
    assert frontmatter["type"] == "tableweaver.tablemodel"
    assert payload == updated_table

    human_index = (tmp_path / "_INDEX-registry.md").read_text()
    assert "Updated Synthetic Archive Table" in human_index
    assert table["id"] in human_index
    assert "Metrics / Count" in human_index


def test_query_filters_by_schema_column_provenance_tag_and_content(tmp_path):
    first = register(tmp_path, complex_table(), tags=["archive", "complex"])
    second = register(tmp_path, simple_table(), tags=["archive", "simple"])

    by_exact_schema = query(tmp_path, {"schema_fingerprint": first["frontmatter"]["schema_fingerprint"]})
    assert [match["id"] for match in by_exact_schema["matches"]] == [first["id"]]

    by_overlap_schema = query(
        tmp_path,
        {
            "schema_fingerprint": [["Metrics", "Count"]],
            "schema_match": "overlap",
        },
    )
    assert {match["id"] for match in by_overlap_schema["matches"]} == {first["id"], second["id"]}

    by_column_name = query(tmp_path, {"column_name": "Status"})
    assert [match["id"] for match in by_column_name["matches"]] == [second["id"]]

    by_column_type = query(tmp_path, {"column": {"name": "Metrics / Count", "type": "integer"}})
    assert {match["id"] for match in by_column_type["matches"]} == {first["id"], second["id"]}

    by_source = query(tmp_path, {"provenance_source": "inline://registry/simple"})
    assert [match["id"] for match in by_source["matches"]] == [second["id"]]

    by_tag = query(tmp_path, {"tag": "complex"})
    assert [match["id"] for match in by_tag["matches"]] == [first["id"]]

    by_content = query(tmp_path, {"content": "needs review"})
    assert {match["id"] for match in by_content["matches"]} == {first["id"], second["id"]}


def test_analyse_surfaces_overlap_frequency_distribution_and_stats(tmp_path):
    complex_entry = register(tmp_path, complex_table(), tags=["archive", "complex"])
    simple_entry = register(tmp_path, simple_table(), tags=["archive", "simple"])

    report = analyse(tmp_path, column="Metrics / Count")

    overlap_groups = report["schema_overlap"]["overlapping_columns"]
    assert any(set(group["table_ids"]) == {complex_entry["id"], simple_entry["id"]} for group in overlap_groups)

    count_frequency = report["column_frequency"]["Metrics / Count"]
    assert count_frequency["table_count"] == 2
    assert set(count_frequency["table_ids"]) == {complex_entry["id"], simple_entry["id"]}

    distribution = report["value_distribution"]["Metrics / Count"]
    assert distribution["values"]["12"]["count"] == 1
    assert distribution["values"]["7"]["count"] == 1
    assert distribution["values"]["5"]["count"] == 1

    assert report["corpus_stats"]["table_count"] == 2
    assert report["corpus_stats"]["total_leaf_columns"] == 5
    assert report["corpus_stats"]["provenance_breakdown"]["capture-html"] == 1
    assert report["corpus_stats"]["provenance_breakdown"]["manual-test"] == 1
    assert report["corpus_stats"]["duplicate_ids"] == []
