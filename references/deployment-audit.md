# Deployment Audit

## Contents

1. Define deployment honestly
2. Source hierarchy
3. Environment matrix
4. Command validation
5. Parameters that require explanation
6. Memory and context
7. Framework and version drift
8. Common deployment errors

## 1. Define deployment honestly

Distinguish:

- direct local inference on one machine;
- multi-GPU local server;
- multi-node private cluster;
- managed API or serverless provider;
- hosted fine-tuning service;
- quantized community build.

Do not label a multi-node, hundreds-of-gigabytes setup as ordinary consumer `本地部署`. Use `多 GPU 部署`, `本地集群部署`, or `私有化部署`.

## 2. Source hierarchy

Use:

1. Model developer's model card and release page.
2. Inference framework's model-specific official documentation or integration PR.
3. Verified hardware recipe or Cookbook.
4. Checkpoint repository instructions.
5. Community recipes only when clearly labeled and independently tested.

Do not assemble a command from unrelated generic flags merely because the CLI accepts them.

## 3. Environment matrix

Record before writing commands:

| Field | Example |
|---|---|
| Checkpoint | `org/model-NVFP4` |
| Weight precision | BF16 / FP8 / NVFP4 / GGUF |
| GPU architecture | Hopper / Blackwell / AMD CDNA |
| GPU model and count | B200 × 8 |
| Memory per GPU | 180 GB |
| Nodes | 1 or more |
| CUDA/ROCm | exact version |
| Framework | vLLM / SGLang / Transformers |
| Version or commit | pinned |
| Tensor parallelism | TP=8 |
| Other parallelism | DP/EP/PP |
| Context tested | 32K / 256K / 1M |
| Modalities tested | text/image/audio/video |
| API protocol | OpenAI-compatible or custom |

Do not publish a command until the checkpoint and hardware are mutually supported.

## 4. Command validation

For each command:

1. Verify the repository name and capitalization. For a ModelScope download, open the live
   ModelScope model card and copy the exact model id; never infer it from the Hugging Face id
   or memory (see `modelscope-integration.md`).
2. Verify local path versus remote model ID.
3. Verify installation method and Python version.
4. Pin a release or commit for source builds when reproducibility matters.
5. Confirm all environment variables are documented.
6. Confirm every CLI flag exists in that framework version.
7. Check line continuations and JSON quoting.
8. Confirm port, host, model name, and endpoint.
9. Run a help/config validation or real launch when hardware is available.
10. Provide one minimal request to test the server when useful.

If hardware is unavailable, say the command is source-verified but not locally executed.

Avoid installing a package from source and then immediately overwriting it with a PyPI upgrade.

## 5. Parameters that require explanation

Explain only unusual or consequential parameters.

### MTP

Multi-Token Prediction uses a model-provided draft head to propose several future tokens before the target model verifies them. Clarify:

- `num_speculative_tokens=8` is the number of proposed tokens per speculative step, not automatically the number of draft layers;
- speedup depends on acceptance rate and workload;
- it adds memory and implementation requirements;
- it should not be described as changing model quality unless the source reports that effect.

### Tensor parallelism

`TP=8` means model tensors are sharded across eight participating GPUs. It is not a universal hardware requirement and must match the verified topology.

### Reasoning and tool parsers

Model-specific parsers separate reasoning content, final text, and tool-call structures. Do not imply they enable reasoning or tools by themselves; they decode the model's output protocol.

### Quantization flag

A flag such as `modelopt_fp4` may load an already quantized checkpoint. Do not describe it as performing quantization at startup unless it does.

### Attention, MoE, and cache backends

Hardware-specific kernels such as FlashAttention, FlashInfer, or TensorRT-LLM backends may require a particular GPU architecture and CUDA build. State the validated environment.

### Unified or hierarchical cache

Explain cache flags only when they affect long context, prefix reuse, memory tiering, or accuracy. Avoid turning internal implementation names into model architecture claims.

## 6. Memory and context

Separate:

- checkpoint size;
- approximate weight VRAM;
- runtime framework overhead;
- activation memory;
- KV or recurrent-state cache;
- multimodal preprocessing memory;
- speculative-decoding draft memory;
- concurrency headroom.

An official statement that NVFP4 requires about 600 GB does not guarantee that eight 80 GB GPUs are operationally sufficient. Reserve memory for caches and runtime.

Separate architectural maximum context from tested and hosted limits. A model may support 1M tokens while a hosted service exposes 64K/256K or a balanced local recipe tests less.

When a compressed KV cache doubles capacity, report latency and accuracy tradeoffs if the source does.

## 7. Framework and version drift

Deployment facts change quickly. Before publication:

- reopen official docs;
- check latest model-specific page;
- compare command flags with the current CLI;
- note whether the recipe is static or generated dynamically;
- save the selected hardware/strategy state;
- record access date;
- pin source installs.

If a documentation page has a `Verified / Not Verified` badge, do not call an auto-derived combination verified.

## 8. Common deployment errors

- Writing `支持 Transformer 架构` instead of `已接入 Hugging Face Transformers`.
- Calling active parameters the memory requirement.
- Omitting that an FP4 checkpoint targets Blackwell.
- Treating a framework's text path as proof of image/audio support.
- Combining flags from different framework versions.
- Copying an eight-GPU recipe onto another GPU family.
- Omitting multi-node launch requirements for a checkpoint that cannot fit one node.
- Calling a community 1-bit quantization the official checkpoint.
- Failing to explain MTP while advertising its speedup.
- Giving `git clone main` commands without a verification date or commit.
- Claiming million-token serving without memory and tested-context evidence.
