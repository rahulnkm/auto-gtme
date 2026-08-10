import json
from gtme_linkedin.format import to_json, to_jsonl, error_line


def test_to_json_compact_single_object():
    assert to_json({"a": 1}) == '{"a": 1}'


def test_to_jsonl_one_record_per_line():
    out = to_jsonl([{"a": 1}, {"b": 2}])
    lines = out.splitlines()
    assert [json.loads(line) for line in lines] == [{"a": 1}, {"b": 2}]


def test_error_line_is_single_json_line():
    line = error_line({"error": "x", "input": "y", "suggestion": "z"})
    assert "\n" not in line
    assert json.loads(line)["error"] == "x"
