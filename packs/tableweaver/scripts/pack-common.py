from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


def read_args() -> dict[str, Any]:
    env_args = json.loads(os.environ.get("BRIDLE_PACK_ARGS_JSON", "{}"))
    argv = sys.argv[1:]
    cli_args: dict[str, Any] = {}
    index = 0
    while index < len(argv):
        arg = argv[index]
        if not arg.startswith("--"):
            raise SystemExit(f"Unexpected positional argument: {arg}")
        key = arg[2:].replace("-", "_")
        if "=" in key:
            key, value = key.split("=", 1)
        else:
            index += 1
            if index >= len(argv):
                value = "true"
            else:
                value = argv[index]
        try:
            cli_args[key] = json.loads(value)
        except json.JSONDecodeError:
            cli_args[key] = value
        index += 1
    return {**env_args, **cli_args}


def read_json_arg(args: dict[str, Any], key: str) -> Any:
    path_key = f"{key}_path"
    if isinstance(args.get(path_key), str):
        return json.loads(Path(args[path_key]).read_text())
    if key in args:
        return args[key]
    raise SystemExit(f"{key} or {path_key} is required")


def write_or_print(text: str, output_path: str | None) -> None:
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(text)
    else:
        print(text, end="")
