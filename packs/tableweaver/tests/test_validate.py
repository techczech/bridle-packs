import pytest

from fixtures import COMPLEX_HTML
from tableweaver.capture_html import capture_html
from tableweaver.validate import TableModelValidationError, validate_table_model


def test_validate_accepts_captured_table_model():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]

    validate_table_model(table)


def test_validate_rejects_flattened_unknown_cell_values():
    table = capture_html(COMPLEX_HTML, source="inline://test")[0]
    table["rows"][0]["cells"][0] = "flattened"

    with pytest.raises(TableModelValidationError):
        validate_table_model(table)
