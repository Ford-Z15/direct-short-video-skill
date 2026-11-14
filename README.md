# 抖音短视频编导专家

一个面向零基础用户的短视频编导 Agent Skill。收集业务事实后，由智能体完成定位、选题、口播、分镜、拍摄、剪辑、发布与风险审查，并支持销售脚本、直播和付费投放规划。

## 仓库内容

```text
skills/direct-short-video/
├── SKILL.md                  # 触发说明与执行入口
├── references/
│   ├── prompts/              # 访谈、分析、主流程与合规审查
│   └── knowledge/            # 13 个按需读取的方法模块，97 条方法
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
