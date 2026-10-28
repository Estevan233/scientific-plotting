# Top-Tier Journal Dimensions & Formatting Reference Guide

本参考手册汇总了国际主流出版商（Elsevier, IEEE, Nature Portfolio, Springer, ACM）以及国内中文顶级核心期刊（CSCD / EI）的图件物理尺寸、线宽下限、字体标准与 DPI 规约。

---

## 1. 国际顶级期刊出版商规约速查表

| 出版商 / 期刊系列 | 单栏排版宽度 (Single) | 1.5 栏 / 特殊宽度 | 双栏通栏宽度 (Double) | 推荐字体 | 印刷字号区间 | 矢量 / 点阵 DPI 要求 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Elsevier**<br>(AiC, AEI, PR, CBM 等) | **85 mm**<br>(3.35 in) | 120 mm<br>(4.72 in) | **170 – 190 mm**<br>(6.69 – 7.48 in) | **Arial** (首选)<br>Helvetica / Times | 7 – 9 pt<br>(绝对下限 6.0 pt) | 矢量 PDF / EPS<br>彩照 ≥300, 组合图 ≥500, 线条图 ≥1000 |
| **IEEE Transactions**<br>(TPAMI, TIP, TCYB 等) | **88.9 mm**<br>(3.50 in / 21 picas) | — | **181.9 mm**<br>(7.16 in / 43 picas) | **Times New Roman**<br>或 Arial | 7.5 – 8.5 pt<br>(下限 6.0 pt) | 矢量 PDF (Type 42 嵌入)<br>线图 600–1200 DPI |
| **Nature Portfolio**<br>(Nature, Nat Comm, Sci Rep) | **89 mm**<br>(3.50 in) | 120 – 136 mm<br>(4.72 – 5.35 in) | **183 mm**<br>(7.20 in) | **Arial** 或 Helvetica<br>(严禁正文用 Times) | 5 – 8 pt<br>(常用 7 pt) | 矢量 PDF (嵌入字型)<br>位图 ≥300 DPI |
| **Springer**<br>(IJCV, Neural Computing 等) | **84 mm**<br>(3.31 in) | 115 mm<br>(4.53 in) | **174 mm**<br>(6.85 in) | **Arial** / Helvetica | 7 – 9 pt | 矢量 PDF / EPS<br>线条 ≥1000 DPI |
| **ACM Transactions**<br>(TOG, TIST 等) | **84 mm**<br>(3.31 in) | — | **178 mm**<br>(7.00 in) | **Linux Biolinum**<br>或 Helvetica / Arial | 7.5 – 9.0 pt | 矢量 PDF<br>点阵 ≥300 DPI |
| **中文核心 / EI 期刊**<br>(计算机/自动化/机械学报等) | **75 – 80 mm**<br>(半栏 / 3.0–3.15 in) | — | **150 – 170 mm**<br>(通栏 / 6.0–6.7 in) | **SimSun (宋体)**<br>+ Times/Arial | 7 – 9 pt<br>(六号至小五) | 矢量 PDF / EPS<br>黑白线条 ≥600 DPI |

---

## 2. 关键排版物理法则

### 2.1 线宽限制 (Hairline Rule)
- 期刊排版系统在印刷制版时，对细线具有物理极限。
- **Elsevier / IEEE 铁律**：线宽不得低于 **0.25 pt (0.09 mm)**。若使用 0.1 pt 细线，印刷后将发生断裂或彻底消失。
- **推荐线宽阶梯**：
  - 坐标轴边框（Spines）：`0.5 – 0.7 pt`
  - 主曲线（Data Lines）：`1.2 – 1.6 pt`
  - 辅助网格线（Grid Lines）：`0.4 – 0.5 pt`（透明度 `alpha=0.5 - 0.7`）
  - ROI 局部放大框（ROI Borders）：`1.0 – 1.2 pt`

### 2.2 字体嵌入防拒稿法则 (TrueType Type-42)
- IEEE PDF eXpress 与 Elsevier 投稿检查系统会对上传的 PDF 进行字体合规性扫描。
- **常见拒稿警告**：`Font Type 3 is not permitted`（Type 3 为位图栅格化字体，缩放会严重虚化且不可检索编辑）。
- **Matplotlib 根治配置**：
  ```python
  import matplotlib.pyplot as plt
  plt.rcParams['pdf.fonttype'] = 42  # 强制 TrueType 矢量嵌入
  plt.rcParams['ps.fonttype'] = 42
  plt.rcParams['text.usetex'] = False # 避免调用本机非标 TeX 引擎
  ```

---

## 3. LaTeX 页面 1:1 导入命令范式

在实际论文撰写中，通过将代码的 `figsize` 严格绑定到单栏/双栏宽度，在 LaTeX 中即可实现原生 1:1 贴合：

### 单栏图件导入
```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figures/fig_curve_errorbar.pdf}
  \caption{Comparison of convergence curves under different noise ratios.}
  \label{fig:curve}
\end{figure}
```

### 双栏通栏图件导入
```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/fig_multipanel_comparison.pdf}
  \caption{Qualitative comparison of crack segmentation results on challenging surfaces. Synchronized red bounding boxes denote regions of interest (ROI) with high magnification details in row (b).}
  \label{fig:comparison}
\end{figure*}
```

