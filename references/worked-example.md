# Worked Example: Evidence Before Prose

This is a completely fictional teaching fixture, not a real model announcement or a
live-source verification report. All names, figures, dates and `example.com` URLs
below are illustrative. Do not publish them as facts, fetch them as model evidence,
or copy them into a real article. No model, benchmark or GPU was run for this example.

## 1. Input and scope

Request: turn two supplied release-note excerpts into a short Chinese developer
brief, preserving uncertainty. No deployment tutorial or public posting is requested.
The editor has no GPU and no rights to redistribute the supplied promotional image.

Fictional source excerpts:

- S-01, release note, https://example.com/model-a/release, section “Model”: Team A
  releases Model A weights; the model accepts text and returns text, with 3 billion
  total parameters. There is no statement about image or audio input.
- S-02, evaluation note, https://example.com/model-a/eval, table 1: Model A scores
  72.0 and Model B scores 70.0 on fictional Task T. The metric is percentage accuracy,
  higher is better. The comparison model's evaluation configuration is not disclosed.
- No license text, tested serving recipe or permitted reproduction of an official
  image is supplied. ModelScope availability has not been checked.

## 2. Source register and claim ledger

Store these in `sources/` alongside a real article; here they remain inline so the
teaching example is self-contained.

| ID | Source URL | Owner | Exact location | Access/revision | Verification status |
|---|---|---|---|---|---|
| S-01 | https://example.com/model-a/release | Fictional Team A | Model paragraph | fixture only | not live-verified |
| S-02 | https://example.com/model-a/eval | Fictional Team A | table 1 | fixture only | not live-verified |

ModelScope state: `unverified`, not `not_listed`. Do not invent a ModelScope ID or
claim the model is absent. For this offline fixture, use optional link lint solely
as a documented test mode; a real release article still requires source review.

| ID | Proposed claim | Type | Evidence | Decision |
|---|---|---|---|---|
| F-01 | Team A releases 3B Model A weights | Direct | S-01, Model paragraph | retain with attribution in fixture |
| F-02 | Supports text input and output | Direct | S-01, Model paragraph | retain; do not expand modalities |
| F-03 | Difference on Task T is 2 percentage points | Derived | S-02: 72.0 - 70.0 = 2.0 | retain with evaluation caveat |
| F-04 | Model A is better overall | Interpretation | no representative comparison | reject |
| F-05 | Model A is open source | License claim | license missing | reject; use release-of-weights wording |
| F-06 | Runs on an ordinary consumer GPU | Deployment claim | no serving or memory evidence | reject |

## 3. Asset and deployment decisions

| Asset ID | Owner/source | Reproduction basis | Privacy check | Status |
|---|---|---|---|---|
| A-01 | Team A / S-01, promotional cover | unknown | not performed | omitted; no file redistributed |

No visual was generated or attributed to Model A. Use text rather than inventing an
official output. For an actual public brief, a link to the release page may be used
after verifying it; do not treat that as permission to copy its images.

Deployment status: `not_applicable` to the short brief. No command, expected API
response, GPU family, peak memory or performance is invented. If the brief becomes a
tutorial, start a deployment record with source-verified commands and mark execution
unverified until suitable hardware and permission are available.

## 4. Candidate prose

The following is the fictional `article.md` content. The prominent disclaimer must
remain in this fixture; remove it only when replacing the entire example with actual
verified material, not by presenting the fictional facts as real.

```markdown
# 教学示例：Model A 权重发布与评测边界

以下团队、模型、分数和链接均为虚构，仅演示文章组织方式，不是真实发布信息。

示例团队 A 发布了 Model A 的模型权重。根据给定材料，这是一款 30 亿总参数的文本模型，接收文本并输出文本；材料没有说明图像或音频输入能力。

● 发布说明：https://example.com/model-a/release
● 评测说明：https://example.com/model-a/eval

## 01　能力与评测

在示例任务 T 上，团队报告的准确率分别为 Model A 72.0%、Model B 70.0%，相差 2 个百分点。这不是独立复测结果，且对照模型的评测设置没有披露，因此不能据此得出整体能力优劣的结论。

## 02　使用边界

材料未提供许可证原文和可核对的部署配置，因此这里不判断使用授权，也不提供下载或启动命令。魔搭收录情况尚未核验，不推测模型 ID。上述信息需要在真实发布前补齐。
```

## 5. Lint versus publication readiness

To exercise the checker, save only the content of the Markdown block above as a local
`article.md`, set `SKILL_DIR` to the installed Skill directory, and run:

```bash
python3 "$SKILL_DIR/scripts/audit_markdown.py" article.md --modelscope optional --fail-on major --format json
```

Expected lint result: exit code `0`, no major/blocker findings for the fixture, and
`passed: true` for the selected threshold. The same file with default
`--modelscope required --fail-on major` should report `MODELSCOPE` and exit `1`.
Neither result means the fictional sources were opened or the article is publishable.

Editorial outcome: **Not ready for real publication**. The text is acceptable as a
labeled teaching fixture only. Source URLs, license, ModelScope availability and any
future asset rights must be verified for a real model. No article was publicly posted.

## 6. Expected decisions for common edge cases

| Situation | Expected decision |
|---|---|
| Official evidence shows weights are not released yet | State availability accurately; do not promise a runnable download |
| A ModelScope card exists but files are incomplete | Record `pending_weights`; disclose it beside the card link |
| A documented live search finds no ModelScope listing | Record `not_listed`, scope/date and verified official fallback; optional link lint is permitted |
| A ModelScope page is inaccessible | Record `unverified`; do not infer absence |
| GPU is unavailable but an official recipe exists | Record `source_verified`, not `executed`; disclose untested hardware assumptions |
| An image is visible only after login | Check access authorization, reuse rights and private data before any reproduction |
| Lint reports a risk word in a properly scoped quotation | Inspect source and record why the warning is resolved; do not silently change the threshold |
