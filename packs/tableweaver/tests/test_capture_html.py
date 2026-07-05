import json
from pathlib import Path

from fixtures import COMPLEX_HTML
from tableweaver.capture_html import capture_html
from tableweaver.validate import validate_table_model


def test_capture_preserves_multi_level_headers_and_row_labels():
    tables = capture_html(COMPLEX_HTML, source="inline://test")

    assert len(tables) == 1
    table = tables[0]
    validate_table_model(table)

    assert table["title"] == "Synthetic Archive Table"
    assert table["row_header_columns"] == [
        {"index": 0, "path": ["Archive labels"]},
        {"index": 1, "path": ["Archive labels"]},
    ]
    assert table["schema_fingerprint"]["leaf_column_paths"] == [
        ["Metrics", "Count"],
        ["Metrics", "Share"],
        ["Notes"],
    ]


def test_capture_records_rowspan_and_colspan_as_spans_not_flattened():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]

    spans = {(span["section"], span["row_start"], span["col_start"], span["rowspan"], span["colspan"], span["text"]) for span in table["spans"]}
    assert ("header", 0, 0, 2, 2, "Archive labels") in spans
    assert ("header", 0, 2, 1, 2, "Metrics") in spans
    assert ("body", 1, 2, 1, 2, "Merged metric pending") in spans
    assert table["rows"][1]["cells"][0]["value"] == "Merged metric pending"
    assert table["rows"][1]["cells"][1] is None


def test_capture_preserves_list_cells_and_nested_tables():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]

    list_cell = table["rows"][0]["cells"][2]
    assert list_cell == {
        "kind": "list",
        "ordered": False,
        "items": [
            {"kind": "scalar", "value": "catalogued", "data_type": "string"},
            {"kind": "scalar", "value": "needs review", "data_type": "string"},
        ],
    }

    nested_cell = table["rows"][1]["cells"][2]
    assert nested_cell["kind"] == "table"
    assert nested_cell["table"]["schema_fingerprint"]["leaf_column_paths"] == [["Flag"], ["Value"]]
    assert nested_cell["table"]["rows"][0]["cells"][1]["value"] == "high"


def test_capture_reads_local_html_files(tmp_path: Path):
    html_path = tmp_path / "fixture.html"
    html_path.write_text(COMPLEX_HTML)

    tables = capture_html(html_path, source=str(html_path))

    assert tables[0]["provenance"]["source"] == str(html_path)
    assert tables[0]["provenance"]["capture_method"] == "capture-html"
