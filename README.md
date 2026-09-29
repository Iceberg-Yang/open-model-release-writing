# Open Model Release Writing

面向中文模型发布文章的 Agent Skill：先核对证据，再组织内容，最后审校。

把模型卡、论文、官方博客、评测表和部署文档整理成面向开发者的公众号稿、技术解读或发布简讯，减少事实错配、夸大比较和不可复现的部署说明。

[魔搭 Skill 页面](https://modelscope.cn/skills/icebergyang/open-model-release-writing) · [Agent 指令入口](SKILL.md) · [完整教学示例](references/worked-example.md)

> 这是写作与审核工作流，不是模型推理服务，也不会自动发布文章。附带的 Python 脚本只做启发式检查；检查通过不代表事实、素材授权或部署命令已验证。

## 适合做什么

| 场景 | 工作内容 |
| --- | --- |
| 新模型发布稿 | 从官方材料提炼发布信息，组织导语、效果案例、技术解读、性能与推理部分 |
| 标题与导语 | 限定“领先”“比肩”“SOTA”等表述的比较范围，避免标题超出正文证据 |
| 技术与评测解读 | 区分总参数与激活参数、输入与输出模态、不同版本和评测设置 |
| 官方素材整理 | 记录图片、视频、PDF 的来源、转换方式、复用依据和隐私检查结果 |
| 下载与部署说明 | 核对模型 ID、权重状态、框架版本、硬件条件和特殊参数 |
| 现有稿件审校 | 按阻断、重要、次要三个等级列出问题，并给出证据缺口和修改建议 |

默认采用客观的第三方技术写作口吻。短讯、完整公众号稿、技术解读和部署教程按实际需求选择结构，不强行套用同一种篇幅。

## 安装与使用

### 环境要求

- **写作与资料核验**：使用能够加载 Agent Skills 的客户端；在线核验需要联网检索能力，保存稿件需要文件访问能力。
- **本地审校脚本**：Python 3.10+，仅使用标准库，无需安装 Python 依赖，也不访问网络。
- **可选能力**：浏览器自动化、PDF 渲染等由客户端提供，本仓库不内置这些服务。缺少能力时应注明未核验，不能声称已经完成。

### 获取 Skill

克隆仓库，或从[魔搭页面](https://modelscope.cn/skills/icebergyang/open-model-release-writing)下载、按页面说明安装：

```bash
git clone https://github.com/Iceberg-Yang/open-model-release-writing.git
```

手动安装时，将整个 `open-model-release-writing` 文件夹放入客户端支持的 Skills 目录，不能只复制 `SKILL.md`。例如，Qoder 的用户级目录为 `~/.qoder/skills/`，Codex 的用户级目录为 `~/.codex/skills/`；以所用客户端的实际安装规则为准。

已有同名 Skill 时先备份或比较差异，不要直接覆盖自己的修改。安装后重新加载 Skills 或重启会话，再在对话中指定使用 `open-model-release-writing`。

`agents/openai.yaml` 是可选的 Codex 展示元数据，其他客户端可忽略。本文用于仓库导览；Agent 的执行规则以 [SKILL.md](SKILL.md) 及其引用文件为准。

### 提问示例

**从官方材料写一篇发布稿：**

```text
使用 open-model-release-writing，根据我提供的官方模型卡、技术报告和博客，
写一篇面向开发者的中文公众号稿。
先整理事实台账，再写正文；优先使用有复用依据的官方素材。
魔搭下载地址需要现场核验，没有核实的信息请明确标注。
只生成本地草稿，不要发布。
```

**审核已有文章，不直接改文件：**

```text
使用 open-model-release-writing 审核 article.md。
重点检查标题是否夸大、评测分数是否对应正确模型、部署条件是否完整。
先列出问题位置、严重程度和来源依据，不要直接修改文章。
```

**只补下载与推理部分：**

```text
根据我提供的官方部署文档，补写模型下载与推理部分。
核对精度、GPU 型号和数量、框架版本、上下文限制以及特殊参数。
如果没有对应 GPU，明确写“按官方资料核对，未实际执行”，不要虚构实测结果。
```

## 工作流与产物

```text
确定范围 → 收集一手来源 → 建立事实台账 → 选择文章角度
         → 整理可用素材 → 撰写正文 → 审核评测与部署 → 最终检查
```

按需生成以下内容，不要求每次把所有模板都填一遍：

- **文章草稿**：中文 Markdown，图片在草稿中使用相对 `assets/` 路径。
- **来源与事实记录**：在文章旁的 `sources/` 中记录来源位置、访问日期、版本、推导过程和限制条件。
- **素材清单**：记录素材归属、复用依据、裁剪或转换、脱敏状态；工作证据目录不默认公开。
- **评测或部署记录**：保留比较条件、命令来源、硬件配置，以及“仅核对来源”或“实际执行”的区别。
- **审核意见**：标明阻断问题、未核验项和仍需补充的证据。

可先阅读[虚构教学示例](references/worked-example.md)，了解“材料 → 事实台账 → 候选正文 → 审校”的全过程。示例中的团队、模型、分数和链接仅用于教学，不是真实发布信息，也没有进行模型或 GPU 测试。

## 单独运行 Markdown 审校

无需加载 Skill，也可以在仓库根目录对已有文章运行检查。先准备 `article.md`，或将命令中的路径替换为自己的稿件路径。

```bash
python3 scripts/audit_markdown.py article.md --fail-on major
```

需要机器可读输出时：

```bash
python3 scripts/audit_markdown.py article.md --fail-on major --format json
```

常见检查包括代码围栏、一级标题、夸大措辞、临时或绝对本地链接、术语、部署版本与硬件提示。围栏内的普通文字不会被当作正文检查，但部署与本地链接等信号仍会扫描全文。

| 参数 | 默认值 | 含义 |
| --- | --- | --- |
| `--modelscope required\|optional` | `required` | 是否报告缺少魔搭模型链接；不验证链接真实性或上架状态 |
| `--fail-on blocker\|major\|minor` | `blocker` | 达到该严重程度或更高时返回失败；发布前建议使用 `major` |
| `--format text\|json` | `text` | 文本或 JSON 输出 |

仅在文章不要求魔搭渠道，或有核查依据表明模型未上架时，使用：

```bash
python3 scripts/audit_markdown.py article.md --modelscope optional --fail-on major
```

例外需要记录范围、日期、理由及已核验的官方替代来源。页面打不开不等于未上架；`optional` 只跳过缺少链接的提示，不免除对已有魔搭链接或下载命令的核验。

退出码：`0` 表示没有问题达到所选阈值，`1` 表示达到阈值，`2` 表示输入或用法错误。JSON 中的 `passed` 也仅表示阈值检查结果。默认阈值为 `blocker`，因此默认返回 `0` 时仍可能存在重要问题。

查看完整参数或运行回归测试：

```bash
python3 scripts/audit_markdown.py --help
python3 -B -m unittest discover -s tests -v
```

## 规范与资源

| 文件 | 内容 |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent 入口、任务路由与证据优先工作流 |
| [来源与事实核验](references/source-and-fact-audit.md) | 一手来源、事实分类、比较范围与评测条件 |
| [文章结构与风格](references/article-structure-and-style.md) | 标题、导语、案例、技术解读及中文写作规范 |
| [素材处理](references/media-and-assets.md) | 图片、视频、PDF 的溯源、复用依据与视觉检查 |
| [魔搭结合规范](references/modelscope-integration.md) | 模型卡核验、下载渠道与未上架时的处理 |
| [部署审核](references/deployment-audit.md) | 环境矩阵、版本固定、显存与上下文限制 |
| [审核关卡](references/review-gates.md) | 事实、技术、素材、部署与发布检查清单 |
| [记录模板](references/templates.md) | 事实台账、来源表、素材表、部署记录与审核报告 |
| [教学示例](references/worked-example.md) | 明确标注为虚构的端到端案例 |
| [审校脚本](scripts/audit_markdown.py) / [回归测试](tests/test_audit_markdown.py) | 标准库 CLI 与测试用例 |

## 使用边界

本 Skill 不提供事实正确率或模型能力保证，不把官方演示当作独立评测，不把开放权重自动称为开源，也不把来源核对当作 GPU 实测。拿不到证据时应收窄表述、注明限制或省略相关内容。

能够访问素材不等于有权转载。发布前需检查许可证或其他复用依据、个人信息、账号信息与签名链接；不得把凭据或受限资料放入公开文章包。撰写或审校请求不等于公开发布授权，最终发布需另获明确授权。

本仓库当前未声明开源许可证，不默认适用 MIT、Apache-2.0 等许可。文章引用的模型、代码与素材仍需分别遵守其权利人的许可和使用条件。
