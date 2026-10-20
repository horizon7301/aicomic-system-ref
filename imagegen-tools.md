# AI漫剧 出图提质工具调研（2026-10-20，UTC+8）

## English summary
Constraint: 9:16 anime/manhua stills via a cloud image API (text + reference images), CPU-only Linux box (8 cores, 15 GB RAM, no GPU). Most famous open-source consistency/pose tools (IP-Adapter, PuLID, InstantID, PhotoMaker, ControlNet, regional prompter, character LoRA training) **need a GPU** — use them only through a hosted API/ComfyUI cloud, or as *ideas* we copy into our API workflow. What runs on CPU **today, tested**: rembg (`isnet-anime` model, ~3.6 s/panel), LaMa object removal via `big-lama.pt` TorchScript (~3.2 s on 576×1024, clean result on crowd heads), OpenCV Telea inpaint (instant, but blurs textures — only for flat areas), and a crop→API edit→feathered paste helper (`tools/region_patch.py`) that keeps the rest of the panel pixel-identical. Biggest usage savers, ranked: (1) **local-edit-instead-of-reroll** (crop region → cheap API edit → paste back; LaMa for removals/logos, free); (2) **reference-pack discipline** (character sheet + face crop + layout sketch as reference images, model e.g. Seedream 4.x edit $0.03–0.04/img or Nano Banana 2.1 ~$0.034/img 1K); (3) **layout sketch as reference** (stick-figure/blocking PNG drawn on CPU encodes court geometry, referee off-court, railing seat) replacing ControlNet; (4) **automatic QC gate** (face-similarity with InsightFace on CPU + LLM vision checklist) before accepting a panel; (5) storyboard/prompt skills already listed in github-research.md.

> 不重复 github-research.md 中已有的项目（Toonflow、ArcReel、shuohao-skills、drama-skills、TypeTale、ComfyUI_IPAdapter_plus 等）。Stars / 最后推送日期均为今天 `gh repo view` 实测。

## 1. 角色一致性（痛点1：脸/发型漂移）
| 项目 | Stars | 最后更新 | 解决什么 | 运行条件 / 成本 |
|---|---|---|---|---|
| [instantX-research/InstantID](https://github.com/instantX-research/InstantID) | 11,992 | 2024-07-18 | 单张人脸图保持身份（SDXL） | GPU ≥16GB；偏写实，动漫脸效果一般；已不活跃 |
| [TencentARC/PhotoMaker](https://github.com/TencentARC/PhotoMaker) | 10,090 | 2024-10-31 | 多张参考图堆叠身份 | GPU；偏写实 |
| [tencent-ailab/IP-Adapter](https://github.com/tencent-ailab/IP-Adapter) | 6,703 | 2024-06-28 | 图像提示适配器（风格/脸/全身参考），动漫可用 | GPU；ComfyUI 节点见旧报告 |
| [ToTheBeginning/PuLID](https://github.com/ToTheBeginning/PuLID) | 3,550 | 2025-07-31 | 无需微调的高保真 ID（SDXL/FLUX） | GPU（FLUX 版 ≥16GB）；ComfyUI：[lldacing/ComfyUI_PuLID_Flux_ll](https://github.com/lldacing/ComfyUI_PuLID_Flux_ll) 479★、[cubiq/PuLID_ComfyUI](https://github.com/cubiq/PuLID_ComfyUI) 911★ |
| [bytedance/InfiniteYou](https://github.com/bytedance/InfiniteYou) | 2,686 | 2025-08-22 | FLUX 身份保持 | GPU 24GB+ |
| [bytedance/UNO](https://github.com/bytedance/UNO) | 1,363 | 2025-09-12 | 多主体参考生成（多人同框保持） | GPU |
| [ostris/ai-toolkit](https://github.com/ostris/ai-toolkit) | 12,368 | 2026-10-19 | 训练角色 LoRA（FLUX/Qwen-Image/SDXL），最活跃 | GPU 24GB；可租云 GPU（约 ¥2–5/小时 × 1–2 小时/角色）或 fal/Replicate LoRA 训练（约 $2–5/次） |
| [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts) | 7,243 | 2026-10-20 | 经典 LoRA 训练脚本 | GPU |
| [deepinsight/insightface](https://github.com/deepinsight/insightface) | 30,003 | 2026-10-19 | 人脸检测/特征（ArcFace），可做“同一角色相似度”打分 | **CPU 可跑**（onnxruntime）；注：动漫脸检测率不稳定，可配合 anime 人脸检测器（如 hysts/anime-face-detector，未核实 stars）；模型非商用许可需注意 |

**对我们（纯 API）的结论**：上述方法在本机无法跑。等价做法是在 API 层面做“参考包”：每个角色固定 ①全身三视图 ②正脸大头裁切（512²）③发型/服装特写；每次只传与本格相关的角色（≤3 人），prompt 写明“图1=陈宇的脸与发型，严格一致”。Seedream 4.x/5 Lite edit 支持 ≤10 张参考（$0.03–0.04/张），Nano Banana 2.1 支持 ≤14 张（约 $0.034/张 1K，参考图另计约 $0.0017/张）。若后续量大且风格稳定，再考虑 **云端训练角色 LoRA + 托管推理**（fal/Replicate/LiblibAI），一致性最好。

## 2. 姿势与构图控制（痛点2、3：克隆脸、空间/物理错误）
| 项目 | Stars | 最后更新 | 解决什么 | 运行条件 |
|---|---|---|---|---|
| [lllyasviel/ControlNet](https://github.com/lllyasviel/ControlNet) | 34,125 | 2024-02-25 | OpenPose/深度/线稿控制构图 | GPU |
| [Mikubill/sd-webui-controlnet](https://github.com/Mikubill/sd-webui-controlnet) | 17,824 | 2024-08-12 | WebUI 版 ControlNet | GPU |
| [Fannovel16/comfyui_controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux) | 4,236 | 2026-10-11 | 预处理器：OpenPose/DWPose/深度/线稿提取 | **预处理器 CPU 可跑**（慢但可用），可把好图的姿势/深度图提出来当“构图参考图”传给 API |
| [hako-mikan/sd-webui-regional-prompter](https://github.com/hako-mikan/sd-webui-regional-prompter) | 1,816 | 2026-09-04 | 分区提示词（左人物A、右人物B，防属性串味） | GPU |
| [gligen/GLIGEN](https://github.com/gligen/GLIGEN) | 2,220 | 2024-03-06 | 框→图（layout-to-image） | GPU；已停更 |
| [YangLing0818/RPG-DiffusionMaster](https://github.com/YangLing0818/RPG-DiffusionMaster) | 1,841 | 2025-02-01 | LLM 先规划区域再分区生成 | GPU；**思路可借鉴**：让 LLM 先输出每格的区域布局 |
| [omerbt/MultiDiffusion](https://github.com/omerbt/MultiDiffusion) | 1,071 | 2023-09-21 | 区域控制 | GPU；陈旧 |
| [Yuanshi9815/OminiControl](https://github.com/Yuanshi9815/OminiControl) | 1,958 | 2026-10-02 | FLUX 统一条件控制（主体+空间） | GPU |
| [jtydhr88/ComfyUI-qwenmultiangle](https://github.com/jtydhr88/ComfyUI-qwenmultiangle) | 1,405 | 2026-09-13 | Qwen-Image-Edit 多角度换机位 | GPU 或云 ComfyUI |

**API 替代方案（本机 CPU 可做，推荐）**：用 Python/PIL 画“布局草图”作为参考图：球场俯视/透视线（中圈、三秒区/禁区、边线）、彩色方块+火柴人标出每个人物位置、裁判放在**边线外**、女主坐在**看台座椅**而非栏杆。prompt 写“严格按图2的构图与位置，图2只是布局不要画出线条”。这在 Nano Banana/Seedream/GPT-Image 上就是“穷人版 ControlNet”。背景群众：prompt 明确“观众面孔各不相同、背景球员号码分别为 4、9、12”，并在分镜表中**为每格预先分配号码**；仍出错就用第3节局部修。

## 3. 局部修复/inpaint（痛点4、5：logo、少重抽）
| 项目 | Stars | 最后更新 | 解决什么 | 运行条件 / 成本 |
|---|---|---|---|---|
| [Sanster/IOPaint](https://github.com/Sanster/IOPaint)（原 lama-cleaner） | 23,303 | 2025-04-29 | 网页刷子去物体/去 logo/去文字，LaMa/MAT 等 | LaMa **CPU 可跑**；但 pip 包在 Python 3.13 安装失败（`KeyError: '__version__'`），需 Python 3.10/3.11 venv 或 Docker。我们已绕开：直接加载其发布的 `big-lama.pt` |
| [advimman/lama](https://github.com/advimman/lama) | 10,326 | 2025-02-05 | LaMa 大掩码修复原始仓库 | CPU 推理可用 |
| 图像 API 自带编辑 | — | — | Nano Banana 2.1 无 mask 参数，需在图上涂画/用语言描述区域；**官方也不保证其他区域不变** | 每次编辑按一张图计费 |

**关键技巧：裁切→编辑→羽化贴回**（`tools/region_patch.py`，已实测）。只把出错区域（例如一张克隆脸、一个号码、一个勾子）裁成小图送 API 修，再羽化贴回，其他像素 100% 不变；比整格重抽省一次完整生成，且不会引入新错误。纯“删除类”修复（logo、多余观众、杂物）直接用本机 LaMa，免费。

## 4. 抠图/分割/合成（CPU 友好）
| 项目 | Stars | 最后更新 | 用途 | 运行条件 |
|---|---|---|---|---|
| [danielgatis/rembg](https://github.com/danielgatis/rembg) | 25,131 | 2026-10-10 | 去背景，含 `isnet-anime` 动漫模型 | **CPU，已实测** |
| [ZhengPeng7/BiRefNet](https://github.com/ZhengPeng7/BiRefNet) | 4,310 | 2026-10-17 | 高精度抠图（rembg 也内置 birefnet 模型） | CPU 可跑但较慢（~10–30 s/张，估计） |
| [facebookresearch/sam2](https://github.com/facebookresearch/sam2) | 20,023 | 2026-05-30 | 点/框提示分割单个人物 | tiny/small 模型 CPU 可跑（数秒级） |
| [facebookresearch/segment-anything](https://github.com/facebookresearch/segment-anything) | 55,036 | 2024-09-18 | SAM1 | CPU 可跑（慢） |
| [IDEA-Research/Grounded-Segment-Anything](https://github.com/IDEA-Research/Grounded-Segment-Anything) | 17,773 | 2024-09-05 | 文字→框→掩码（“the referee”“swoosh logo”自动出 mask） | CPU 勉强；GroundingDINO 10,689★ |
| [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) | 62,657 | 2026-10-20 | YOLO 检测/分割，快速数人、找人物框 | **CPU 很快**；AGPL |

## 5. 分镜/提示词/工作流库
已在 github-research.md 列出的 skills 不再重复。补充：[anthropics/skills](https://github.com/anthropics/skills)（182,322★，2026-10-09）——官方 Agent Skills 格式与示例，用来把本报告的“参考包+布局草图+QC 清单”写成我们自己的 `manhua-panel` skill。[Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI)（140,054★）——若将来租 GPU，上面的 PuLID/ControlNet/区域提示都在这里组合；[nunchux-ai/ComfyUI-nunchaku](https://github.com/nunchux-ai/ComfyUI-nunchaku)（2,934★）4-bit FLUX 加速，可降低云 GPU 成本。`gh search` 中“漫剧 ComfyUI 工作流”多为小仓库/广告，没有值得推荐的成熟项目。

## 6. 质检（QC）
- **InsightFace / anime 人脸检测 + 余弦相似度**（CPU）：每格主角脸与角色标准脸比对，低于阈值自动打回；同格内多张脸两两相似度过高 → 判“克隆脸”。
- **YOLO（CPU）**：数人数、检查人物框是否与布局草图一致（裁判框是否在边线外）。
- **视觉 LLM 清单**（便宜的多模态模型，约几分钱/格）：逐项问“有无品牌 logo？号码是否重复？人物是否悬空/坐在栏杆？比赛位置是否在禁区？”，只把未通过项送去局部修。

## 7. 本机实测（CPU，8 核）
测试图 `ep01/p05-v2.jpg`（576×1024），产物在 `tools/test/`：
| 测试 | 结果 |
|---|---|
| rembg `u2net_human_seg` | 3.8 s；前景识别差（裁判头部半透明、右侧人物丢失）。不推荐 |
| rembg `isnet-anime` 整图 | 3.6 s；前景人群完整，但女主与看台连一起，无法只抠一人 |
| rembg `isnet-anime` 先裁 7 号球员框再抠 | ~2 s，单人抠图可用 → `p05-no7-cut.png`。单人精确抠图建议框裁+rembg，或 SAM2 点提示 |
| OpenCV Telea inpaint（去左上观众） | 0.02 s，结果糊成色块，只适合纯色/地板 |
| LaMa (`big-lama.pt`, torch 2.14 CPU) | 3.2 s，观众区自然补全，几乎看不出 → `p05-inpaint-lama.jpg`；适合去 logo/多余人物 |
| IOPaint pip 安装 | 失败（Python 3.13 不兼容），已改为直接加载模型 |
| `region_patch.py` crop→paste 往返 | 区域外像素不变（最大差 16 仅为 JPEG 重压缩） |
环境：`/workspace/venv-img`（rembg、onnxruntime、opencv、torch-cpu）。模型缓存 `~/.rembg/`，`tools/test/big-lama.pt`（206 MB）。顺带发现：p05-v2 本身就有“女主坐栏杆”和“左右两名球员同脸同号 7”的问题，可直接作为第一批局部修复对象。

## 8. 推荐升级流水线（按“省下的用量 ÷ 投入”排序）
1. **局部修复代替整格重抽**（投入：低，已就绪）— 出错只修区域：删除类用 LaMa（免费，3 s），重画类用 `region_patch.py` 裁切→API edit→贴回。预计减少 50%+ 整格重抽。
2. **布局草图参考图**（投入：低—中，半天写脚本）— 每格用 PIL 自动画球场/看台/人物站位块，与角色参考一起传给 API；直接针对空间/物理错误与“裁判上场”。
3. **角色参考包 + 每格只传相关角色**（投入：低）— 三视图+脸部特写+固定连续性锁短语；号码/观众面孔在分镜表中预先指定；负面写明“no brand logos, no Nike swoosh”。
4. **自动 QC 闸门**（投入：中）— InsightFace 相似度 + YOLO 人数/位置 + 视觉 LLM 清单，在人工看图之前拦截，只把问题区域送修。
5. **（可选，量大时）云端角色 LoRA / PuLID**（投入：高，需付费 GPU 或托管 API）— ai-toolkit 训练每角色 LoRA，在托管 ComfyUI 上配合 ControlNet OpenPose，一致性最高。

成本参考：Seedream 4.0/4.5/5.0 Lite edit $0.03/$0.04/$0.035 每张（fal）；Nano Banana 2.1 约 $0.034（1K）/$0.050（2K）；Nano Banana Pro $0.15。本机工具全部免费。
