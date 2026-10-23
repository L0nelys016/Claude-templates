#!/usr/bin/env python3
"""Build dist/claude-templates.py: setup.py with every template embedded, so one file is enough."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_LINE = 'ROOT = Path(__file__).resolve().parent / "templates"  # build.py swaps this line in the bundle'

SHIM = '''import atexit as _atexit, json as _json, shutil as _shutil, tempfile as _tempfile

_DATA = _json.loads(%r)


def _materialize():
    d = _tempfile.mkdtemp(prefix="claude-templates-")
    _atexit.register(_shutil.rmtree, d, ignore_errors=True)
    for rel, text in _DATA.items():
        p = Path(d) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    return Path(d)


ROOT = _materialize()
'''


def bundle():
    data = {
        p.relative_to(HERE / "templates").as_posix(): p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        for p in sorted((HERE / "templates").rglob("*")) if p.is_file()
    }
    src = (HERE / "setup.py").read_text(encoding="utf-8")
    if ROOT_LINE not in src:
        sys.exit("error: ROOT line in setup.py changed; update ROOT_LINE in build.py")
    return src.replace(ROOT_LINE, SHIM % json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    dist = HERE / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / "claude-templates.py"
    target.write_bytes(bundle().encode("utf-8"))
    print(f"built {target} ({target.stat().st_size // 1024} KiB)")
