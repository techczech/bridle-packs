import json
import re
import runpy
import sys
from pathlib import Path


def paper_id_from_pdf(path: str) -> str:
    stem = Path(path).stem.lower().replace(" ", "-")
    cleaned = re.sub(r"[^a-z0-9_-]", "", stem)
    return cleaned or "paper"


def main() -> int:
    raw_args = json.loads(Path("/dev/stdin").read_text() if False else "{}")
    env_args = json.loads(__import__("os").environ.get("BRIDLE_PACK_ARGS_JSON", "{}"))
    args = {**raw_args, **env_args}

    input_pdf = args.get("input_pdf")
    output_dir = args.get("output_dir")
    if not isinstance(input_pdf, str) or not isinstance(output_dir, str):
        print("input_pdf and output_dir are required string arguments", file=sys.stderr)
        return 2

    paper_id = args.get("paper_id")
    if not isinstance(paper_id, str) or not paper_id:
        paper_id = paper_id_from_pdf(input_pdf)

    script_dir = Path(__file__).resolve().parent
    target = script_dir / "docling-extract.py"
    sys.argv = [str(target), input_pdf, output_dir, paper_id]
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
