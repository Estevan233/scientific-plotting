---
name: scientific-plotting
description: Publication-ready scientific plotting and visualization skill for top-tier international (Elsevier, IEEE, Nature, Springer, ACM) and Chinese core journals (CSCD, EI, CCF, 计算机学报, 自动化学报, 机械工程学报). Generates 1:1 physical canvas scaled figures, multi-panel algorithm comparison grids with ROI zoom insets, colorblind-safe palettes (Tol-muted, Okabe-Ito), dual-language fonts (Arial, Times, SimSun, SimHei), and TikZ architecture diagrams.
---

# Scientific Plotting (科研绘图 — 顶刊与核心期刊标准)

本 Skill 提供面向国际顶级期刊（Elsevier, IEEE, Nature, Springer, ACM 等）及中文顶级/核心期刊（CSCD, EI, 《计算机学报》《自动化学报》《电子学报》《机械工程学报》等）的**全套科研绘图准则、通用配置引擎与代码模板**。

---

## 核心设计哲学：物理尺寸 1:1 映射法则

在 LaTeX / Word 排版中，绝大多数图件模糊、字号失调或审稿人挑刺的根源，都是**在超大画布（如 12×8 英寸）上绘图，然后强行在论文中缩放（`\includegraphics[width=\columnwidth]{...}`）**，导致原本 10 pt 的文字在论文中缩水到 4 pt，无法肉眼辨析。

**1:1 映射黄金法则：**
1. **直接按照论文版面的物理宽度设定画布尺寸（`figsize`）**：
   - Elsevier 单栏：`figsize=(3.35, height)`（85 mm / 3.35 in）
   - Elsevier 双栏：`figsize=(6.70, height)`（170 mm / 6.70 in）或 190 mm（7.48 in）
   - IEEE 单栏：`figsize=(3.50, height)`（88.9 mm / 3.5 in）
   - IEEE 双栏：`figsize=(7.16, height)`（181.9 mm / 7.16 in）
   - Nature 单栏：`figsize=(3.50, height)`（89 mm）
   - Nature 双栏：`figsize=(7.20, height)`（183 mm）
   - 中文核心单栏：`figsize=(3.15, height)`（80 mm）
   - 中文核心双栏：`figsize=(6.50, height)`（165 mm）
2. **在代码中直接指定印刷字号**：
   - 轴标签（Labels）：8.5 – 9.5 pt
   - 刻度值（Ticks）：7.5 – 8.5 pt
   - 图例（Legend）：7.5 – 8.5 pt
   - 子图标识 `(a)`：8.5 – 9.5 pt（加粗或正体加浅底）
   - **绝对下限**：印刷在论文页面上严禁低于 6.5 pt！
3. **输出矢量 PDF 并嵌入 TrueType 字体**（`pdf.fonttype = 42`，杜绝 Type 3 字体导致 IEEE PDF eXpress 报错）。

---

## 三段式工作流：目标 → 决策 → 校验

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   1. 目标分析    │  ──>  │   2. 规范决策    │  ──>  │   3. 终审校验    │
│ 期刊/栏宽/图件类型 │       │ 尺寸/配色/字体/布局 │       │ 12项顶刊合规检查 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

### 第一步：目标分析
- **目标期刊**：Elsevier / IEEE / Nature / 中文核心
- **排版版宽**：单栏（Single Column）还是双栏全宽（Double Column）？
- **图件类型**：
  - 数据图（折线趋势、误差棒、柱状图、箱线图、散点图、雷达图）
  - 矩阵与相关性（热力图、混淆矩阵、注意力图）
  - 算法多子图定性对比（原始图像、GT、Baseline1..N、Ours，含局部 ROI 放大与指标角标）
  - 流程与架构图（TikZ 神经网络结构图、研究框架图）

### 第二步：规范决策
1. **调用预设配置引擎**：
   引入本 skill 提供的 `figure_config.py`，调用 `set_journal_profile(...)` 自动注入全局 rcParams。
2. **调色板选择（色盲安全 + 灰度可分）**：
   - **Tol-muted**（首选）：8色安全离散配色（`#332288`, `#CC6677`, `#DDCC77`, `#117733`, `#88CCEE`, `#882255`, `#44AA99`, `#AA4499`）。
   - **Okabe-Ito**：国际权威色盲友好方案（黑、橙、天蓝、青绿、黄、深蓝、朱红、紫红）。
   - **Nature 风格**：清雅高对比度（深蓝 `#2E86AB`、紫红 `#A23B72`、金橙 `#F18F01`、砖红 `#C73E1D`、橄榄绿 `#95C623`）。
   - **语义红色约束**：纯红/明亮红（`#D62728` 或 `#FF1A1A`）**仅保留用于 ROI 局部放大框、截断阈值、异常告警或重点强调**，切忌在大面积背景或普通曲线上滥用。
3. **子图标签与命名决策**：
   - 对比实验图：采用 `(a) Method Name` 形式置于每个 panel 下方，或统一在列头加粗标出方法名，并高亮突出 `Ours`。
   - 流程工作流图：仅使用 `(a)`, `(b)`, `(c)` 标在左上角，方法描述放在 Caption。

### 第三步：终审校验（12项检查清单）
每次生成图件后，对照以下清单逐一排查：
- [ ] 1. **物理尺寸**：宽度与目标期刊单栏或双栏 1:1 吻合，在 LaTeX 中 `\includegraphics[width=\linewidth]{...}` 不被缩放失真。
- [ ] 2. **字号阶梯**：成品字号均在 7–10 pt 之间，无过大或过小（<6.5 pt）字号。
- [ ] 3. **字体统一**：全图使用统一字体族（英文优先 Arial 或 Times，数学公式 `mathtext` 字体匹配，中文采用宋体/黑体）。
- [ ] 4. **TrueType 嵌入**：`pdf.fonttype = 42`，`ps.fonttype = 42`，无 Type 3 栅格字体。
- [ ] 5. **坐标轴线宽**：主轴线宽 0.5–0.7 pt（符合 Elsevier/IEEE >=0.25 pt 印刷下限）。
- [ ] 6. **刻度线朝向**：工程类期刊刻度线宜朝内（`xtick.direction: "in"`）且上下左右双向对齐，或干净单向对齐。
- [ ] 7. **配色原则**：非霓虹色、非 Matplotlib 默认浓艳基础色；灰度打印仍可明显区分。
- [ ] 8. **图例位置**：图例不遮挡数据拐点或峰值；若内部拥挤，置于外侧上方或子图空白处。
- [ ] 9. **数据范围**：Y 轴范围紧凑合理，避免留存超过 30% 的无效空白区域。
- [ ] 10. **ROI 局部放大**：若有对比实验细节，配备统一坐标的红色矩形框与对应的高倍放大 Inset。
- [ ] 11. **中文双语标注**：若投递中文核心期刊，图名与图注提供中英双语（例如：图1 系统总体架构 / Fig. 1 System architecture）。
- [ ] 12. **矢量与高分备份**：同时输出矢量 `.pdf`、`.svg` 以及 450–600 DPI 高清 `.png`。

---

## 常用图表开发规范与模式

### 1. 算法多 Panel 定性对比图（Qualitative Comparison Matrix）
- **布局规则**：
  - 170 mm / 190 mm 双栏全宽。
  - 第一列固定为原始输入（`Image`），第二列固定为真实标注（`Ground Truth`），后续为各基线方法，最后一列为本方法（`Ours`）。
  - 各子图间距极小化（`wspace=0.015`, `hspace=0.02`），边缘加淡灰边框（`#D2D6DC`, 0.5 pt）。
  - **ROI 红框与放大**：使用红色矩形框（`#FF1A1A`, 1.1 pt）精准标定关键区域，并在对应面板下方或右侧展示细节放大图（标注如 `5.8× Zoom`）。
  - **客观指标角标**：在各方法 panel 左下角附带黑色半透明底色的小标牌展示定量指标（如 `IoU: 85.2%`），本方法高亮绿色。

### 2. 实验曲线与误差带（Curves & Error Bands）
- **线宽与标记**：主曲线 `linewidth=1.2 - 1.5 pt`，散点标记 `markersize=3.5 - 4.5 pt`。
- **误差阴影**：标准差或置信区间使用 `ax.fill_between(x, y-std, y+std, alpha=0.18)`，不使用突兀的多重误差竖线破坏视线。
- **网格线**：极淡虚线（`linestyle=":"`, `color="#E2E8F0"`, `linewidth=0.5`）。

### 3. 分组柱状图与消融雷达图（Grouped Bars & Radar）
- **分组柱图**：柱体宽度 `0.22 - 0.28`，柱间微缝，边缘加 `edgecolor="white", linewidth=0.5`。
- **雷达图**：四象限极坐标，网格环线设为淡灰，填充色透明度 `alpha=0.25 - 0.35`，标签留足外边距（`pad=12`）防截断。

### 4. 中文核心期刊中英双语图表（Chinese Journal Specs）
- **字体配置**：正文使用中文字体（如黑体 SimHei、宋体 SimSun），英文与数字保持 Arial 或 Times New Roman，严禁中文字体乱码显示为方框。
- **负号修复**：必须设置 `plt.rcParams['axes.unicode_minus'] = False`。
- **双语图注**：图下排版为：
  ```
  图1 不同算法在微裂缝检测下的分割效果对比
  Fig. 1 Comparison of segmentation performance under micro-crack detection
  ```

### 5. TikZ 神经网络与系统架构图（LaTeX / TikZ）
- 使用标准几何图元（圆角矩形 `rounded corners=3pt`、渐变卡片、带阴影三维立体方块）。
- 连线采用标准箭头（`>=stealth, thick`），交叉线使用跳线或层次对齐。
- 配色统一为顶刊学术色调（浅蓝 `#E8F4F8` 充当背景组框，深蓝 `#2B6CB0` 用于核心算子，浅橙 `#FEF3C7` 用于输出）。

---

## 快速调用与资源索引

- **开源仓库**：[GitHub - scientific-plotting](https://github.com/Estevan233/scientific-plotting)
- **核心配置脚本**：[figure_config.py](./scripts/figure_config.py)
  可以直接在项目中 `from figure_config import set_journal_profile, TOL_MUTED, save_publication_figure` 或安装包后 `from scientific_plotting import set_journal_profile` 调用。
- **样例库**：
  - [折线与误差带样例](./examples/example_curve_and_errorbar.py)
  - [分组对比柱图与四象限雷达图](./examples/example_grouped_bar_and_radar.py)
  - [多Panel算法对比图与ROI局部放大](./examples/example_multipanel_comparison.py)
  - [中文核心期刊双语图表样例](./examples/example_chinese_bilingual.py)
  - [TikZ 神经网络架构图源码](./examples/example_architecture.tex)
- **参数速查参考**：
  - [各大期刊尺寸与排版参数对照表](./references/journal_dimensions.md)
  - [色盲安全色板与灰度测试对照表](./references/color_palettes.md)


