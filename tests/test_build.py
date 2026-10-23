import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402


class BuildTest(unittest.TestCase):
    def test_bundle_matches_setup_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            bundle = tmp / "claude-templates.py"
            bundle.write_bytes(build.bundle().encode("utf-8"))
            outs = []
            for script in (HERE / "setup.py", bundle):
                t = tmp / script.stem
                t.mkdir()
                args = [sys.executable, "-I", str(script), "--target", str(t), "--stacks", "unity,react",
                        "--area", "game", "--extras", "all", "--forge", "both", "--yes"]
                subprocess.run(args, check=True, capture_output=True)
                outs.append({p.relative_to(t).as_posix(): p.read_bytes() for p in t.rglob("*") if p.is_file()})
            self.assertEqual(outs[0], outs[1])
            self.assertIn(".github/pull_request_template.md", outs[0])

    def test_bundle_has_no_templates_dir_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp) / "c.py"
            bundle.write_bytes(build.bundle().encode("utf-8"))
            r = subprocess.run([sys.executable, "-I", str(bundle), "--version"], check=True, capture_output=True, text=True)
            self.assertIn("claude-templates 0.1.0", r.stdout)


if __name__ == "__main__":
    unittest.main()
