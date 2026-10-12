# 仓库、Pages、验收与缓存

## 项目与网址

先看实际 Git 根目录、远端、工作区。原站源码在课程目录的 `personal-homepage`，同名桌面文件夹为空，不据此重建。并行任务存在时不重置、覆盖或混入其未提交改动。

用户主页仓库为 `OWNER.github.io`，项目站通常为 `OWNER.github.io/REPO/`，相对资源路径适配子路径。品牌名和账号名可不同，改 logo 不必改 GitHub 账号；原站最终保留 peppaoinks 网址，没有完成账号改名/新组织。

有用户授权且目标明确时使用 CLI/连接器建仓和推送。不要打印 token；代理/网络拒绝按当前权限机制处理，不擅改全局代理或关闭安全设置。

## 发布样板

将 `assets/pages.yml` 复制到**网站仓库**的 `.github/workflows/pages.yml`，调整分支和文件清单。版本来自原站成功部署，不保证永远最新；新环境按 [GitHub 官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)核对。

Pages Source 选择 GitHub Actions，使用 github-pages environment；准备静态目录、上传 artifact、部署。需 contents 读取、pages 写入、id-token 写入权限，部署输出包含正式 URL。

原站公开白名单：index.html、style.css、script.js、.nojekyll、assets/。README、工具、原始素材和其他工作文件不发布。增加 PDF、文章页面或新脚本时同步白名单，不能简单上传整个工作区。

CLI 先读 `repos/OWNER/REPO/pages` 确认现状，首次启用才创建配置，已有配置只改必要字段；不要无条件重试建仓或建配置。

## 本地验收

在网站目录运行 `python3 -m http.server 8080 --bind 127.0.0.1`。先验证当前变化，再按需要覆盖：

| 维度 | 核对 |
| --- | --- |
| 语言/主题 | 中英 × 深浅，偏好刷新保留，地图/相册/标签同步 |
| 屏幕 | 桌面与约 375px 手机，英文不使整页横向溢出，轨道自身滚动正常 |
| 内容 | 日期、地点、经历真实，无空链接，删除在另一语言也生效 |
| 相册/视频 | 按钮、圆点、键盘、手势、预加载，切换后暂停视频 |
| 地图 | 延迟加载、定位/全图/缩放、失败状态，手机可滚页面 |
| 书架/音乐 | 封面匹配、按钮边界、减少动态效果、真实外链 |
| 页眉 | 顶部/中间/居中，无重叠，锚点不被遮住 |
| QR | 实际深浅与手机/桌面截图解码，payload 相同 |
| 构建 | 新资源进入公开目录，无夹带工作文档/原始素材 |

改动 JS 用 `node --check`，差异用 `git diff --check`，静态资源用 `scripts/check_site.py SITE`。脚本不执行 JS，不证明动态行为。浏览器工具不可用时说明未做视觉验证，HTTP 200 不能代替版式验收。

## 推送后验证

只暂存本次变化，核对暂存差异与提交身份。推送前获取最新远端，冲突先看新变化，不为省事强推。

1. 记录目标 SHA，推送到正确远端/分支。
2. 用 SHA 找对应 Pages 工作流，不默认列表第一条就是本次。
3. 等工作流成功，失败读任务日志并有限重试。
4. 用正式 URL 读取 HTML 和改动资源，与目标提交的发布快照逐字节比较。
5. 核对新增图片、PDF、JS 可访问，必要时线上浏览关键交互。

```bash
python3 /path/to/skill/scripts/check_site.py /path/to/clean-site --base-url https://OWNER.github.io/ --cache-tag FULL_COMMIT_SHA
```

脚本比较当前本地文件，执行时不能继续修改；并行工作时从目标提交导出临时目录。未公开的 README 等不参与比较。

## 缓存排查

先核对线上 HTML、引用的 CSS/JS URL 和部署 SHA。原站图库与栏目删除曾遇到旧显示，用资源版本号和带版本的查看链接帮助刷新。

只给页面 URL 加 ?v= 不一定刷新其图片/CSS/JS。替换资源时更新其引用 URL、文件名或缓存策略。确认线上是新版后再建议硬刷新，不让“可能缓存”替代调查，部署未成功不说已上线。

## 交付

给正式页、源码/提交、完成能力及验证范围。缺 PDF、未确认曲目、无法访问个人记录等影响使用的限制明确说明；新增维护入口更新现有项目文档，保持数据流说明与实现一致。
