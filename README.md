# Scientific Plotting (科研绘图 — 国际顶刊与中文核心标准)

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version"></a>
  <a href="https://matplotlib.org"><img src="https://img.shields.io/badge/Matplotlib-Publication--Ready-green.svg" alt="Matplotlib"></a>
  <a href="#"><img src="https://img.shields.io/badge/Standards-Elsevier%20%7C%20IEEE%20%7C%20Nature%20%7C%20CSCD-orange.svg" alt="Standards"></a>
  <a href="#"><img src="https://img.shields.io/badge/AI%20Assistant-Antigravity%20%7C%20Claude%20%7C%20Cursor%20%7C%20Codex-purple.svg" alt="AI Ready"></a>
</p>

面向国际顶级期刊（**Elsevier, IEEE Transactions, Nature Portfolio, Springer, ACM**）与中文顶刊/核心期刊（**CSCD, EI, 《计算机学报》《自动化学报》《电子学报》《机械工程学报》** 等）的**全套科研绘图准则、通用配置引擎、极简样例库与 AI Assistant (Agent) 技能包**。

彻底终结：
- ❌ 画布太大插进 LaTeX 被强行缩放，导致字号比蚂蚁还小（< 6 pt）
- ❌ 导出 PDF 被 IEEE PDF eXpress / Elsevier 报错 `Type 3 fonts not allowed`
- ❌ 默认配色浓艳杂乱、审稿人警告色盲不友好、黑白打印糊成一团
- ❌ 中文图表负号变方框乱码、宋体与英文数字混排割裂

---

## ⚡ 快速安装与导入 (Installation)

本仓库同时支持作为 **AI 编码助手技能（Skill）** 或 **Python 独立模块** 使用。

### 1. 作为 AI Agent 技能安装 (跨生态多助手全面兼容)

本仓库原生内置了面向各大主流 AI 助手的规范适配层：
- **Antigravity / Gemini CLI**：通过 `SKILL.md` 自动发现技能
- **Claude / Claude Code**：通过根目录 `CLAUDE.md` 深度理解指令
- **OpenAI Codex / DeepSeek / 通用智能体**：通过 `AGENTS.md` 注入顶刊绘图准则
- **Cursor / Windsurf**：通过 `.cursor/rules/scientific-plotting.mdc` 自动生效

#### A. 全局安装 (所有项目均可直接唤醒)
- **Windows (PowerShell)**:
  ```powershell
  git clone https://github.com/Estevan233/scientific-plotting.git "$HOME\.gemini\skills\scientific-plotting"
  ```
- **macOS / Linux**:
  ```bash
  git clone https://github.com/Estevan233/scientific-plotting.git ~/.gemini/skills/scientific-plotting
  ```

#### B. 当前项目工作区安装 (适用 Codex / Claude / DeepSeek / Cursor)
在任意科研代码仓库根目录下运行：
- **作为工作区技能目录引入**:
  ```bash
  mkdir -p .agents/skills
  git clone https://github.com/Estevan233/scientific-plotting.git .agents/skills/scientific-plotting
  ```
- **作为 Git 子模块引入 (团队协同推荐)**:
  ```bash
  git submodule add https://github.com/Estevan233/scientific-plotting.git .agents/skills/scientific-plotting
  ```
- **Cursor 规则一键链接 (可选)**:
  ```bash
  mkdir -p .cursor/rules
  cp .agents/skills/scientific-plotting/.cursor/rules/* .cursor/rules/
  ```

### 2. 作为 Python 绘图包安装 (Pip)
```bash
pip install git+https://github.com/Estevan233/scientific-plotting.git
```
或克隆后本地可编辑模式安装：
```bash
git clone https://github.com/Estevan233/scientific-plotting.git
cd scientific-plotting && pip install -e .
```

---

## 🚀 5 行代码极速上手 (Quickstart)

```python
import matplotlib.pyplot as plt
from scientific_plotting import set_journal_profile, get_canvas_size, TOL_MUTED_LIST, save_publication_figure

# 1. 注入顶级期刊风格（自动适配 Elsevier/IEEE/Nature/中文核心）
set_journal_profile(journal="elsevier", font_style="sans-serif", base_fontsize=9.0)

# 2. 申请 1:1 原生物理画布尺寸（单栏 85mm，在 LaTeX 中 width=\linewidth 时 0 缩放）
fig, ax = plt.subplots(figsize=get_canvas_size(journal="elsevier", columns=1))

# 3. 使用色盲安全与灰度可分色板绘图
ax.plot([0, 10, 20], [0.1, 0.6, 0.9], color=TOL_MUTED_LIST[0], label="Ours", linewidth=1.4)
ax.set_xlabel("Epoch"); ax.set_ylabel("Score"); ax.legend()

# 4. 一键导出 TrueType Type-42 矢量 PDF 与 600 DPI 备份
save_publication_figure(fig, "figures/fig1_quickstart", formats=("pdf", "png"), dpi=600)
```

---

## 🎨 核心能力与顶刊标准

### 1. 物理尺寸 1:1 映射法则
直接在 Python 画布上定义论文版面物理尺寸，**在 LaTeX 中 `\includegraphics[width=\linewidth]{...}` 零缩放贴合**，彻底保证印刷字号严格在 7.5–9.5 pt，绝不低于 6.5 pt 审稿红线。

| 出版商 / 体系 | 单栏宽 (Single Col) | 双栏宽 (Double Col) | 推荐字体族 | 印刷字号区间 |
| :--- | :--- | :--- | :--- | :--- |
| **Elsevier** | 85 mm (3.35 in) | 170 / 190 mm (6.70 / 7.48 in) | Arial (无衬线) | 7.5 – 9.5 pt |
| **IEEE Transactions** | 88.9 mm (3.50 in) | 181.9 mm (7.16 in) | Times New Roman / Arial | 7.5 – 8.5 pt |
| **Nature Portfolio** | 89 mm (3.50 in) | 183 mm (7.20 in) | Arial / Helvetica | 5.0 – 8.0 pt |
| **Springer** | 84 mm (3.31 in) | 174 mm (6.85 in) | Arial / Helvetica | 7.0 – 9.0 pt |
| **中文核心 / EI** | 80 mm (3.15 in) | 165 mm (6.50 in) | SimSun (宋体) + Arial | 7.0 – 9.0 pt |

### 2. 国际权威色盲友好与灰度双保险
- **Paul Tol's Muted Qualitative Palette**（8色安全色相，单调亮度，首选推荐）
- **Okabe-Ito Palette**（国际权威色盲标准）
- **Nature 学术风格色板**（高质感低饱和现代学术配色）
- **语义红色约束**：鲜红（`#FF1A1A`）严格限定用于 **ROI 红框、截断阈值或极限告警**，杜绝大面积滥用。
- **灰度双保险**：针对中文期刊黑白印刷要求，示例示范了结合不同线型（`-`, `--`, `-.`）与数据标记（`o`, `s`, `^`）的视觉区分。

### 3. 多 Panel 算法定性对比图矩阵 (Qualitative Comparison Matrix)
提供业界领先的多方法对比矩阵与细节放大方案：
- 列间距微缝布局（`wspace=0.015`, `hspace=0.03`）。
- **同步标定 ROI 矩形红框**（`add_roi_box`）。
- **高倍率局部放大 Inset**（带红色边框与倍数标识，如 `5.8× Zoom`）。
- **非遮挡量化指标深底标牌**（`add_metric_badge`，如 `IoU: 88.5%`）。

### 4. 深度学习与系统架构图 (LaTeX / TikZ)
提供开箱即用的 TikZ 神经网络数据流与算法流程图模板，包含立体阴影、圆角卡片、跳跃连接与层次分组。

---

## 📂 项目结构 (Repository Structure)

```text
scientific-plotting/
├── SKILL.md                          # AI 助手技能规范说明书 (Agent Runbook)
├── README.md                         # 仓库说明文档 (English / 中文)
├── pyproject.toml                    # Python 标准打包配置 (PEP 517/518)
├── requirements.txt                  # 依赖清单
├── LICENSE                           # MIT 许可证
├── install.ps1                       # Windows PowerShell 一键安装脚本
├── install.sh                        # macOS / Linux Bash 一键安装脚本
├── scientific_plotting/              # Python 核心包源码
│   ├── __init__.py
│   └── figure_config.py              # 多期刊预设、字号阶梯、字体探测、色板、导出函数
├── scripts/                          # Agent 兼容脚本入口
│   └── figure_config.py
├── examples/                         # 5大常用顶刊图表最小工作样例 (MWE)
│   ├── example_curve_and_errorbar.py # 1. 实验收敛曲线与半透明置信区间带
│   ├── example_grouped_bar_and_radar.py # 2. 分组对比柱图 + 四象限极坐标雷达图
│   ├── example_multipanel_comparison.py # 3. 算法多Panel对比图 + 红色ROI选框 + 局部放大 + IoU角标
│   ├── example_chinese_bilingual.py     # 4. 中文顶级核心期刊双语图表（宋体/黑体+Arial，灰度线型）
│   ├── example_architecture.tex      # 5. TikZ 深度学习神经网络架构图模板
│   └── outputs/                      # 样例生成的矢量 PDF 与 600 DPI PNG 效果图
├── references/                       # 顶刊深入排版与色彩手册
│   ├── journal_dimensions.md         # 出版商尺寸、线宽下限与 LaTeX 引入指南
│   └── color_palettes.md             # HEX 色值明度对照表与色盲无障碍准则
└── tests/                            # 自动化测试套件
    └── test_examples.py              # 样例脚本完整性与 PDF 输出回归测试
```

---

## 🧪 运行测试 (Running Tests)

```bash
python tests/test_examples.py
```
一键运行 4 大核心绘图样例测试，验证 TrueType 嵌入、矢量 PDF 生成与 600 DPI 点阵导出。

---

## 🤝 贡献与开源许可 (Contributing & License)

欢迎提交 Issue 和 Pull Request 补充更多学科（如医学、化学、材料力学等）的期刊预设！

本项目采用 [MIT License](LICENSE) 开源。

