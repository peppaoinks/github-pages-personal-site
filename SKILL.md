---
name: github-pages-personal-site
description: 从真实建站经验搭建、迭代和发布原生 HTML/CSS/JavaScript 的 GitHub Pages 个人主页。适用于双语切换、深浅主题、相册与视频、校园地图、阅读书架、音乐封面、赞赏码和上线验证，也用于维护 Felixzhou 的 peppaoinks.github.io。不会把文章系统、账户歌单同步或后端服务视为已有功能。
---

# GitHub Pages 个人网站

把用户逐步提供的信息变成可以持续维护的静态个人网站。此 skill 提炼自 `peppaoinks/peppaoinks.github.io` 的完整初建与 29 次提交，覆盖内容、设计、素材、交互、发布及反馈修订。

## 先定位项目与需求

- 检查当前目录、适用的 `AGENTS.md`、实际 Git 根目录、远端和未提交改动。同名桌面文件夹可能为空；先从现有项目或建站记录定位真实源码。
- 区分新建、维护、添加组件、处理素材和排查线上版本，仅执行本次需要的部分。沿用现有技术栈，不为小改动迁移框架；新建此类主页默认原生静态三件套。
- 获取愿意公开的姓名、身份、语言、项目和联系方式；缺内容时先做可扩展布局。已有回答不重复询问，无内容模块隐藏或使用简洁空状态。
- 网址、文件与地点对应、账号来源确实无法确定时再提问，继续完成不依赖答案的部分。

## 按需读取

| 当前工作 | 资料 |
| --- | --- |
| 原站从初版到最终版本的完整过程 | [references/build-history.md](references/build-history.md) |
| 信息收集、排版、字体、品牌、双语、主题 | [references/design-and-content.md](references/design-and-content.md) |
| 相册、HEIC/JPEG/MOV、日期、压缩、二维码 | [references/media-and-qr.md](references/media-and-qr.md) |
| 页眉动画、校园地图、书架、音乐滑动卡片 | [references/interactive-components.md](references/interactive-components.md) |
| 仓库、Pages、验收、缓存、提交与部署 | [references/release-and-qa.md](references/release-and-qa.md) |

## 实现流程

1. **搭出可用初版。** 建立首屏、关于、真实公开项目和联系入口，保证小屏可读、键盘可用。先确定内容层级，再根据截图调整字体与间距。
2. **逐步补充真实内容。** 按用户提供的信息加入教育、爱好、相册、近况、随笔和摄影；简历 PDF 未提供时隐藏入口。
3. **全站统一。** CSS 变量管理主题；语言切换同步正文、按钮、替代文字、页面标题、描述及地图文字，默认 HTML 与翻译字典一致。
4. **先确认素材，再加工。** 原图只读，先读取日期与方向，再生成网页副本；照片、封面和二维码分别处理。
5. **交互渐进增强。** 书架使用原生横向滚动；相册支持按钮、键盘和手势；地图接近视口再加载；视频手动播放；动画尊重减少动态效果偏好。
6. **本地验收。** 检查中文/英文与深浅主题的四种组合、桌面/手机和真实操作；按发布文件白名单构建预览目录，确认新增资源完整。
7. **按任务授权发布并验证。** 新建、推送和发布的权限来自用户请求，skill 本身不构成授权。找到目标提交对应的部署，再核对线上文件与关键行为。

用户反馈优先于旧设计。删除、改名、移位或移除联系方式时，同步处理默认 HTML、翻译、导航、无障碍标签和项目文档。不要把原站的绿色、logo、栏目顺序和七首歌曲强加到其他人的主页。

## 可复用资源

- [assets/pages.yml](assets/pages.yml)：原站成功运行的静态 Pages 工作流样板，复制到目标网站 `.github/workflows/pages.yml` 后调整分支与文件清单；它在 skill 仓库中不会自行部署。
- [scripts/optimize_images.py](scripts/optimize_images.py)：用 Pillow 生成 WebP 副本，记录源 EXIF 日期、方向与体积，默认不覆盖。HEIC 需要可选的 pillow-heif 或先用系统工具转换。
- [scripts/check_site.py](scripts/check_site.py)：用 Python 标准库检查本地资源、HTML 锚点与 JSON，可对线上静态文件逐字节比对；不替代浏览器验收。

以下路径须替换为实际位置：

```bash
python3 /path/to/skill/scripts/optimize_images.py photo.jpg --output-dir /site/assets/gallery --report /tmp/media-report.json
python3 /path/to/skill/scripts/check_site.py /path/to/site
python3 /path/to/skill/scripts/check_site.py /path/to/site --base-url https://OWNER.github.io/ --cache-tag COMMIT_SHA
```

## 完成标准

- 不以推送成功替代部署成功，不以文件一致替代视觉与交互验收。
- 不编造照片日期、个人经历、阅读状态或播放记录；候选歌单与真实最近播放分别说明。
- 空的随笔/摄影模块不等于已完成内容管理系统；简历入口准备好不等于已接入 PDF。
- 交付正式网址或本地预览、源码/提交链接、验证结果和实际限制；新增素材记录来源与维护入口。
