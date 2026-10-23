import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import setup as s  # noqa: E402


def run(target, **kw):
    args = dict(stacks=["unity"], area="game", extras=[], forge="github", force=False)
    args.update(kw)
    acts, notes = s.build(target, args["stacks"], args["area"], args["extras"], args["forge"], args["force"])
    s.apply(acts)
    return acts, notes


class SetupTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.t = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_unity_implies_csharp_and_area(self):
        run(self.t)
        claude = (self.t / "CLAUDE.md").read_text(encoding="utf-8")
        for needle in ("Core principles", "C# / .NET", "Unity", "Area: Game", "# Что сделано"):
            self.assertIn(needle, claude)
        self.assertNotIn("Node.js", claude)
        self.assertIn("Review levels", (self.t / "REVIEW.md").read_text(encoding="utf-8"))

    def test_rerun_is_idempotent_and_keeps_user_text(self):
        (self.t / "CLAUDE.md").write_text("my own rules\n", encoding="utf-8")
        run(self.t)
        first = (self.t / "CLAUDE.md").read_text(encoding="utf-8")
        run(self.t)
        self.assertEqual(first, (self.t / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertTrue(first.startswith("my own rules"))

    def test_settings_merge_keeps_existing_keys(self):
        p = self.t / ".claude" / "settings.json"
        p.parent.mkdir()
        p.write_text(json.dumps({"model": "x", "permissions": {"deny": ["Bash(rm *)"]}}), encoding="utf-8")
        run(self.t, extras=["settings"])
        data = json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(data["model"], "x")
        self.assertIn("Bash(rm *)", data["permissions"]["deny"])
        self.assertIn("Bash(git push -f*)", data["permissions"]["deny"])
        self.assertEqual(data["attribution"], {"commit": "", "pr": ""})

    def test_hooks_depend_on_stack_and_both_forges(self):
        run(self.t, stacks=["react"], extras=["commitlint", "pr"], forge="both")
        for rel in (".husky/commit-msg", "commitlint.config.mjs", ".github/pull_request_template.md", ".gitea/pull_request_template.md"):
            self.assertTrue((self.t / rel).exists(), rel)
        other = self.t / "unity"
        other.mkdir()
        run(other, extras=["commitlint"])
        self.assertTrue((other / ".githooks" / "commit-msg").exists())

    def test_existing_extra_skipped_without_force(self):
        (self.t / ".editorconfig").write_text("mine\n", encoding="utf-8")
        acts, _ = run(self.t, extras=["editorconfig"])
        self.assertEqual((self.t / ".editorconfig").read_text(encoding="utf-8"), "mine\n")
        self.assertTrue(any(how.startswith("skip") for _, _, how in acts))

    def test_parse_list(self):
        self.assertEqual(s.parse_list("1, unity", s.STACKS), ["csharp", "unity"])
        self.assertEqual(s.parse_list("all", s.EXTRAS), s.EXTRAS)
        with self.assertRaises(ValueError):
            s.parse_list("cobol", s.STACKS)


if __name__ == "__main__":
    unittest.main()
