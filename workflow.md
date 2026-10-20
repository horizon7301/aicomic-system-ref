# AI漫剧制作工作流 · 谁做什么

> 你 = Horizon（决策 / 账号 / 最终发布）  
> 我 = Horizon-comic（写稿、分镜、工具、生成、导出）

```mermaid
flowchart TD
  A[1. 选题与设定<br/>genre / 人设 / 世界观] --> B[2. 系列圣经]
  B --> C[3. 单集分镜 + 对白]
  C --> D{你审核?}
  D -->|改| C
  D -->|过| E[4. 角色参考图 + 空景背景<br/>小额生图费用]
  E --> F{你审核画风?}
  F -->|改| E
  F -->|过| G[5. 按分镜批量出静帧面板]
  G --> H[6. 系统UI叠加 + 配音字幕<br/>edge-tts / 剪映模板]
  H --> I[7. 轻动效<br/>推拉 / 抖动 / 1–2个英雄镜头]
  I --> J[8. 导出剪映草稿 / 成片]
  J --> K{你终审?}
  K -->|改| G
  K -->|过| L[9. 你发布<br/>抖音 + 视频号]
  L --> M[10. 看数据 → 下一集]

  style A fill:#1a3a5c,color:#fff
  style B fill:#1a3a5c,color:#fff
  style C fill:#1a3a5c,color:#fff
  style E fill:#1a3a5c,color:#fff
  style G fill:#1a3a5c,color:#fff
  style H fill:#1a3a5c,color:#fff
  style I fill:#1a3a5c,color:#fff
  style J fill:#1a3a5c,color:#fff
  style D fill:#c45c26,color:#fff
  style F fill:#c45c26,color:#fff
  style K fill:#c45c26,color:#fff
  style L fill:#c45c26,color:#fff
  style M fill:#2d6a4f,color:#fff
```

## 你的位置（橙色节点）

| 节点 | 你做什么 | 我做什么 |
|---|---|---|
| **审核分镜** | 改剧情、对白、节奏、人设意见 | 按你的意见重写 |
| **审核画风** | 看角色/背景图，说像不像、要不要换 | 重生图、锁连续性 |
| **终审成片** | 看完整集，决定发不发 | 按反馈改面板/音轨 |
| **发布** | 用你的抖音/视频号账号发 | 只给成片+标题+话题建议 |
| **看数据** | 告诉我播放/完播/评论 | 据此改下一集钩子 |

## 现在卡在哪

**已完成：** 1 选题 → 2 系列圣经 → 3 Ep1 分镜（待你审核）  
**你当前动作：** 读 `ep01-storyboard.md`，说改哪里  
**通过后下一步：** 4 角色参考图（第一次产生图片费用，会先报价）

## 钱与电脑

- 生图 API：我跑在我的电脑上，你只确认预算
- 剪映终修 / 发抖音·视频号：只在你手机或电脑上
- 故事技能 / 分镜：我这边，零图片费用
