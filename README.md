<div align="center">

# GitHub Pages Personal Site

**把一个真实个人网站的建设过程，变成可以反复使用的 Codex Skill。**

![Codex Skill](https://img.shields.io/badge/Codex-Skill-173124?style=flat-square)
![Static Web](https://img.shields.io/badge/Web-HTML%20%2F%20CSS%20%2F%20JavaScript-43735A?style=flat-square)
![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-24292F?style=flat-square)

[查看网站案例](https://peppaoinks.github.io/) · [阅读 Skill](SKILL.md) · [查看完整建站记录](references/build-history.md)

</div>

---

## 项目介绍

这个项目把 [Felixzhou 个人网站](https://github.com/peppaoinks/peppaoinks.github.io)从初版到 29 次提交的建设经验，整理成一套 Codex 可以按需读取的工作流程。

从一句“做一个个人主页”开始，逐步补充介绍、调整字体和配色、加入生活照与视频、制作书架和歌单，再通过 GitHub Pages 发布。过程中关于图片加载、照片日期、双语链接、二维码配色和浏览器缓存的实际处理方法，也保存在这里。

仓库提供 Skill 指令、专题参考文档、两个 Python 工具，以及一份 Pages 发布工作流样板。网站案例的完整前端源码位于[原站仓库](https://github.com/peppaoinks/peppaoinks.github.io)。

## 能做什么

| 方向 | 覆盖内容 |
| --- | --- |
| 个人介绍与内容 | 逐步收集真实信息，整理教育、兴趣、项目、社交入口与近况 |
| 视觉与排版 | 衬线字体、中文字重、响应式布局、个人字标、滚动页眉 |
| 双语与主题 | 中英文切换、深浅模式、偏好保存、替代文字与控件标签同步 |
| 图片与视频 | EXIF 日期核对、方向修正、WebP 压缩、相邻图片预加载、MP4 与封面 |
| 二维码 | 内嵌 SVG、主题配色、静区保留、实际截图解码验证 |
| 互动组件 | 生活相册、校园地图、横向阅读书架与专辑封面轨道 |
| 发布与维护 | GitHub Pages、公开文件清单、资源核对、部署确认与缓存排查 |

可以用它从头建立静态主页，也可以只处理现有网站的一项改动。配色、品牌和栏目顺序随项目需要调整。

## 快速开始

### 1. 安装 Skill

需要 Git，以及能够加载本地 Skill 的 Codex 环境。将仓库克隆到 skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/peppaoinks/github-pages-personal-site.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/github-pages-personal-site"
```

如果已经安装了同名 Skill，请先确认它的来源，避免重复克隆。阅读 Skill 与参考文档无需安装 Python 依赖；只有运行相应工具时才需要。

### 2. 在 Codex 中调用

打开目标网站的项目目录，用 `$github-pages-personal-site` 指定这个 Skill，再描述本次需求。例如：

**新建主页**

```text
使用 $github-pages-personal-site 帮我做一个 GitHub Pages 个人主页。
需要中英文切换、深浅主题和项目展示。先做好初版，个人信息逐步补充。
```

**维护现有网站**

```text
使用 $github-pages-personal-site 给我的主页加入“最近在读”。
我会提供书名，需要封面、手机横向滑动、左右按钮和键盘切换。
```

**处理照片并检查发布**

```text
使用 $github-pages-personal-site 把这些照片加入生活相册。
读取能确认的拍摄日期，优化网页副本，保留原图，完成后发布并核对线上版本。
```

Skill 会根据任务读取所需专题。新建仓库、推送或发布，仍以你在当前任务中的要求为准。

## 工作流程

```mermaid
flowchart LR
    A[确认项目与需求] --> B[搭建页面与内容]
    B --> C[统一视觉与双语]
    C --> D[处理媒体与交互]
    D --> E[本地验收]
    E --> F[提交与 Pages 部署]
    F --> G[核对线上版本]
```

实际任务可以从其中任一步开始。比如更换照片只需处理素材、相册与发布；修改简介则重点检查两种语言和布局。

## 工具使用

以下命令在本仓库根目录运行。将示例中的 `./my-site` 和输入文件替换为自己的路径。

### 图片优化

需要 Python 3.9+ 和 Pillow。建议使用独立虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Pillow
```

生成 WebP 网页副本，同时把原图读取到的日期、方向、尺寸和体积写入本地报告：

```bash
python scripts/optimize_images.py ./photos/photo.jpg \
  --output-dir ./my-site/assets/gallery \
  --max-edge 1200 \
  --quality 78 \
  --report ./media-report.json
```

- 先按 EXIF 修正方向，再缩放；输出不携带源 EXIF，原图保持不变。
- 报告中的拍摄时间仍需核对，缺失时标为未知，不用文件修改时间代替。
- 默认拒绝覆盖已有输出；明确更新网页副本时可以加 `--overwrite`。
- HEIC 可选安装 `pillow-heif`，也可按[媒体处理说明](references/media-and-qr.md)使用系统工具转换。

### 静态资源核对

需要 Python 3.9+，仅使用标准库：

```bash
python3 scripts/check_site.py ./my-site
```

检查页面引用的本地资源、HTML 锚点、重复 ID、JSON 语法及清单中的封面路径。发现问题时以非零状态退出。

部署后还可以与正式站点逐字节比较：

```bash
python3 scripts/check_site.py ./my-site \
  --base-url https://YOUR_USERNAME.github.io/ \
  --cache-tag YOUR_COMMIT_SHA
```

比较前确保本地目录对应要验证的提交，检查期间不再修改文件。这个工具不执行 JavaScript，也不验证版式、扫码能力或全部外部链接；这些仍需要实际操作检查。

### GitHub Pages 工作流

[assets/pages.yml](assets/pages.yml)提供静态网站发布样板。将它复制到**网站仓库**的 `.github/workflows/pages.yml`，然后按实际情况调整：

1. 修改触发分支和需要发布的文件清单。
2. 在网站仓库的 Pages 设置中选择 **GitHub Actions**。
3. 推送后检查对应提交的部署结果，再核对正式页面和资源。

样板默认发布 `index.html`、`style.css`、`script.js`、`.nojekyll` 和 `assets/`。新增独立页面或其他资源时，需要同步调整。具体配置与验收步骤见[发布说明](references/release-and-qa.md)。

## 仓库结构

```text
github-pages-personal-site/
├── README.md                         # 给使用者看的项目说明
├── SKILL.md                          # Codex 读取的入口与工作流程
├── agents/
│   └── openai.yaml                   # Skill 展示名称与默认提示
├── assets/
│   └── pages.yml                     # 网站部署工作流样板
├── scripts/
│   ├── optimize_images.py            # 生成网页图片副本
│   └── check_site.py                 # 检查资源与部署文件
└── references/
    ├── build-history.md              # 完整建设过程与 29 次提交索引
    ├── design-and-content.md         # 内容、字体、双语与主题
    ├── media-and-qr.md               # 图片、视频、日期与二维码
    ├── interactive-components.md     # 页眉、地图、书架与音乐
    └── release-and-qa.md              # 发布、验收与缓存排查
```

## 实践记录

完整建设记录固定在原站提交 [`637f237`](https://github.com/peppaoinks/peppaoinks.github.io/tree/637f237)，便于追溯每项经验的实际来源。正式网站可能继续更新。

这套流程强调几件在实际迭代中反复遇到的事：

- **个人内容有出处。** 经历、在读书目、照片日期和地点来自本人提供或核验，不为填满栏目编造内容。
- **双语改动成对维护。** 默认 HTML、翻译字典、标签和地图文字一起检查，链接不会被整段文本替换删除。
- **素材按用途处理。** 生活照可以有损压缩，二维码需要保留模块与静区，并验证真实截图。
- **上线有证据。** 推送完成后继续确认对应部署及线上文件，遇到旧页面先核对版本与缓存。

基线中，随笔与摄影仍为空，简历等待 PDF，音乐是候选曲目；文章系统和私人 Apple Music 记录同步属于后续扩展。仓库保留方法与工具，不包含个人照片、赞赏码内容或账户凭据。

## 反馈与改进

欢迎通过 [Issues](https://github.com/peppaoinks/github-pages-personal-site/issues)反馈无法复用的步骤、工具问题或新的建站案例，也可以提交 Pull Request。

反馈时请附上预期行为、实际结果、相关文件和必要环境信息。修改工具后验证它实际处理的场景；修改流程时同步对应参考文档。截图、日志和示例素材请使用适合公开的内容。
