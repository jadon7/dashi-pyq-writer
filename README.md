# dashi-pyq-writer：大师朋友圈文案 Skill

让 AI 按定好的写法撰写「大师的AI小灶」大师的朋友圈：把推特上的热门 AI 内容或大师自己的观点，写成像大师亲身体会的朋友圈，结尾自然带出线下课。

## 怎么装

- **Claude Code**：克隆到个人 skills 目录（也可以放进项目里的 `.claude/skills/`）。

  ```bash
  git clone https://github.com/jadon7/dashi-pyq-writer.git ~/.claude/skills/dashi-pyq-writer
  ```

- **Claude 网页版 / 桌面版**：从 [Releases](https://github.com/jadon7/dashi-pyq-writer/releases) 下载 `dashi-pyq-writer.skill`，在设置的 Skills 里上传。
- **其他 Agent**：把仓库放进它的 skills 目录，或者直接让它先读 `SKILL.md`。

## 怎么用

把排期时间和原帖（推特链接、原文或截图）给 AI，例如：

> 用 dashi-pyq-writer，给 11 月 20 日 12:00 和 18:00 各写一条朋友圈，原帖分别是 https://x.com/... 和 https://x.com/...

每条会交出正文、第一条评论和待核事项。

## 文件说明

| 文件 | 内容 |
| --- | --- |
| `SKILL.md` | 这类朋友圈是什么、四段结构、最容易写错的地方、怎么写 |
| `references/voice.md` | 大师的口吻，和可以用的大师亲历清单 |
| `references/course.md` | 课程信息、对外课纲、结尾怎么写。开新一期时先更新这一页 |
| `references/rules.md` | 去 AI 味的硬禁令、「我」字指标、微信敏感点、灰色题材处理 |
| `references/review-notes.md` | 三轮审稿意见的原意，和开头的包装方式 |
| `references/examples.md` | 改前改后的对照和定稿示例 |
| `scripts/check.py` | 可选的自查脚本：禁用句式、「我」字数量、敏感词、字数（只需 Python 3） |

## 需要更新时

- 新一期课程：改 `references/course.md`。
- 大师有了新的经历或观点：照他推特原文补进 `references/voice.md` 的清单。
- 又有新的写法要求：补进 `references/review-notes.md`，必要时同步 `SKILL.md`。

## 致谢与许可

去 AI 味的规则整理自数字生命卡兹克开源的写作 Skill [human-writing](https://github.com/KKKKhazix/human-writing)（MIT）。本仓库以 MIT 许可开源，见 [LICENSE](LICENSE)。
