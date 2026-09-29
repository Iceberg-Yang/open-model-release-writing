# ModelScope Integration

ModelScope (魔搭) is the home platform for these articles. Treat it as the primary
download and deployment channel, not as a secondary mirror. This file fixes the
conventions that make a release article recognizably a 魔搭公众号稿.

## Contents

1. Hard rule: verify the download command on the model card
2. Link block order
3. Standard download command
4. ModelScope SDK and pipeline inference
5. Series, papers, and documentation links
6. Ecosystem and trust anchors
7. Closing framing
8. Platform notes for 微信公众号

## 1. Hard rule: verify the download command on the model card

Never write a ModelScope model id, namespace, capitalization, or download command
from memory, from the Hugging Face id, or by guessing the organization name.

Before publishing any `modelscope download` command:

1. Open the actual ModelScope model card page (`https://modelscope.cn/models/{namespace}/{name}`).
2. Confirm the page exists and the namespace and model name match exactly, including
   capitalization and any version suffix.
3. Copy the model id from the page or from the card's own download snippet rather than
   reconstructing it.
4. Confirm the weights are actually present. If the card still says weights are coming
   soon, or only some files are uploaded, state that and mark the command as pending
   instead of presenting it as runnable.
5. Record the access date and the card snapshot in `sources/source-register.md`.

The Hugging Face id and the ModelScope id are frequently different (different
namespace, different capitalization, a re-uploader account, or a renamed model).
A correct Hugging Face path is never evidence of a correct ModelScope path. If the
model is not on ModelScope, say so and link the official source instead of inventing
a ModelScope id. Record `not_listed` with the checked search scope, date and official
fallback URL in the source registry. For non-ModelScope editorial work, record
`not_applicable` and the agreed scope. An inaccessible page is `unverified`, not proof
that the model is absent. A card with incomplete weights is `pending_weights`; do not
present its download command as a tested runnable recipe.

Only documented `not_listed` or `not_applicable` cases may omit the ModelScope link
and use the checker's `--modelscope optional` option. Every ModelScope link or command
actually included still requires live verification. Missing a ModelScope listing is
not itself a blocker when the official fallback satisfies the article's purpose.

This is a publication blocker: an unverified or guessed download command fails the
review even if the rest of the article is sound.

## 2. Link block order

Place the link block right after the introduction, before the first section. Use the
`●` bullet. Put the verified ModelScope download first when available; for a documented
exception in section 1, omit that slot and put the official model card first:

```text
● 模型下载（魔搭）：https://modelscope.cn/models/{namespace}/{name}
● 官方模型卡 / Hugging Face：...
● GitHub：...
● 技术报告 / 官方博客：...
```

Only list links that were opened and verified. Drop a slot rather than padding it.

## 3. Standard download command

Use the ModelScope CLI as the default download path:

```bash
pip install -U modelscope

modelscope download \
  --model {namespace}/{name} \
  --local_dir ./{name}
```

The `{namespace}/{name}` value must come from the verified model card (section 1).
When a model needs companion weights (a base model, a VAE, an external geometry or
text encoder), give a separate verified `modelscope download` command for each, and
say which ones are not bundled and must be obtained elsewhere under their own license.

## 4. ModelScope SDK and pipeline inference

When the model is callable through the ModelScope pipeline SDK, prefer showing that
path for quick inference, and name the exact task, model id, and output keys:

```python
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

predictor = pipeline(Tasks.{task_name}, model='{namespace}/{name}', device='cpu')
result = predictor({'input': 'example.wav'}, output_path='output.wav')
```

If the repository ships native code, note that `trust_native_code=True` should only
be enabled for repositories the reader trusts, and say so explicitly. Record any
minimum SDK version (for example ModelScope greater than a specific release) and
whether it requires the master branch before a PyPI release.

## 5. Series, papers, and documentation links

- Model series and families: link the ModelScope collection (合集) page when one exists.
- Technical reports hosted on ModelScope: link `https://modelscope.cn/papers/{id}`.
- In-repo documentation: link the file view, for example
  `https://modelscope.cn/models/{namespace}/{name}/file/view/master/docs/installation.md`,
  rather than pasting a long doc into the article.
- Ecosystem tooling maintained by ModelScope (for example DiffSynth-Studio for video
  models): name it and link the official repository when it is part of the run path.

## 6. Ecosystem and trust anchors

When the source supports it, ground the model in the ModelScope ecosystem:

- Download counts on ModelScope as a trust anchor, only when the number is read from
  a live page and dated, never estimated.
- Community projects, Skills (for example on ClawHub), and hosted APIs (for example
  百炼) that already wrap the model or its family.
- Related models in the same series that readers can combine.

Keep ecosystem claims sourced. A download count or a community project list is a
dynamic fact: record the access date.

## 7. Closing framing

The house closing move ties the release back to ModelScope as the place where research
becomes usable: from a method in a paper, to a model that can be downloaded and called
on 魔搭, to a component that can be embedded in a real workflow. Keep it to one or two
sentences and grounded in what was actually released. Omit this framing for
`not_listed`, `not_applicable` or `unverified` cases; do not imply ModelScope hosting
or usability without evidence. Do not add a separate 总结 section unless a license
or usage boundary genuinely needs restating.

## 8. Platform notes for 微信公众号

- 微信公众号 cannot embed a local mp4 reliably. For video cases, keep a poster frame
  plus a caption in the draft, and re-upload the video to the platform or a durable
  host before publishing. Mark each video as a hosted asset in `sources/asset-manifest.md`.
- Article images must use relative `assets/` paths in the draft and be replaced with
  hosted URLs at publish time. No absolute local filesystem paths in the deliverable.
