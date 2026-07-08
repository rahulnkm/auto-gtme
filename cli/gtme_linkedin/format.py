import json


def to_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def to_jsonl(items) -> str:
    return "\n".join(json.dumps(item, ensure_ascii=False) for item in items)


def error_line(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)
