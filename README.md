<div align="center">

# GitHub Pages Personal Site

用 Codex 搭建和维护 GitHub Pages 个人主页。

![Codex Skill](https://img.shields.io/badge/Codex-Skill-173124?style=flat-square)
![Static Web](https://img.shields.io/badge/Web-HTML%20%2F%20CSS%20%2F%20JavaScript-43735A?style=flat-square)
![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-24292F?style=flat-square)

[网站示例](https://peppaoinks.github.io/) · [Skill 说明](SKILL.md) · [建站记录](references/build-history.md)

</div>

---

## 项目介绍

这是一个面向个人主页的 Codex Skill，适合使用 HTML、CSS 和 JavaScript 的 GitHub Pages 网站。可以从简单的自我介绍和项目展示开始，按需要添加相册、校园地图、阅读书架和歌单。

仓库里有 Skill 指令和参考文档，也有图片压缩、资源检查工具与 Pages 工作流模板。想看完整的网页实现，可以参考 [Felixzhou 个人网站源码](https://github.com/peppaoinks/peppaoinks.github.io)。

## 能做什么

| 功能 | 内容 |
| --- | --- |
| 内容整理 | 个人介绍、教育经历、兴趣、项目、社交链接与近况 |
| 视觉与排版 | 衬线字体、中文字重、响应式布局、个人字标、滚动页眉 |
| 双语与主题 | 中英文切换、深浅模式、偏好保存、替代文字与控件标签同步 |
| 图片与视频 | EXIF 拍摄时间、方向修正、WebP 压缩、图片预加载、MP4 与封面 |
| 二维码 | 内嵌 SVG、深浅配色与扫码检查 |
| 互动组件 | 生活相册、校园地图、横向阅读书架与专辑封面轨道 |
| 发布与维护 | GitHub Pages 部署、资源检查与缓存排查 |

已有网站也可以使用，直接说明要改的部分即可。配色、字体和栏目顺序都可以自己选。

## 快速开始

### 1. 安装 Skill

在支持本地 Skill 的 Codex 环境中，用 Git 将仓库克隆到 skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/peppaoinks/github-pages-personal-site.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/github-pages-personal-site"
```

已经安装过的可以跳过这一步。Python 用于下方的辅助工具，安装 Skill 本身不需要。

### 2. 在 Codex 中调用

打开网站项目目录，在请求中写上 `$github-pages-personal-site`。例如：

新建主页：

```text
使用 $github-pages-personal-site 帮我做一个 GitHub Pages 个人主页。
需要中英文切换、深浅主题和项目展示。先做好初版，个人信息逐步补充。
```

给现有网站加书架：

```text
使用 $github-pages-personal-site 给我的主页加入“最近在读”。
我会提供书名，需要封面、手机横向滑动、左右按钮和键盘切换。
```

添加生活照：

```text
使用 $github-pages-personal-site 把这些照片加入生活相册。
读取能确认的拍摄日期，优化网页副本，保留原图，完成后发布并核对线上版本。
```

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

## 工具使用

以下命令在本仓库根目录运行，将 `./my-site` 和输入文件换成自己的路径。

### 图片优化

图片工具需要 Python 3.9+ 和 Pillow，可以在虚拟环境中安装：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Pillow
```

将照片转为 WebP，并在报告中保存原图的拍摄时间、方向和尺寸：

```bash
python scripts/optimize_images.py ./photos/photo.jpg \
  --output-dir ./my-site/assets/gallery \
  --max-edge 1200 \
  --quality 78 \
  --report ./media-report.json
```

工具会按 EXIF 修正方向、缩放图片并移除输出中的 EXIF，保留原图。报告也会记录转换前后的文件大小；读不到拍摄时间时留空。

已有输出文件默认不会被覆盖，更新时加 `--overwrite`。处理 HEIC 可以安装 `pillow-heif`，或使用[媒体处理说明](references/media-and-qr.md)中的系统工具。

### 静态资源核对

资源检查工具只需要 Python 3.9+：

```bash
python3 scripts/check_site.py ./my-site
```

它会检查本地资源和 HTML 锚点，查找重复 ID，并核对 JSON 语法和封面路径。发现问题时返回非零退出状态。

部署后可以比较本地与线上文件是否一致：

```bash
python3 scripts/check_site.py ./my-site \
  --base-url https://YOUR_USERNAME.github.io/ \
  --cache-tag YOUR_COMMIT_SHA
```

比较时使用对应提交的本地文件，检查期间不要修改。脚本不执行 JavaScript；页面布局、交互、二维码和外部链接还需要在浏览器或相应 App 中检查。

### GitHub Pages 工作流

将 [assets/pages.yml](assets/pages.yml) 复制到网站仓库的 `.github/workflows/pages.yml`：

1. 修改触发分支和需要发布的文件清单。
2. 在网站仓库的 Pages 设置中选择 **GitHub Actions**。
3. 推送后检查对应提交的部署结果，再核对正式页面和资源。

模板默认发布 `index.html`、`style.css`、`script.js`、`.nojekyll` 和 `assets/`。如果添加了其他页面或资源，记得更新文件清单。详细步骤见[发布说明](references/release-and-qa.md)。

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
    ├── build-history.md              # 建站记录
    ├── design-and-content.md         # 内容、字体、双语与主题
    ├── media-and-qr.md               # 图片、视频、日期与二维码
    ├── interactive-components.md     # 页眉、地图、书架与音乐
    └── release-and-qa.md              # 发布、验收与缓存排查
```

## 参考文档

按需要查看对应文档：

| 文档 | 内容 |
| --- | --- |
| [设计与内容](references/design-and-content.md) | 页面排版、字体、双语和主题切换 |
| [媒体处理](references/media-and-qr.md) | 照片、视频、拍摄时间和二维码 |
| [交互组件](references/interactive-components.md) | 页眉、校园地图、书架和音乐卡片 |
| [发布说明](references/release-and-qa.md) | Pages 配置、上线检查和缓存问题 |
| [建站记录](references/build-history.md) | 示例网站的开发过程 |

## 反馈与改进

有问题可以提 [Issue](https://github.com/peppaoinks/github-pages-personal-site/issues)，说明遇到的情况，附上运行环境和报错信息。也欢迎提交 Pull Request。
