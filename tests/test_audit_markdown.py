"""Standard-library regression tests using real files and CLI subprocesses."""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_markdown.py"
SPEC = importlib.util.spec_from_file_location("audit_markdown", SCRIPT)
AUDITOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDITOR
SPEC.loader.exec_module(AUDITOR)

MODEL_LINK = "[模型](https://modelscope.cn/models/example/model)\n"
NORMAL = "# 模型发布\n\n" + MODEL_LINK


class AuditMarkdownTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.article = self.root / "article.txt"
        self.article.write_text(NORMAL, encoding="utf-8")

    def audit(self, text, **kwargs):
        self.article.write_text(text, encoding="utf-8")
        return AUDITOR.audit(self.article, **kwargs)

    def codes(self, text, **kwargs):
        return [item.code for item in self.audit(text, **kwargs)]

    def cli(self, *options, path=None):
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(path or self.article), *options],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def assert_report(self, result, *, failed_input=False):
        self.assertEqual(result.stderr, "")
        report = json.loads(result.stdout)
        self.assertEqual(set(report), {
            "article", "modelscope", "fail_on", "findings", "counts", "passed", "error", "notice",
        })
        self.assertEqual(report["article"], str(self.article))
        self.assertEqual(set(report["counts"]), {"blocker", "major", "minor"})
        for finding in report["findings"]:
            self.assertEqual(set(finding), {"severity", "line", "code", "message"})
            self.assertIn(finding["severity"], report["counts"])
            self.assertTrue(finding["line"] is None or isinstance(finding["line"], int))
            self.assertIsInstance(finding["code"], str)
            self.assertIsInstance(finding["message"], str)
        for severity, count in report["counts"].items():
            self.assertEqual(count, sum(item["severity"] == severity for item in report["findings"]))
        self.assertIn("severity threshold, not fact verification", report["notice"])
        self.assertIn("does not confirm listing status", report["notice"])
        if failed_input:
            self.assertIsNone(report["passed"])
            self.assertTrue(report["error"])
            self.assertEqual(report["findings"], [])
            self.assertEqual(result.returncode, 2)
        else:
            self.assertIsInstance(report["passed"], bool)
            self.assertIsNone(report["error"])
            self.assertEqual(result.returncode, 0 if report["passed"] else 1)
        return report

    def test_normal_article(self):
        self.assertEqual(self.audit(NORMAL), [])

    def test_normal_cli_defaults(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("Findings: 0 blocker, 0 major, 0 minor", result.stdout)
        self.assertIn("fail-on: blocker; modelscope: required", result.stdout)
        self.assertIn("not fact verification", result.stdout)

    def test_normal_json_structure_and_determinism(self):
        result = self.cli("--format", "json")
        report = self.assert_report(result)
        self.assertEqual(report["findings"], [])
        self.assertTrue(report["passed"])
        self.assertEqual(report["fail_on"], "blocker")
        self.assertEqual(report["modelscope"], "required")
        self.assertEqual(result.stdout, self.cli("--format", "json").stdout)

    def test_major_default_compatibility_and_thresholds(self):
        self.article.write_text(NORMAL + "最强\n", encoding="utf-8")
        for threshold, expected in ((None, 0), ("blocker", 0), ("major", 1), ("minor", 1)):
            for output in ("text", "json"):
                with self.subTest(threshold=threshold, output=output):
                    options = ["--format", output]
                    if threshold:
                        options.extend(("--fail-on", threshold))
                    result = self.cli(*options)
                    self.assertEqual(result.returncode, expected)
                    if output == "json":
                        report = self.assert_report(result)
                        self.assertEqual(report["counts"], {"blocker": 0, "major": 1, "minor": 0})
                        self.assertEqual(report["passed"], expected == 0)
                    else:
                        self.assertIn("[MAJOR] CLAIM_SCOPE", result.stdout)

    def test_minor_threshold(self):
        self.article.write_text(NORMAL + "震惊\n", encoding="utf-8")
        for threshold, expected in (("blocker", 0), ("major", 0), ("minor", 1)):
            with self.subTest(threshold=threshold):
                result = self.cli("--fail-on", threshold, "--format", "json")
                self.assertEqual(result.returncode, expected)
                self.assertEqual(self.assert_report(result)["counts"]["minor"], 1)

    def test_blocker_fails_every_threshold(self):
        self.article.write_text(NORMAL + "```python\n", encoding="utf-8")
        for threshold in ("blocker", "major", "minor"):
            with self.subTest(threshold=threshold):
                result = self.cli("--fail-on", threshold, "--format", "json")
                self.assertEqual(result.returncode, 1)
                self.assertEqual(self.assert_report(result)["counts"]["blocker"], 1)

    def test_required_and_optional_audit(self):
        text = "# 发布\n最强\n"
        required = self.audit(text)
        explicit = self.audit(text, modelscope="required")
        optional = self.audit(text, modelscope="optional")
        self.assertEqual(required, explicit)
        self.assertIn("MODELSCOPE", [item.code for item in required])
        self.assertEqual(optional, [item for item in required if item.code != "MODELSCOPE"])

    def test_required_and_optional_cli(self):
        self.article.write_text("# 发布\n", encoding="utf-8")
        for mode, expected in (("required", 1), ("optional", 0)):
            with self.subTest(mode=mode):
                result = self.cli("--modelscope", mode, "--fail-on", "major", "--format", "json")
                self.assertEqual(result.returncode, expected)
                report = self.assert_report(result)
                self.assertEqual(report["modelscope"], mode)
                self.assertEqual(report["counts"]["major"], expected)

    def test_optional_does_not_suppress_other_findings(self):
        self.article.write_text("# 发布\n最强\n", encoding="utf-8")
        result = self.cli("--modelscope", "optional", "--fail-on", "major", "--format", "json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual([item["code"] for item in self.assert_report(result)["findings"]], ["CLAIM_SCOPE"])

    def test_both_fence_characters_and_longer_closers(self):
        for marker in ("```", "~~~", "````", "~~~~"):
            for closing in (marker, marker + marker[0] * 2):
                with self.subTest(marker=marker, closing=closing):
                    self.assertEqual(self.audit(NORMAL + f"{marker}python\n最强 震惊\n{closing}\n"), [])

    def test_shorter_fence_cannot_close_long_fence(self):
        for marker in ("````", "~~~~"):
            with self.subTest(marker=marker):
                text = NORMAL + f"{marker}python\n{marker[:3]}\n最强\n{marker}\n震惊\n"
                findings = self.audit(text)
                self.assertEqual([(item.code, item.line) for item in findings], [("STYLE", 8)])

    def test_mismatched_characters_do_not_close_fence(self):
        for opening, wrong in (("```", "~~~"), ("~~~", "```")):
            with self.subTest(opening=opening):
                text = NORMAL + f"{opening}python\n{wrong}\n最强 震惊\n{opening}\n"
                self.assertEqual(self.audit(text), [])
                findings = self.audit(NORMAL + f"{opening}python\n{wrong}\n最强\n")
                self.assertEqual([(item.code, item.line) for item in findings], [("FENCE", 4)])

    def test_closing_fence_cannot_have_info_string(self):
        for marker in ("```", "~~~"):
            with self.subTest(marker=marker):
                findings = self.audit(NORMAL + f"{marker}python\n{marker}python\n最强\n")
                self.assertEqual([(item.code, item.line) for item in findings], [("FENCE", 4)])

    def test_unclosed_fence_suppresses_prose_until_eof(self):
        findings = self.audit(NORMAL + "~~~python\n# 示例标题\n最强 震惊\n支持 Transformer 架构\n")
        self.assertEqual([(item.code, item.line) for item in findings], [("FENCE", 4)])

    def test_code_language_and_length_checks_are_retained(self):
        for marker in ("```", "~~~", "````"):
            with self.subTest(marker=marker):
                findings = self.audit(NORMAL + marker + "\n" + "x = 1\n" * 31 + marker + "\n")
                self.assertEqual([(item.code, item.line) for item in findings], [("CODE_LANG", 4), ("CODE_LENGTH", 4)])
                self.assertEqual(self.codes(NORMAL + marker + "\n" + "x = 1\n" * 30 + marker + "\n"), ["CODE_LANG"])

    def test_code_prose_signals_are_ignored(self):
        content = (
            "# " + "长" * 70 + "\n"
            "## 01 架构与训练\n## 09 示例\n"
            + " ".join(AUDITOR.RISK_WORDS) + "\n"
            + " ".join(AUDITOR.HYPE_PATTERNS) + "\n"
            "支持 Transformer 架构\n仅具备解码功能\n参数W\n"
            "![image](https://example.com/figure.png)\n开源\n"
        )
        for marker in ("```", "~~~", "````"):
            with self.subTest(marker=marker):
                self.assertEqual(self.audit(NORMAL + f"{marker}text\n{content}{marker}\n"), [])

    def test_prose_findings_keep_physical_line_numbers(self):
        findings = self.audit(NORMAL + "~~~text\n最强\n~~~\n最强\n震惊\n支持 Transformer 架构\n")
        self.assertEqual([(item.code, item.line) for item in findings], [
            ("CLAIM_SCOPE", 7), ("STYLE", 8), ("TRANSFORMERS_TERM", 9),
        ])

    def test_prose_checks_remain_active(self):
        text = NORMAL + (
            "支持 Transformer 架构\n仅具备解码功能\n参数W\n"
            "![image](https://example.com/image.png)\n开源\n"
            "## 01 架构与训练\n仅讨论架构。\n## 03 结果\n"
        )
        self.assertEqual(set(self.codes(text)), {
            "TRANSFORMERS_TERM", "DECODER_TERM", "SPACING", "ALT_TEXT", "OPENNESS",
            "SECTION_ORDER", "SECTION_CONTENT",
        })

    def test_section_numbers_ignore_code_headings(self):
        text = NORMAL + "## 01 简介\n~~~text\n## 99 示例\n~~~\n## 02 结果\n"
        self.assertEqual(self.audit(text), [])

    def test_code_cannot_supply_training_discussion(self):
        text = NORMAL + "## 架构与训练\n~~~text\n预训练 SFT RL\n~~~\n## 结果\n后训练\n"
        findings = self.audit(text)
        self.assertEqual([(item.code, item.line) for item in findings], [("SECTION_CONTENT", 4)])
        self.assertEqual(self.audit(NORMAL + "## 架构与训练\n预训练和后训练。\n"), [])

    def test_missing_h1_including_only_h2_or_code_title(self):
        for content in ("正文\n", "## 二级标题\n", "#\n", "#   \n", "# ###\n", "```text\n# 示例\n```\n"):
            with self.subTest(content=content):
                self.assertEqual(self.codes(MODEL_LINK + content), ["TITLE"])

    def test_h1_after_h2_is_used_for_title_length(self):
        self.assertEqual(self.audit(MODEL_LINK + "## " + "长" * 70 + "\n# 发布\n"), [])
        findings = self.audit(MODEL_LINK + "## 简介\n# " + "长" * 61 + "\n")
        self.assertEqual([(item.code, item.line) for item in findings], [("TITLE_LENGTH", 3)])
        self.assertEqual(self.audit(MODEL_LINK + "   # " + "长" * 60 + " ###\n"), [])

    def test_full_text_deployment_signals_remain_active(self):
        content = (
            "# 从源码构建 package\ngit clone https://example.com/repository\n"
            "serve --quantization NVFP4 --num_speculative_tokens 3\n1M tokens\n"
        )
        for marker in ("```", "~~~", "````"):
            with self.subTest(marker=marker):
                self.assertEqual(set(self.codes(NORMAL + f"{marker}bash\n{content}{marker}\n")), {
                    "UNPINNED_SOURCE", "DEPLOY_CONTEXT", "GIT_PIN", "FP4_HARDWARE", "MTP", "LONG_CONTEXT",
                })

    def test_full_text_deployment_context_remains_effective(self):
        text = NORMAL + (
            "~~~bash\n# 从源码构建 package\ngit clone https://example.com/repository\n"
            "git checkout v1\n# 推理 B200 推测解码 KV Cache\n"
            "serve --quantization NVFP4 --num_speculative_tokens 3\n1M tokens\n~~~\n"
        )
        self.assertEqual(self.audit(text), [])

    def test_temporary_asset_and_local_link(self):
        asset = self.root / "asset.png"
        asset.write_bytes(b"test asset")
        text = NORMAL + f"![性能对比]({asset.as_posix()})\n"
        findings = self.audit(text)
        self.assertEqual({item.code for item in findings}, {"TEMP_URL", "LOCAL_LINK"})
        self.assertEqual(self.cli().returncode, 1)

    def test_temporary_links_still_checked_inside_code(self):
        self.assertEqual(set(self.codes(NORMAL + "~~~text\n[资源](/tmp/asset.png)\n~~~\n")), {"TEMP_URL", "LOCAL_LINK"})

    def test_json_finding_order_and_counts(self):
        self.article.write_text(NORMAL + "最强 震惊\n![图](/tmp/chart.png)\n~~~python\n", encoding="utf-8")
        result = self.cli("--format", "json")
        report = self.assert_report(result)
        self.assertEqual(report["counts"], {"blocker": 2, "major": 2, "minor": 1})
        self.assertEqual([item["code"] for item in report["findings"]], [
            "TEMP_URL", "FENCE", "LOCAL_LINK", "CLAIM_SCOPE", "STYLE",
        ])
        self.assertEqual(result.stdout, self.cli("--format", "json").stdout)

    def test_nonbreaking_space_check_is_preserved(self):
        self.assertEqual(self.codes(NORMAL + "~~~text\na\u00a0b\n~~~\n"), ["NBSP"])

    def check_input_error(self):
        for output in ("text", "json"):
            with self.subTest(output=output):
                result = self.cli("--format", output)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                if output == "json":
                    self.assert_report(result, failed_input=True)
                else:
                    self.assertEqual(result.stdout, "")
                    self.assertTrue(result.stderr.startswith("ERROR: Cannot read article:"))
                    self.assertEqual(len(result.stderr.splitlines()), 1)

    def test_missing_file(self):
        self.article.unlink()
        self.check_input_error()

    def test_directory_input(self):
        self.article.unlink()
        self.article.mkdir()
        self.check_input_error()

    def test_invalid_utf8(self):
        self.article.write_bytes(b"# article\n\xff\xfe\n")
        self.check_input_error()

    def test_invalid_cli_choices(self):
        for option in ("--modelscope", "--fail-on", "--format"):
            with self.subTest(option=option):
                result = self.cli(option, "invalid")
                self.assertEqual(result.returncode, 2)
                self.assertIn("invalid choice", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_missing_article_argument(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT)], capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("article", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_help_explains_contract(self):
        result = self.cli("--help")
        self.assertEqual(result.returncode, 0)
        for option in ("--modelscope", "--fail-on", "--format"):
            self.assertIn(option, result.stdout)
        self.assertIn("not fact verification", " ".join(result.stdout.split()))
        self.assertIn("does not confirm listing status", " ".join(result.stdout.split()))

    def test_python_310_syntax(self):
        ast.parse(SCRIPT.read_text(encoding="utf-8"), feature_version=(3, 10))
        ast.parse(Path(__file__).read_text(encoding="utf-8"), feature_version=(3, 10))


if __name__ == "__main__":
    unittest.main()
