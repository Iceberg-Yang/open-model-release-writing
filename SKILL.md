---
name: open-model-release-writing
description: Research, draft, revise, fact-check, source, and audit Chinese WeChat or ModelScope release articles about open-weight or open-source AI models. Use when the user provides a model card, paper, official blog, README, PDF, benchmark table, demo, or deployment guide and asks for model analysis, a launch article, title or introduction, effect cases, technical interpretation, benchmark comparison, ModelScope download, vLLM/SGLang deployment, official media collection, article polishing, or final publication review. Enforces first-party source priority, claim-scope boundaries, benchmark-date tracking, official-asset provenance, hardware-specific deployment validation, objective third-party language, and explicit separation of facts from editorial inference.
---

# Open Model Release Writing

Produce concise, visual-first, technically accurate Chinese model-release articles whose claims remain traceable to evidence. Treat the task as editorial research plus source auditing, not as paraphrasing one announcement.

## Route the task

Read only the references needed for the request:

- For a full article or comprehensive review, read the seven workflow references listed below; use `references/worked-example.md` only when an end-to-end example is useful.
- For title, introduction, comparison, or wording work, read `references/source-and-fact-audit.md` and `references/article-structure-and-style.md`.
- For images, videos, screenshots, or PDFs, also read `references/media-and-assets.md`.
- For model download or inference commands, also read `references/deployment-audit.md`.
- For any ModelScope download command, model id, link block, SDK inference, collection/paper/doc link, or ecosystem claim, also read `references/modelscope-integration.md`. The ModelScope model id and download command must be verified on the live model card every time; never infer them from the Hugging Face id or memory.
- For final review, read `references/review-gates.md` and run `scripts/audit_markdown.py` when a local Markdown file exists.
- Use `references/templates.md` when creating a fact ledger, source registry, asset manifest, outline, or audit report.

If another applicable artifact skill exists, use it for the artifact operation: PDF rendering for PDFs, browser control for authenticated pages, and image generation only when the user explicitly wants a generated illustration.

## Runtime and portability

Use a host Agent with web access for live source verification and file access for local outputs. The audit script requires Python 3.10+ and only the standard library; it does not access the network. PDF rendering and browser automation are optional host capabilities, not bundled services. If a capability is unavailable, request source material or mark the corresponding check unverified rather than claiming success.

Resolve `scripts/` and `references/` relative to the installed Skill directory, not the article working directory. Set `SKILL_DIR` to that directory before running the commands below. `agents/openai.yaml` is optional Codex display metadata; other hosts may ignore it. Publishing this package to ModelScope Skills does not provision a runtime or publish articles automatically.

## Respect the requested operation

Distinguish among analysis, drafting, editing, and publishing. Preparing a draft or reviewing it does not authorize posting to a public platform; obtain explicit publication authorization for the final candidate.

- If asked to analyze, inspect and report; do not edit files.
- If asked to provide replacement prose, return prose only; do not modify the document.
- If asked to change the article, edit the requested file and verify the result.
- If the directory contains multiple drafts, identify the likely final version from names, timestamps, links, and user context before reviewing it.
- Preserve user-owned edits and unrelated files.
- Do not insert a collected asset into the article when the user asks only to download, render, or organize it.

## Follow the evidence-first workflow

### 1. Define scope and audience

Determine the deliverable, platform, target reader, desired length, reference article, required sections, and whether the user wants objective reporting or promotional copy. Default to an objective third-party release article for developers and researchers.

When a reference article is supplied, learn its macro-structure, paragraph rhythm, information density, image cadence, and formatting. Do not reproduce distinctive sentences or imitate an identifiable author's wording line by line.

### 2. Build a source pack

Start with first-party sources:

1. Official release page or paper.
2. Official model card and repository.
3. Official framework documentation or integration announcement.
4. Official benchmark page, safety report, license, and deployment recipe.
5. Reputable reporting for company history or independent context.

Browse whenever facts can change: benchmark scores, model versions, framework support, commands, hardware requirements, licensing, leaderboards, company roles, or pricing. Record the access date for dynamic sources.

Do not use secondary news to override first-party technical details. Do not treat a search-result snippet as sufficient evidence when the source page is available.

### 3. Create a claim ledger before drafting

Record each consequential claim with its source, exact location, date, type, and caveat. Use the template in `references/templates.md`.

Classify claims as:

- **Direct fact**: explicitly stated by a primary source.
- **Derived fact**: calculated or translated from source data; show the derivation.
- **Interpretation**: an editorial synthesis such as “balanced” or “close”; state its comparison scope.
- **Promotion**: a headline-level claim such as “best,” “beats,” or “rivals”; require unusually strong evidence.

If evidence is incomplete, narrow the sentence instead of filling the gap with plausible reasoning.

### 4. Select the article angle

Choose one dominant angle rather than listing every capability:

- **Case-led** for models with strong official demos or multimodal artifacts.
- **Benchmark-led** for releases whose main contribution is measurable performance.
- **Architecture-led** for novel model design or training methods.
- **Deployment-led** for inference engines, quantization, or infrastructure releases.

Use supporting angles only when they reinforce the main one.

### 5. Collect official evidence assets

Prefer official figures, screenshots, videos, PDFs, tables, and model outputs. Keep an asset manifest with source URL, capture date, description, and any crop or conversion applied.

Do not generate architecture, benchmark, or deployment diagrams unless the user requests a generated schematic. If generated, label it clearly as an interpretation rather than an official figure.

### 6. Draft in evidence order

Use this default order unless the reference format or model requires another:

1. Title.
2. Concise introduction and open links.
3. Effect cases or core capabilities.
4. Architecture and training.
5. Performance and comparison.
6. Download, deployment, and inference.

The published article body normally ends at step 6. Do not add a 总结, 资料来源, or 核验日期 section by default. A short closing sentence may restate a material license/usage boundary or a verified ModelScope workflow connection (see `references/modelscope-integration.md`). Keep dense tables and exhaustive benchmark rows inline near the point they support, with the conditions needed to interpret them, rather than in a separate appendix.

Put the strongest visual evidence early. Record sources, access and verification dates, the claim ledger, and the asset manifest in the sibling `sources/` files, not in the article body.

Scale the `sources/` artifacts to the claim risk: a case-led release needs a claim ledger and an asset manifest; add a comparison note for benchmark-led work and a deployment record for deployment-led work. Do not produce every template artifact when the claim risk does not warrant it.

### 7. Explain technology in two passes

First translate the official technical description faithfully. Then compress it into reader-facing language while preserving quantities, topology, modality boundaries, and uncertainty.

For each technical point, answer:

- What component is used?
- How is it configured?
- What work does it perform?
- What did the source actually claim about its benefit?

Do not invent causal benefits. If the source says a component “is intended to” improve efficiency, do not rewrite it as a measured speedup.

### 8. Audit comparisons

Never expand a conclusion beyond the evaluated rows. “Close on four selected benchmarks” does not mean “overall equal.” “Best open-weight audio model among compared systems” does not mean “best model.”

Before using `领先`, `超越`, `比肩`, `最强`, `SOTA`, `第一`, or `相近`, define:

- compared models;
- benchmark set;
- metric direction;
- evaluation setting;
- score source;
- date or snapshot.

Prefer qualified language such as `在上述评测中互有高低` or `官方将其定位为能力覆盖较广的基础模型` when the evidence is mixed.

### 9. Audit deployment as executable documentation

Treat commands as versioned technical instructions, not decorative code. Verify the exact checkpoint, quantization, GPU architecture, total and runtime memory, framework version or commit, parallelism, context limit, modality support, and API behavior.

Explain only the unusual parameters readers must understand, such as MTP, tensor parallelism, model-specific reasoning/tool parsers, KV-cache formats, or hardware-specific kernels. Avoid a paragraph for every tuning flag.

### 10. Run final gates

Use `references/review-gates.md`. Block delivery or publication when a core claim lacks a source, a benchmark is mapped to the wrong model, a deployment command is unsupported for the stated hardware, or an unofficial visual is presented as official.

Run a publication-oriented lint pass from any working directory:

```bash
python3 "$SKILL_DIR/scripts/audit_markdown.py" /absolute/path/to/article.md --fail-on major
```

Use `--modelscope optional` only when the publication does not require a ModelScope channel, or the model is not listed and that finding is documented with the search scope, date and official fallback URL in `sources/`. An inaccessible page alone does not establish absence. Do not use this option to skip checking a ModelScope link or command that is present. Use `--format json` for machine-readable findings and counts.

Exit codes: `0` means no finding reached the selected threshold, `1` means the threshold was reached, and `2` means an input/usage error. The default threshold is `blocker` for backward compatibility; `--fail-on major` also fails on major findings, and `--fail-on minor` fails on any finding. JSON `passed` has this same lint-only meaning.

Treat script output as heuristic warnings. A zero exit code does not verify facts, URLs, asset rights, benchmark mappings, or deployment compatibility. Resolve findings through source inspection and record justified exceptions rather than mechanically deleting flagged words or weakening the threshold. Human review gates still determine publication readiness.

Run the standard-library regression suite when modifying the checker:

```bash
python3 -B -m unittest discover -s "$SKILL_DIR/tests" -v
```

## Apply strict writing rules

- Lead with who released what and the most important differentiator.
- Keep the introduction short enough to create forward motion; do not turn it into an abstract.
- Use third-person, evidence-backed language.
- Prefer concrete nouns and verbs over rhetorical questions.
- Keep one paragraph focused on one claim.
- Use consistent Chinese terminology and spacing around English words and numbers.
- Separate input modalities, output modalities, pretraining data modalities, and evaluated modalities.
- Separate total parameters, active parameters, checkpoint size, and runtime memory.
- Separate architectural context support from context actually exposed by a hosted service.
- Call a release `开放权重` when that is the source's wording; use `开源` only when the license and released components justify it.
- Attribute official claims with `官方表示`, `官方评测`, or a caption when independence is not established.
- State when results are from an earlier checkpoint, internal harness, self-reported comparison, or different reasoning effort.
- Avoid `本文将`, `小编`, `震惊`, `竟然`, empty superlatives, and question-based hype.
- Do not repeat the same parameter block in the title, introduction, architecture section, and conclusion.

## Stop and narrow the claim when

- the official page changed after a screenshot was captured;
- a table omits a score or plots missing data as zero;
- a leaderboard mixes open and closed models or different settings;
- an example is official but its prompt, tool access, or iteration count is unclear;
- a video-capable input path exists but out-of-the-box video performance was not evaluated;
- a quantized checkpoint requires a GPU architecture different from the user's hardware;
- a framework recipe is generated dynamically and has no pinned version;
- a company-history claim comes only from an unsourced biography or aggregator;
- a reference article's distinctive phrasing would be copied too closely.

In these cases, state the limit, record the date, or omit the claim.

## Deliver transparently

When handing off an article or review, report:

- which file is the final candidate;
- which primary sources were used;
- which facts remain dynamic or self-reported;
- which assets are official, converted, cropped, or generated;
- what was changed and what was intentionally left unchanged;
- any publication-blocking issues.

Do not claim the work is fully verified if only prose was reviewed and links, images, tables, or commands were not checked.
