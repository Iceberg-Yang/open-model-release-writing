# Article Structure and Style

## Contents

1. Editorial positioning
2. Structure selection
3. Titles
4. Introductions
5. Effect cases
6. Technical interpretation
7. Performance sections
8. Deployment sections
9. Language rules
10. Reference-style adaptation

## 1. Editorial positioning

Default to a third-party technical release article for developers and researchers:

- Objective, concise, and information-dense.
- Interested in what the model does, how it works, how it compares, and how to run it.
- Positive when evidence supports it, but not written as the vendor.
- Visual-first when official demos are strong.
- Practical without pretending cluster deployment is consumer-local inference.

Decide whether the output is:

- a short news post;
- a full WeChat article;
- a ModelScope promotional article;
- a technical explainer;
- a deployment tutorial;
- a review or revision of an existing draft.

Do not apply the same length and section requirements to all formats.

## 2. Structure selection

### Canonical skeleton and formatting

Default article body, in order:

1. Title.
2. Introduction: who released what plus the single biggest differentiator.
3. Link block using `●` bullets, verified ModelScope download first when available (otherwise the documented official fallback in `modelscope-integration.md`), then a permitted cover image if available.
4. `## 01　效果案例` (or 效果展示 / 核心更新).
5. `## 02　技术解读`.
6. `## 03　性能表现`.
7. `## 04　模型下载与推理`.

Formatting rules:

- Number sections with two digits followed by one full-width space, as in `01　效果案例`.
- Use these canonical Chinese section names; do not invent synonyms per article.
- The body ends at `04`. Do not append 总结, 资料来源, or 核验日期 sections by default; those facts live in `sources/`.
- Use `●` for the link block, a bold lead-in for sub-points inside a section, and Markdown tables for comparisons.
- Keep consistent Chinese-English spacing around English words and numbers.

### Case-led model release

Use when official demos communicate value better than benchmark rows.

1. Introduction and links.
2. Two or three effect cases.
3. Architecture and training.
4. Performance overview.
5. Deployment.
6. Full scores inline where they support the point; no separate appendix by default.

### Benchmark-led release

Use when the main news is a measurable capability jump.

1. Introduction with one or two decisive scores.
2. Evaluation conditions.
3. Comparison table.
4. Technical explanation for the gain.
5. Examples.
6. Deployment.

### Architecture-led release

Use when the release introduces a new attention, MoE, modality, or training method.

1. Introduction.
2. One official architecture figure.
3. Three to five technical points.
4. Ablations or supporting results.
5. Cases and deployment.

### Deployment-led release

Use for quantization, serving, or inference-engine articles.

1. What can now run and where.
2. Hardware and memory matrix.
3. Download and verified commands.
4. Special flags.
5. Performance and known limits.

## 3. Titles

Build a title from:

`model + release action + one defensible differentiator + optional scale`

Good ingredients:

- total/active parameters;
- context length;
- native modality set;
- an independently defensible benchmark claim;
- a deployment breakthrough.

Rules:

- Keep it readable on mobile.
- Use one main claim, not five comma-separated claims.
- Prefer `开放权重` when technically precise.
- Avoid exclamation marks unless the publication convention requires one.
- Do not use `比肩` or `超越` without an explicit benchmark scope in the body.
- Re-audit the title after the article is finished.

Safer example:

> Model X 开放权重：总参数 500B、激活 30B，支持原生音频输入

Risky example:

> Model X 开源：全面比肩所有闭源模型！

## 4. Introductions

The first sentence must answer who released what.

Then cover only the most important items:

1. Company or team identity, in one short clause or sentence.
2. Model scale and primary differentiator.
3. Broad performance position or one decisive result.
4. Intended role: generalist, coding, multimodal, edge, or customization.

Do not turn the introduction into a benchmark table or architecture inventory. Exact benchmark digits may be omitted when a figure immediately follows, but retain at least one concrete scale or capability fact.

Preferred pattern:

> Company A 开放了 Model X，一款总参数 500B、每 Token 激活 30B 的多模态 MoE 模型。公司此前推出了 Product Y，Model X 是其首个从零训练并开放完整权重的基础模型。在所列推理、代码和工具评测中，Model X 与多款主流开放权重模型互有高低；其主要特点是把图像、音频、长上下文和可控推理整合到同一可定制模型中。

Avoid:

- company biographies longer than the model introduction;
- four benchmark names and four scores in one sentence;
- repeating the same parameter block twice;
- vague openings such as `随着 AI 快速发展`;
- first-person meta language such as `本文将介绍`.

## 5. Effect cases

Select two or three cases with different capability signals:

- One-shot creation.
- Tool or browser operation.
- Long iterative refinement.
- Multimodal understanding.
- Multi-page or structured artifact generation.

For each case, state:

1. What prompt or task was given.
2. What the model produced or did.
3. Which tools, iterations, or external reviewer were involved.
4. Where the official evidence appears.
5. What the case does not prove.

Do not describe a 40-iteration result as one-shot. Do not describe a web-verified artifact as pure parametric knowledge. Do not infer general benchmark quality from one polished demo.

Prefer official outputs over recreated examples. Remove a case when it needs more explanation than the capability insight it provides.

## 6. Technical interpretation

Use compact subheads and explain one mechanism per paragraph.

Recommended order:

1. Base architecture and parameter routing.
2. Attention and context handling.
3. Native modalities and encoders/embeddings.
4. Training and post-training.
5. Controllable reasoning or tool behavior.

Apply a three-stage transformation:

### Stage A: faithful translation

Translate the official description without adding benefits or removing qualifiers.

### Stage B: terminology normalization

Use consistent terms:

- `仅解码器架构`, not `仅具备解码功能`.
- `Token`, not alternating among `标记`, `词元`, and `Token` unless the publication requires Chinese terminology.
- `短卷积`, not a new term that implies another architecture.
- `路由专家` and `共享专家` with explicit counts.

### Stage C: reader-facing compression

Explain how information flows without replacing precision with analogy. Keep exact ratios, counts, patch sizes, chunk sizes, and caveats when they are central.

After the precise explanation, one short reader-facing analogy line is an endorsed house technique, introduced as `可以简单理解为：` (for example, 可以简单理解为：GDN 负责高效记住，QSA 负责精准查找). The analogy anchors understanding; it supplements the precise numbers and never replaces them. Use at most one per technical point.

Do not write unsupported headings such as `共享专家带来更强表现` when no ablation measures that benefit. Use descriptive headings such as `256 个路由专家与 2 个共享专家`.

## 7. Performance sections

Use three layers:

### Layer 1: overview

One short paragraph describing the evaluated domains and broad position.

### Layer 2: visual evidence

Use an official table, chart, or a compact sourced comparison table. Include a caption and evaluation conditions.

### Layer 3: full detail

Place the full official table, footnotes, or long benchmark matrix inline near the point it supports, or keep it in `sources/` when it is too dense for the body. Do not create a separate 附录 section by default.

When a figure already contains the numbers,正文不必重复所有数字. Use text to explain only the important pattern and limitation.

Avoid cherry-picking four favorable scores to imply broad superiority. If different benchmark families tell different stories, say so.

## 8. Deployment sections

Use this order:

1. Practical scale warning.
2. Checkpoint and hardware choice.
3. ModelScope or official download.
4. Framework installation.
5. Server launch.
6. One test request when useful.
7. Explanations for exceptional flags.

Record the command source and validation date in `sources/`, not in the article body. Verify every ModelScope model id and download command on the live model card before publishing (see `modelscope-integration.md`); never infer them.

Avoid saying `支持 Transformer 架构` when the intended claim is `已接入 Hugging Face Transformers`.

Do not call a 600 GB multi-GPU setup ordinary local deployment. Use `私有化部署`, `本地集群部署`, or `多 GPU 部署` where appropriate.

## 9. Language rules

### Prefer

- `官方公布的结果显示`
- `在上述评测中互有高低`
- `官方将其定位为`
- `支持文本、图像和音频输入，输出为文本`
- `预训练数据包含视频，但视频能力尚未单独评测`
- `该配置在 B200 × 8 环境验证`

### Avoid or qualify

- `最强`, `顶级`, `全面领先`, `彻底超越`
- `表现更佳` without an ablation
- `仅激活 30B，所以只需 30B 模型显存`
- `支持百万上下文，所以任何部署都能开满百万`
- `官方开源` when only weights are available
- question-led hype such as `为什么它只激活……？`

Use Chinese-English spacing consistently. Keep model names and benchmark capitalization consistent with the source.

### Approved caveat sentences

Reuse these house patterns instead of inventing new wording each time. Place each caveat next to the claim it limits.

- Effect cases: 以上为官方展示的案例，非独立第三方评测，不能单独证明模型在所有同类任务上的成功率。
- Performance: 上述结果来自官方评测表，不代表模型在所有项目上都领先；不同数据集的评测体系存在差异，分数不宜跨数据集直接比较。
- Self-reported scores: 表中部分对照成绩来自公开榜单或模型提供方自报，缺少公开来源的结果由开发团队自行评测。
- Deployment: 这些命令是官方针对指定 GPU 拓扑提供的部署示例，不应直接视为其他 GPU、单节点或消费级设备上的通用配置。
- Deployment validation: 命令按官方仓库核对，但未在相应 GPU 环境实际执行。
- License: 使用前应核对许可证原文、模型版本与适用地域或营收限制；涉及真实人物或事件时应标注 AI 生成内容。

## 10. Reference-style adaptation

When asked to follow another article:

- Extract section order, paragraph length, image placement, heading hierarchy, caption style, and code-block density.
- Create a structural style sheet before drafting.
- Preserve the new model's evidence and natural terminology.
- Do not copy distinctive metaphors, slogans, transitions, or long sentence patterns.
- Do not force a section from the reference when the new model lacks evidence for it.

The target is recognizably similar editorial architecture, not textual imitation.
