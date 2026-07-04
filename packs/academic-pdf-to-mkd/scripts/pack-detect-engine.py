import json
import runpy
import sys
from pathlib import Path


def main() -> int:
    env_args = json.loads(__import__("os").environ.get("BRIDLE_PACK_ARGS_JSON", "{}"))
    input_pdf = env_args.get("input_pdf")
    if not isinstance(input_pdf, str):
        print("input_pdf is a required string argument", file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    target = script_dir / "detect-engine.py"
    sys.argv = [str(target), input_pdf]
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
