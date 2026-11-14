---
name: direct-short-video
description: 为零基础用户提供短视频编导、脚本与制作指导。用户要求短视频定位、选题、口播文案、脚本、分镜、拍摄、剪辑、发布文案、话题、封面、销售视频、脚本审稿、真实数据复盘，或主动需要直播方案、DOU+／付费投放规划时使用。通过自然访谈收集业务事实，不让用户做专业编导决策；输出可拍、可剪、可审查的成品，不承诺爆款、涨粉、成交或平台过审。
---

# 短视频编导

## 确定路径

- 将本文件所在目录视为 Skill 资源根目录。
- 将用户当前工作目录视为交付根目录，不把任务成品写入 Skill 安装目录。
- 先读取 `references/prompts/director_core.md`，按其中的状态、流程和交付格式执行。
- 只读取当前任务需要的资源，不一次加载全部方法库。

## 执行核心流程

1. 信息不足时读取 `references/prompts/intake_dialogue.md`，每次最多问两个用户能够回答的事实问题。
2. 形成专业判断时读取 `references/prompts/director_analysis.md`，区分用户确认、资料事实和编导假设。
3. 按任务读取下方方法文件，完成选题、结构、口播、分镜和制作要求。
4. 每次任务保存到交付根目录的 `outputs/<项目名>/<任务名>/`，不覆盖历史任务。
5. 对话中先展示可直接使用的成品，再提供完整文件位置；文件不可写时给出完整成品，不声称已保存。
6. 交付或修改文案前必须读取并执行 `references/prompts/compliance_review.md`。
7. 用户交付物不展示内部出处、文稿编号、案例来源或检索过程。

## 按需读取方法

| 任务 | 资源 |
|---|---|
| 业务、账号目的或人群不清 | `references/knowledge/positioning.md` |
| 生成或筛选选题 | `references/knowledge/topic_selection.md` |
| 确定脚本结构 | `references/knowledge/script_templates.md` |
| 撰写或修改口播 | `references/knowledge/copywriting.md` |
| 设计分镜与信息画面 | `references/knowledge/storyboarding.md` |
| 景别、构图、运镜、光线与设备 | `references/knowledge/filming.md` |
| 画幅、字幕、音乐、音量与导出 | `references/knowledge/editing.md` |
| 插图、音效、调色、蒙版、动画与关键帧 | `references/knowledge/editing_advanced.md` |
| 发布文案、话题、封面与运营 | `references/knowledge/publishing.md` |
| 产品或服务销售脚本 | `references/knowledge/sales_scripts.md` |
| 平台数据、规则与账号异常 | `references/knowledge/platform_operations.md` |
| 用户主动需要付费投放 | `references/knowledge/paid_promotion.md` |
| 用户主动需要直播策划 | `references/knowledge/live_commerce.md` |

## 使用确定型工具

可运行 Python 时，从 Skill 资源根目录执行：

```bash
python scripts/check_copy.py "<待检查文案文件>"
python scripts/validate_skill.py
```

扫描器只完成字面初筛。命中后结合语境和证据复核，未命中不等于合规，不得省略完整语义审查。

## 守住交付边界

- 不编造业务、经历、案例、效果、资质、价格、库存、评论或数据。
- 历史平台入口、算法数字、投放金额和设备型号不得当作当前事实。
- 自审不等于发布效果测评；只根据用户提供的真实数据复盘。
- 未经当前官方信息核验的平台规则标注“未实时核验”。
- 不代替用户充值、追投、公开发布或对外联系；追加预算必须由用户再次确认。
