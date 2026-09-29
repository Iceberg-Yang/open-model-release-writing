# Reusable Templates

These artifacts live in the model's `sources/` directory and back the article; they are
not part of the published article body. Produce only the artifacts the claim risk warrants
(see SKILL.md, draft in evidence order).

## Contents

1. Fact ledger
2. Source registry
3. Asset manifest
4. Article outline
5. Comparison note
6. Deployment record
7. Final audit report

## 1. Fact ledger

All rows below are illustrative placeholders, not verified model facts. Replace them
with actual evidence before using the register for a real article.

```markdown
| ID | Proposed claim | Type | Source ID/location | Version/date | Conditions | Caveat | Status |
|---|---|---|---|---|---|---|---|
| F-01 | Model X has 500B total and 30B active parameters | Direct | S-01, Architecture section 1 | checkpoint/date | per token | active != VRAM | Pending |
| F-02 | Performance is close to Model Y | Interpretation | S-02, benchmark rows A-D | accessed YYYY-MM-DD | effort/temp/tools | only selected rows | Pending narrowing |
```

## 2. Source registry

```markdown
| ID | Source | URL | Owner | Role/location | Published | Accessed | Mutable | Revision/local snapshot | Shareable? |
|---|---|---|---|---|---|---|---|---|---|
| S-01 | Official release | verified canonical URL | Model developer | architecture, section 2 | YYYY-MM-DD | YYYY-MM-DD | Yes | permitted local path or none | yes/no/unknown |
| S-02 | Model card | verified canonical URL | Model developer | weights/license/inference | YYYY-MM-DD | YYYY-MM-DD | Yes | commit | yes/no/unknown |
| S-03 | Framework recipe | verified canonical URL | Framework project | deployment matrix cell | YYYY-MM-DD | YYYY-MM-DD | Yes | version/commit | yes/no/unknown |
| S-04 | News profile | verified canonical URL | Publication | company background | YYYY-MM-DD | YYYY-MM-DD | No/Yes | none | link only |

ModelScope availability: available / pending_weights / not_listed / not_applicable / unverified
Checked scope and date:
ModelScope card URL and exact ID, when available:
Official fallback URL, when needed:
Exception reason and reviewer:
```

Reference source IDs plus exact sections/pages/rows from the fact ledger. A URL
and an access date are required for a checked web source; do not mark example rows
as verified. Keep credentials and temporary signed URLs out of this register.

## 3. Asset manifest

```markdown
| Asset ID | Local file | Type | Source ID/page URL | Direct asset URL | Owner | Captured | Transform/pages/time | Caption | Article position |
|---|---|---|---|---|---|---|---|---|---|
| A-01 | assets/model-cover.png | Official | S-01 / canonical URL | direct URL | model developer | YYYY-MM-DD | none | Official cover | intro |
| A-02 | assets/demo/page-01.png | Official conversion | S-01 / canonical URL | PDF URL | model developer | YYYY-MM-DD | page 1, 180 DPI render | Demo page 1 | case 2 |

| Asset ID | Reproduction basis | Required attribution | Privacy/redaction check | Publication status | Durable public URL | Local master shareable? |
|---|---|---|---|---|---|---|
| A-01 | license/permission reference or pending | exact credit | checked/pending, edits | ready/blocked/omitted | verified URL or pending | yes/no/unknown |
| A-02 | license/permission reference or pending | exact credit | checked/pending, edits | ready/blocked/omitted | verified URL or pending | yes/no/unknown |
```

Join the two tables by Asset ID. Mark unclear rights or incomplete redaction as
`blocked`; omit an asset rather than implying public access grants redistribution.

## 4. Article outline

```markdown
# Model X 开放权重：核心卖点

Company A 发布了 Model X，……

● ModelScope：
● Official release：
● Model card：

## 01　效果案例

案例一：任务、工具、结果、证据、限制。

案例二：任务、迭代、结果、证据、限制。

## 02　技术解读

**架构点一**

官方机制 + 配置 + 谨慎解释。

**训练**

预训练数据、优化器、SFT/RL、可控推理。

## 03　性能表现

官方条件、代表性结论、图表和限制。

## 04　模型下载与推理

硬件警告、下载（ModelScope 命令先在模型卡核验）、框架 A、框架 B、特殊参数。
```

## 5. Comparison note

```markdown
Comparison scope:
- Models:
- Benchmarks:
- Same harness? yes/no/mixed
- Same reasoning setting? yes/no/mixed
- Missing scores:
- Largest gap:
- Mixed wins/losses:
- Allowed wording:
- Disallowed wording:
```

## 6. Deployment record

```markdown
Checkpoint:
Quantization:
Weight license:
Hardware:
GPU count and memory:
Nodes:
CUDA/ROCm:
Framework and version/commit:
Install source:
Parallelism:
Context tested:
Modalities tested:
Special flags:
Command source URL:
Validation status: source_verified / executed / unverified / not_applicable
Verification date:
Test request and input (no credentials):
Expected response shape and source:
Actual response and exit status, if executed:
Hardware availability and reason for any unexecuted check:
Known limitations:
```

## 7. Final audit report

```markdown
## Outcome

Ready / Ready with caveats / Not ready.

## Final candidate

Absolute path and modification date.

## Blockers

- Claim, location, evidence gap, recommended narrowing.

## Major issues

- Stale benchmark, missing condition, unsupported visual, environment mismatch.

## Minor issues

- Terminology, spacing, duplicate content, generic alt text.

## Source status

- Primary sources checked:
- Dynamic sources accessed:
- Self-reported results:
- Unresolved facts:

## Asset status

- Official:
- Converted/cropped:
- Generated:
- Access or durability risks:

## Deployment status

- Source-verified:
- Locally executed:
- Hardware/version caveats:
```
