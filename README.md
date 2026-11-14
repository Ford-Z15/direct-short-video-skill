# 抖音短视频编导专家

一个面向零基础用户的短视频编导 Agent Skill。收集业务事实后，由智能体完成定位、选题、口播、分镜、拍摄、剪辑、发布与风险审查，并支持销售脚本、直播和付费投放规划。

## 背景

本 Skill 的方法体系基于国内头部短视频博主培训课程提炼打造，覆盖从市场调研、账号定位、选题策划、脚本写作、分镜设计到拍摄剪辑、发布运营和风险审查的完整编导链路，共 14 个方法模块、103 条可执行方法。你不需要懂编导术语，智能体会把专业判断做完，你只需要回答关于自己业务的事实问题。

## 工作流程

你和 Skill 的协作按下面的循环进行，每一轮对话只做一小步：

```text
第 1 步  收集信息
        智能体用大白话问你业务事实：你卖什么、账号想达到什么、
        拍给谁看、有什么拍摄条件。每次最多问两个问题。

第 2 步  市场调研（做定位时）
        你选调研方式：人工采集对标账号和评论 + AI 分析（推荐），
        或 AI 直接出报告（会说明自动调研的限制）。
        调研后得到市场分析报告，以及三个分优先级的定位方向，
        由你选一个。

第 3 步  编导判断
        智能体把事实整理成专业判断：内容定位、选题方向、
        脚本结构。它会明确区分「你确认的事实」和「它的假设」。

第 4 步  产出成品
        按任务输出可直接使用的成品：选题、口播文案、分镜表、
        拍摄和剪辑要求、发布文案与话题。

第 5 步  风险审查
        交付前自动做违禁词初筛（内置词库 + 语义审查），
        标记风险并给出改写建议。初筛不能替代你最终确认平台规则。

第 6 步  交付与保存
        对话中先给你能直接用的成品，再附完整文件位置；
        每次任务保存到 outputs/<项目名>/<任务名>/，不覆盖历史。
```

每一步都可以打断和纠正：信息给错了就重新回答，方向不对就直接说「换个思路」，智能体不会替你编业务事实。

## 仓库内容

```text
skills/direct-short-video/
├── SKILL.md                  # 触发说明与执行入口
├── references/
│   ├── prompts/              # 访谈、分析、主流程与合规审查
│   └── knowledge/            # 14 个按需读取的方法模块，103 条方法
├── scripts/
│   ├── check_copy.py         # 文案风险词初筛
│   └── validate_skill.py     # Skill 完整性校验
├── data/                     # 风险词库与维护说明
└── tests/fixtures/           # 扫描测试样例
```

公开版不包含原始文稿、逐字清洗稿或内部溯源索引。原工程中的内部验证材料不应直接上传到公开仓库。

## 安装为 Agent Skill

将整个 `skills/direct-short-video/` 文件夹复制到宿主使用的 Skills 目录，或导入发布包中的 `direct-short-video.skill`。不同宿主的目录和导入入口可能不同，以对应版本的说明为准。

安装后可直接提出：

- “帮我为一家社区宠物店写第一条视频，只能用手机拍。”
- “把这段口播改得自然一些，并补上分镜和剪辑要求。”
- “根据这些真实后台数据，帮我复盘下一条应该怎么改。”

## 在 WorkBuddy 中使用

支持 Agent Skills 的版本可按其技能入口导入本 Skill。

如果当前版本不支持技能导入：

1. 将 `direct-short-video/` 文件夹完整复制到工作目录。
2. 把 `SKILL.md` 的内容放入智能体自定义指令，或作为新对话的首条指令。
3. 确保智能体能读取同目录下的 `references/`、`data/` 和 `scripts/`。
4. 没有文件能力时仍可生成对话成品，但不得声称已经保存文件。

## 在 Claude / Codex 中使用

**方式一：直接发给 AI 一行指令（最简单）**

新开对话，把下面这段原样发给 Claude 或 Codex：

```text
请从 GitHub 仓库 https://github.com/Ford-Z15/direct-short-video-skill 获取 skills/direct-short-video 目录的全部文件到当前工作目录，阅读其中的 SKILL.md 并严格按照它作为「抖音短视频编导专家」技能与我协作。
```

AI 会自己完成下载和读取，之后直接用大白话提需求即可。

**方式二：命令行安装（Claude Code 用户）**

一行命令装到 Claude Code 技能目录：

```bash
mkdir -p ~/.claude/skills && git clone --depth 1 https://github.com/Ford-Z15/direct-short-video-skill.git /tmp/dsv && cp -r /tmp/dsv/skills/direct-short-video ~/.claude/skills/ && rm -rf /tmp/dsv
```

Windows（PowerShell）：

```powershell
git clone --depth 1 https://github.com/Ford-Z15/direct-short-video-skill.git $env:TEMP\dsv; Copy-Item -Recurse $env:TEMP\dsv\skills\direct-short-video $HOME\.claude\skills\; Remove-Item -Recurse $env:TEMP\dsv
```

装好后重启会话，技能自动生效。

**方式三：手动安装**

下载 Release 中的 `direct-short-video.skill` 或仓库 `skills/direct-short-video/` 文件夹，解压后放到宿主支持的技能目录，或将 `SKILL.md` 全文粘贴为自定义指令。

## 本地验证

在 `skills/direct-short-video/` 目录运行：

```bash
python scripts/validate_skill.py
python scripts/check_copy.py tests/fixtures/compliance_sample.txt
```

词库扫描仅用于初筛，不能替代语义、事实、证据和当前平台规则审查。

## 发布前检查

- 确认你拥有公开这些方法、文案和词库内容的权利。
- 不上传原始培训文稿、用户资料、账号数据或任务成品。
- 当前未指定开源许可证；公开仓库不等于授权他人自由复制或再发布。需要开放使用时，请由仓库所有者明确选择许可证。
