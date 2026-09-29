# Review Gates

## Contents

1. Severity model
2. Scope and file gate
3. Evidence gate
4. Comparison gate
5. Technical gate
6. Media gate
7. Deployment gate
8. Editorial gate
9. Publication gate
10. Failure patterns

## 1. Severity model

Classify findings:

- **Blocker**: publication would contain a false, unsupported, misleading, inaccessible, or non-executable core element.
- **Major**: material ambiguity, missing caveat, stale dynamic data, or claim broader than evidence.
- **Minor**: terminology, style, redundancy, caption, filename, or formatting issue that does not change the central meaning.

Do not mark an article complete while blockers remain. Resolve major issues or record
a source-backed reason why the warning does not apply. A checker's zero exit code is
only a lint result, not approval to publish. Apply only relevant gates; mark omitted
sections `not_applicable` with a reason instead of fabricating missing evidence.

## 2. Scope and file gate

- [ ] The requested operation is clear: analyze, draft, edit, collect assets, or publish.
- [ ] The correct final candidate was identified when multiple drafts exist.
- [ ] The user asked for file changes before any edits were made.
- [ ] Collected-only assets were not inserted prematurely.
- [ ] Existing unrelated edits were preserved.
- [ ] The article platform and target audience are known.

## 3. Evidence gate

- [ ] Every title and introduction claim appears in the claim ledger.
- [ ] Parameter, context, modality, training, license, and availability claims use primary sources.
- [ ] Company-history claims use an organizational or reputable reporting source.
- [ ] Direct facts, derived facts, interpretations, and promotional claims are distinguishable.
- [ ] Mutable sources have access dates.
- [ ] No search snippet is the sole evidence for a consequential claim.
- [ ] `开源`, `开放权重`, and license wording match the released artifacts.
- [ ] Input, output, training-data, and evaluated modalities are not conflated.
- [ ] Hosted-service limits are not presented as architecture limits or vice versa.

## 4. Comparison gate

- [ ] Benchmark name, version, split, metric, and direction are correct.
- [ ] Every score is under the correct model column.
- [ ] Missing values remain missing.
- [ ] Reasoning effort, temperature, tools, context, and harness are stated where material.
- [ ] External results are labeled self-reported, independent, or internally rerun.
- [ ] Claims such as `接近`, `领先`, `比肩`, `最强`, and `SOTA` have explicit scope.
- [ ] A few selected rows are not generalized to overall model quality.
- [ ] The official page has been reopened since any screenshot was captured.
- [ ] Earlier checkpoint results are labeled.
- [ ] The title does not overstate the body.

## 5. Technical gate

- [ ] Total and active parameters are distinguished.
- [ ] Expert pool, selected experts, and shared experts are correctly described.
- [ ] Attention ratio and positional method are accurate.
- [ ] Technical benefits do not exceed official claims or ablations.
- [ ] Translations use consistent terminology.
- [ ] The section name matches its contents; a `架构与训练` section actually includes training.
- [ ] Video, audio, or image capabilities retain official caveats.
- [ ] `Token`, patch size, audio chunk, heads, layers, and context units are transcribed correctly.
- [ ] No architecture diagram is presented as official unless it is official.

## 6. Media gate

- [ ] Every image/video/PDF has a source, owner and capture date, with a documented basis for its intended use.
- [ ] Redistribution permission, license or other applicable basis is recorded; logged-in access alone is not permission to publish.
- [ ] No personal data, private conversations, account identifiers, tokens, cookies or signed access URLs leak through screenshots, metadata or shared source files.
- [ ] Official, converted, cropped, editorial, and generated assets are labeled correctly.
- [ ] Figure legends, axes, footnotes, and model names remain visible.
- [ ] All requested PDF pages were rendered in order and visually checked.
- [ ] Video links and permissions work outside the editor's account.
- [ ] Remote URLs are durable enough for publication, with local masters retained.
- [ ] Filenames and alt text are descriptive rather than generic.
- [ ] No generated image impersonates model output or an official diagram.

## 7. Deployment gate

- [ ] Checkpoint name and quantization match the command.
- [ ] ModelScope model id and download command were verified on the live model card, not inferred from the Hugging Face id or memory.
- [ ] GPU family, count, memory, CUDA/ROCm, nodes, and parallelism are stated.
- [ ] The framework version or source commit is recorded.
- [ ] The exact flags exist in that version.
- [ ] The recipe is verified for the stated hardware or labeled source-only.
- [ ] Weight memory is not presented as total runtime memory.
- [ ] Architectural context is distinguished from tested context.
- [ ] Text/image/audio/video serving support is verified per framework.
- [ ] MTP and model-specific parsers are explained when used.
- [ ] A source installation is not overwritten by a package upgrade.
- [ ] Commands have valid quoting and balanced continuation lines.
- [ ] At least one request path is documented or the omission is intentional.

## 8. Editorial gate

- [ ] First sentence says who released what.
- [ ] Introduction is not an abstract or benchmark dump.
- [ ] One paragraph communicates one main claim.
- [ ] Cases precede technical detail when visual evidence is the main angle.
- [ ] Dense score tables and long notes are kept inline near their claim or moved to `sources/`, not dumped into a separate appendix section.
- [ ] The article contains enough explanation to interpret official images.
- [ ] No empty hype, rhetorical question, or author self-reference remains.
- [ ] Model names, benchmark capitalization, units, and terminology are consistent.
- [ ] Chinese-English spacing is consistent.
- [ ] The same parameter sentence is not repeated in multiple sections.
- [ ] A reference article influenced structure, not copied wording.

## 9. Publication gate

- [ ] The user authorized publication of the final candidate to the intended destination.
- [ ] A ModelScope link, when available, is verified on the live card and placed first. Otherwise, a documented `not_listed` or `not_applicable` exception includes a verified official fallback; `unverified` is not an acceptable absence claim. See `modelscope-integration.md`.
- [ ] All links included in the article were opened during final review; any `pending_weights` state is disclosed rather than presented as a runnable download.
- [ ] Hosted images render at mobile width.
- [ ] Attachments are public or have correct permissions and redistribution rights.
- [ ] Draft images use relative `assets/` paths; replace them with durable hosted URLs when the publication platform requires this. Neither draft nor publishable article contains absolute local filesystem paths.
- [ ] No expiring temporary paths remain.
- [ ] Markdown code fences are balanced and language-tagged.
- [ ] Non-breaking spaces and export artifacts were checked.
- [ ] The final file name is stable and distinguishable from intermediate drafts.
- [ ] Sources and data snapshot date are recorded in `sources/`; they are not required in the article body unless the platform asks for them.

## 10. Failure patterns

### Generated diagram presented as source evidence

Why it fails: it embeds editorial assumptions while appearing official.

Fix: replace it with an official figure or label it as a schematic and disclose its data source.

### Benchmark screenshot becomes stale

Why it fails: official pages may update scores after launch.

Fix: reopen the page before publication, update the image, or add a capture date and explain the snapshot.

### `比肩` escapes its benchmark scope

Why it fails: four close rows do not prove general parity.

Fix: name the evaluated capability categories and write `在上述评测中互有高低`.

### Official demo is overinterpreted

Why it fails: one-shot, tool-assisted, iterative, and fine-tuned demonstrations prove different things.

Fix: state the prompt, tools, iterations, reviewer, and output artifact.

### Architecture translation changes topology

Why it fails: a selected-expert count is mistaken for the candidate pool, or a shared expert is treated as routed.

Fix: return to the primary architecture paragraph and write the flow numerically.

### Training modality becomes inference capability

Why it fails: data exposure is not the same as released input support or evaluated performance.

Fix: separate pretraining data, input interface, output modality, and evaluation.

### Active parameters become “small deployment”

Why it fails: all weights still need storage or distributed loading.

Fix: cite checkpoint size and runtime memory independently.

### Framework compatibility becomes a generic architecture claim

Why it fails: `Transformer` is an architecture family; `Transformers` is a software library.

Fix: name the exact library and engine integrations.

### Dynamic cookbook copied without environment

Why it fails: generated recipes change with hardware, strategy, and version.

Fix: record the selected matrix cell, verified badge, version/commit, hardware, and access date.

### Reference article is imitated too literally

Why it fails: the new model's evidence is forced into another article's claims and distinctive wording.

Fix: reuse only macro-structure, pacing, and formatting conventions.
