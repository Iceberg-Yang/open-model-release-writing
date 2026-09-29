# Source and Fact Audit

## Contents

1. Source hierarchy
2. Claim ledger
3. Openness and licensing
4. Architecture and modality facts
5. Benchmark auditing
6. Company and product context
7. Time-sensitive facts
8. Citation and quotation practice

## 1. Source hierarchy

Use the strongest available source for each claim rather than one source for the whole article.

### Tier A: primary technical evidence

- Official model release page.
- Official model card, configuration, weights repository, license, or paper.
- Official benchmark table, evaluation report, safety report, or appendix.
- Official framework integration documentation and tested deployment recipe.
- Official demo, prompt, output artifact, video, or PDF.

Use Tier A for parameters, training, modalities, performance, license, commands, and model behavior claims.

### Tier B: primary organizational evidence

- Company about page, newsroom, executive announcement, product documentation, or regulatory filing.
- Named statements by company leaders.

Use Tier B for company identity, leadership, product history, and mission. A model launch page may not support founder or funding claims.

### Tier C: independent reporting and evaluation

- Reputable news organizations.
- Independent benchmark organizations.
- Peer-reviewed or clearly authored technical analysis.

Use Tier C for company history not covered by official sources, outside reactions, independent replication, and context. Attribute it.

### Tier D: discovery only

- Search snippets, aggregators, social reposts, community threads, unsourced summaries, and generated search answers.

Use Tier D to find better sources, not as final evidence for consequential claims.

## 2. Claim ledger

Create a ledger before drafting. One row may support one sentence or a cluster of tightly related facts.

Required fields:

- Claim ID.
- Proposed wording.
- Claim type: direct, derived, interpretation, promotion.
- Source title and URL.
- Exact section, table row, line, page, or timestamp.
- Source owner.
- Publication date and access date.
- Checkpoint or version.
- Evaluation setting or hardware.
- Caveat.
- Status: verified, narrowed, omitted, stale, or unresolved.

Apply these rules:

- Keep the source's unit and metric direction.
- Record whether a percentage is absolute accuracy, pass rate, win rate, or normalized score.
- Record whether a model name includes a reasoning level, tool setting, checkpoint suffix, or quantization.
- Mark translations as derived facts when terminology could change meaning.
- Store screenshots as snapshots, not as timeless truth.

## 3. Openness and licensing

Do not use `开源` and `开放权重` interchangeably without checking what was released.

Verify separately:

- Are full weights available?
- Is training code available?
- Is inference code available?
- Are data or data recipes available?
- Is the license OSI-approved, custom, research-only, noncommercial, or otherwise restricted?
- Are quantized checkpoints covered by the same license?
- Is hosted fine-tuning a separate paid service?

Preferred wording:

- Use `开放权重模型` when the official release says open weights and the broader stack is not fully open.
- Use `采用 Apache 2.0 许可证开放权重` only after confirming the repository license.
- Avoid `完全开源` unless weights, code, and relevant license terms justify it.

## 4. Architecture and modality facts

### Parameters

Keep these distinct:

- Total parameter count.
- Active parameters per token.
- Routed experts and shared experts.
- Experts selected per token.
- Checkpoint size on disk.
- Weight memory at a precision or quantization.
- Runtime memory including caches and framework overhead.

Do not infer that active parameters equal required VRAM. Sparse activation reduces computation but the weights still need storage or sharding.

### Modality

Track four different scopes:

1. Modalities present in pretraining data.
2. Modalities accepted by the released checkpoint.
3. Modalities generated as output.
4. Modalities evaluated and supported by serving frameworks.

Examples of invalid expansion:

- `video appeared in pretraining data` → not automatically `released model has verified video understanding`.
- `image inputs contain a temporal dimension` → not automatically `out-of-the-box video performance is established`.
- `audio model input is supported in Transformers` → not automatically `every hosted inference provider supports audio`.

### Architecture benefits

Distinguish mechanism from measured outcome:

- Mechanism: five sliding-window layers per global layer.
- Source intention: chosen for efficiency and long-context performance.
- Measured outcome: requires a benchmark or ablation.

Do not change `intended to`, `we find`, or `designed for` into a universal causal claim.

Translate topology precisely. For MoE, identify the selection pool and active count; do not write `select top-k from six experts` if six is already the number selected from a larger pool.

## 5. Benchmark auditing

### Preserve evaluation identity

For every score, record:

- Benchmark name and version.
- Split or public/private subset.
- Tools allowed or not allowed.
- Reasoning effort, temperature, sampling, and pass count.
- Context or trajectory limit.
- Harness and grader.
- Model checkpoint and date.
- Whether higher or lower is better.

Do not merge similarly named benchmarks such as SWE-Bench Verified and SWE-Bench Pro Public.

### Inspect table geometry

When transcribing a screenshot or HTML table:

- Match each score to the correct column.
- Check multi-row headers and model suffixes.
- Preserve dashes as missing values; never convert missing values to zero unless the source explicitly does so.
- Check whether charts normalize different metrics to a shared scale.
- Check whether a radar plot places unreported values at zero.
- Keep footnotes tied to the affected rows.

### Qualify comparison language

Use a comparison matrix before writing conclusions:

| Wording | Minimum evidence |
|---|---|
| `取得 X` | Direct score and setting |
| `接近模型 Y` | Defined benchmark set and small, visible differences |
| `互有高低` | Multiple rows showing mixed wins and losses |
| `领先模型 Y` | Same setting and better score on the named row |
| `整体领先` | Broad representative suite with consistent advantage |
| `最强` / `SOTA` | Defined population, date, leaderboard, and no stronger eligible result |
| `比肩` | Explicit scope; never rely on one cherry-picked metric |

When results are mixed, prefer:

> 在所列推理、代码和工具评测中，该模型与若干主流开放权重模型互有高低。

Do not write:

> 整体能力全面比肩顶级模型。

### Separate official and independent results

State when:

- the model developer ran the benchmark;
- external model scores are self-reported;
- an internal harness is used;
- an independent evaluator supplied selected rows;
- different models used different reasoning settings;
- safety, forecasting, or arena results came from another checkpoint.

An official table is a valid report of official claims, not automatically an independent apples-to-apples evaluation.

## 6. Company and product context

Keep company introductions short and sourced. Verify:

- Founder versus cofounder.
- Current executive role.
- Founding year.
- Previous product names and launch order.
- Whether a release is the first model, first foundation model, or first open-weight model.

Do not add funding, valuation, employee pedigree, or strategic interpretation unless it serves the article and has a reputable source.

Use exact role wording where possible, such as `联合创始人兼 CEO`, rather than collapsing a team into one founder.

## 7. Time-sensitive facts

Recheck immediately before delivery:

- Benchmark tables and leaderboards.
- Model-card revisions and checkpoint names.
- Framework support and command flags.
- Pricing and hosted context limits.
- License files.
- Company titles and product availability.

For mutable official pages, save:

- access date;
- screenshot or archived local copy;
- visible checkpoint/version;
- a note if the source later changes.

If an official score changes after capture, do not call the older screenshot fabricated. Label it as an earlier snapshot and either update it or state the capture date.

## 8. Citation and quotation practice

- Link directly to the supporting page, not a search result.
- Place a source near the claim it supports.
- Use captions to identify official figures and screenshots.
- Paraphrase rather than copying long passages.
- Quote only the minimum words needed and respect source quotation limits.
- When a statement is inferred from several rows, say `根据官方表格可见` and identify the scope.
- Never cite one source for a sentence containing unrelated company, benchmark, architecture, and license claims unless it supports all of them.
