from fixtures import COMPLEX_HTML
from tableweaver.capture_html import capture_html
from tableweaver.transform import transform_table


def base_table():
    return capture_html(COMPLEX_HTML, source="inline://test")[0]


def test_transpose_swaps_rows_and_columns():
    transformed = transform_table(base_table(), {"op": "transpose"})

    assert transformed["schema_fingerprint"]["leaf_column_paths"][0] == ["Collection A / Letters"]
    assert transformed["rows"][0]["labels"][0]["value"] == "Metrics / Count"


def test_group_by_and_aggregate_sum():
    transformed = transform_table(base_table(), {
        "op": "group-by",
        "by": "Archive labels",
        "aggregations": [{"column": "Metrics / Count", "function": "sum", "as": "Total count"}],
    })

    assert transformed["schema_fingerprint"]["leaf_column_paths"] == [["Total count"]]
    assert transformed["rows"][0]["labels"][0]["value"] == "Collection A"
    assert transformed["rows"][0]["cells"][0]["value"] == 12


def test_aggregate_avg_count_min_max():
    transformed = transform_table(base_table(), {
        "op": "aggregate",
        "aggregations": [
            {"column": "Metrics / Count", "function": "avg", "as": "Average count"},
            {"column": "Metrics / Count", "function": "count", "as": "Rows with count"},
            {"column": "Metrics / Count", "function": "min", "as": "Min count"},
            {"column": "Metrics / Count", "function": "max", "as": "Max count"},
        ],
    })

    assert transformed["rows"][0]["cells"][0]["value"] == 12
    assert transformed["rows"][0]["cells"][1]["value"] == 1
    assert transformed["rows"][0]["cells"][2]["value"] == 12
    assert transformed["rows"][0]["cells"][3]["value"] == 12


def test_filter_sort_reorder_and_rename_columns():
    filtered = transform_table(base_table(), {"op": "filter", "column": "Archive labels", "equals": "Reports"})
    sorted_table = transform_table(filtered, {"op": "sort", "column": "Metrics / Share", "direction": "desc"})
    transformed = transform_table(sorted_table, {
        "op": "reorder-rename",
        "columns": [
            {"from": "Notes", "to": "Evidence"},
            {"from": "Metrics / Count", "to": "Count"},
        ],
    })

    assert len(transformed["rows"]) == 1
    assert transformed["schema_fingerprint"]["leaf_column_paths"] == [["Evidence"], ["Count"]]


def test_split_list_cell_on_delimiter():
    table = base_table()
    table["rows"][0]["cells"][2] = {"kind": "scalar", "value": "catalogued; needs review", "data_type": "string"}

    transformed = transform_table(table, {"op": "split-list-cell", "column": "Notes", "delimiter": ";"})

    assert transformed["rows"][0]["cells"][2]["kind"] == "list"
    assert [item["value"] for item in transformed["rows"][0]["cells"][2]["items"]] == ["catalogued", "needs review"]


def test_promote_and_demote_header_level():
    promoted = transform_table(base_table(), {"op": "promote-header-level", "level": 1})
    demoted = transform_table(promoted, {"op": "demote-header-level", "label": "Restored"})

    assert promoted["schema_fingerprint"]["leaf_column_paths"][0] == ["Count"]
    assert demoted["schema_fingerprint"]["leaf_column_paths"][0] == ["Restored", "Count"]


def test_flatten_and_unnest_remove_rich_cell_structure():
    flattened = transform_table(base_table(), {"op": "flatten"})
    unnested = transform_table(base_table(), {"op": "unnest"})

    assert flattened["rows"][0]["cells"][2]["kind"] == "scalar"
    assert "catalogued; needs review" == flattened["rows"][0]["cells"][2]["value"]
    assert unnested["rows"][1]["cells"][2]["kind"] == "scalar"
    assert "quality | high" in unnested["rows"][1]["cells"][2]["value"]
