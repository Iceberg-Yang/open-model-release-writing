# Media and Asset Workflow

## Contents

1. Asset priority
2. Provenance manifest
3. Official figures and screenshots
4. PDFs and multi-page artifacts
5. Video and interactive demos
6. Generated visuals
7. Storage, naming, and publication durability
8. Visual quality checks

## 1. Asset priority

Use this order:

1. Official original asset supplied with the release.
2. Lossless local copy of an official web asset.
3. Screenshot of an official interactive figure or table.
4. Conversion of an official PDF/video into publishable frames.
5. Clearly labeled editorial diagram.
6. Generated illustration only when explicitly requested.

For a fact-heavy model release article, do not replace an available official figure with a generated approximation.

## 2. Provenance manifest

Track every asset with:

- Local filename.
- Asset type.
- Source page and direct asset URL.
- Owner or publisher.
- Capture/download date.
- Original caption.
- Conversion: screenshot, crop, resize, frame extraction, PDF render, or none.
- Pages or timestamps included.
- Whether labels or legends were altered.
- Intended article location.
- Publication status.
- License, permission or other documented basis for the intended reproduction, including required attribution.
- Privacy/redaction review and whether the source copy may be shared publicly.

Never call an image official when it was recreated, translated, recolored, or relabeled by the editor.

Access is not redistribution permission. Before reproducing an asset, verify the owner's
terms or other applicable basis; when unclear, link to the source or request permission
instead of republishing the file. Do not upload restricted source snapshots as part of
a public article bundle. Treat `sources/` as working evidence, not automatically public.

For logged-in pages, capture only material the user is authorized to access and share.
Inspect screenshots, captions, metadata and URLs for personal data, internal records,
account details, tokens, cookies and signed query parameters. Crop or redact irrelevant
private information without removing technical conditions; disclose material edits.
If redaction would distort the evidence, omit the asset and explain the limit. Keep
only permitted local masters and re-check the public copy separately.

## 3. Official figures and screenshots

### Prefer original files

Download the original PNG, SVG, WebP, or PDF when accessible. Keep its original aspect ratio and a lossless master.

### Screenshot only when necessary

Use screenshots for interactive charts, canvas graphics, dynamically generated tables, or authenticated pages. Capture enough context to preserve:

- title;
- axes and scale;
- model legend;
- footnotes;
- date or version when visible.

Do not crop away conditions that change the meaning. Do not translate model names inside a chart unless the article clearly labels the result as an edited figure.

### Captions

Use captions such as:

> 图：Company A 官方 Figure 2。各项指标统一映射到 0–100，缺失成绩按官方图示规则处理。

Captions should state the source and any normalization, crop, or edit relevant to interpretation.

## 4. PDFs and multi-page artifacts

When an official case is a PDF:

1. Save the original PDF.
2. Inspect page count, dimensions, metadata, and embedded text.
3. Render every requested page at one resolution and format.
4. Use deterministic names such as `page-01.png`.
5. Verify each page visually for clipping, missing fonts, black boxes, image corruption, and page-number loss.
6. Store rendered pages in a dedicated folder.
7. Do not insert them into the article unless requested.

If the user wants “all pages,” do not substitute a cover montage. If the user wants only representative pages, select them by content role and record the omitted pages.

Use the PDF processing skill when available.

## 5. Video and interactive demos

For each video, record:

- official source;
- whether it is a full run, edited demo, or looping excerpt;
- prompt and result relationship;
- tool access;
- iteration count;
- reviewer or human involvement;
- whether audio is necessary for comprehension.

Create a poster frame only when needed. Do not imply a video proves latency, autonomy, or reliability unless the source measures it.

For publishing platforms that cannot embed local video, provide a durable attachment or hosted link and verify access permissions.

## 6. Generated visuals

Generate a visual only when:

- the user explicitly requests one;
- no official visual exists;
- a conceptual relationship materially benefits from illustration;
- the result can be labeled `示意图`.

Never generate:

- benchmark charts from remembered values;
- an architecture diagram presented as official;
- fake product screenshots;
- output examples attributed to the model without running it.

If an editorial chart is created from official data, retain the data table and source, label the chart as editorial, and verify every plotted value.

## 7. Storage, naming, and publication durability

Keep a fixed per-model layout: the article as `{model}-公众号稿.md`, official media under
`assets/official-figures/` and `assets/official-cases/`, and backing artifacts under
`sources/` (claim ledger, source register, asset manifest, model-card and docs snapshots).

Reference every image and video in the draft with a relative `assets/...` path. Never use an
absolute local filesystem path in the article; it breaks on any other machine and fails the
publication gate. Replace relative paths with hosted URLs at publish time.

Use descriptive filenames:

- `model-official-cover.png`
- `model-relative-attention-official.png`
- `design-arena-2026-07-15.png`
- `breakfast-magazine/page-01.png`

Avoid `image.png`, `screenshot-final-2.png`, and ambiguous names.

Keep a local source copy even when the final article uses OSS, CDN, or document-platform URLs. Remote links may expire, require login, or change crop parameters.

Check:

- public accessibility;
- hotlink policy;
- URL expiration;
- access authentication;
- image compression;
- mobile width;
- attachment permissions.

## 8. Visual quality checks

Before delivery verify:

- expected asset count;
- identical page dimensions for a set;
- readable labels at mobile width;
- no clipped legends or footnotes;
- correct page order;
- no duplicate or near-duplicate images;
- no accidental translation in the image itself;
- caption matches the actual source;
- screenshot still matches the current official page;
- article does not contain a local relative path when the publication platform requires hosted URLs.

Treat visual QA as part of fact checking: a wrong crop can create a false claim even when the underlying source is correct.
