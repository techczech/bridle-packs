import json

from fixtures import COMPLEX_HTML
from tableweaver.capture_html import capture_html
from tableweaver.export import export_csv, export_json, export_markdown, export_tsv, load_table_model


def test_json_export_round_trips_losslessly():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]

    encoded = export_json(table)
    decoded = load_table_model(encoded)

    assert decoded == table


def test_markdown_export_keeps_header_paths_and_signals_nested_content():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]

    markdown = export_markdown(table)

    assert "| Archive labels | Archive labels | Metrics / Count | Metrics / Share | Notes |" in markdown
    assert "catalogued; needs review" in markdown
    assert "[nested table:" in markdown


def test_csv_export_is_lossy_and_documents_dropped_structure():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]

    csv_text, report = export_csv(table)

    assert "Archive labels,Archive labels,Metrics / Count,Metrics / Share,Notes" in csv_text
    assert "Merged metric pending" in csv_text
    assert report["format"] == "csv"
    assert {"kind": "span", "detail": "rowspan/colspan structure was projected to a rectangular export"} in report["losses"]
    assert any(loss["kind"] == "nested_table" for loss in report["losses"])
    assert any(loss["kind"] == "list_cell" for loss in report["losses"])


def test_tsv_export_uses_tabs_and_has_loss_report():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]

    tsv_text, report = export_tsv(table)

    assert "Archive labels\tArchive labels\tMetrics / Count" in tsv_text
    assert report["format"] == "tsv"
