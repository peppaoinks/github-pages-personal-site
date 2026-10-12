# 建站过程与证据

此文件是建设回顾与维护上下文，不把每个个性化决定变成通用要求。依据为原站 Git 历史、README、实际源码与建站对话，核对日期为 2026-10-12（北京时间）。

- [正式网站](https://peppaoinks.github.io/)
- [源码仓库](https://github.com/peppaoinks/peppaoinks.github.io)
- [总结基线 637f237](https://github.com/peppaoinks/peppaoinks.github.io/tree/637f237)：引用源码优先固定此版本，避免后续工作混入历史。

## 从需求到发布

1. **初建。** 用户只给姓名与 GitHub 用户名；实现原生静态初版、两个真实公开项目、联系入口、手机适配及深浅主题，建用户主页仓库、配置 Actions、启用 Pages，检查部署与线上资源。初次浏览器不可用时明确没有视觉验收。
2. **收集信息。** 逐步补充中文/英文名、学校、专业、年级、兴趣和社交链接，新增随笔空状态与赞助预留。双语从并排展示改为按钮切换，每次只显示一种语言。
3. **视觉迭代。** 改为阅读型衬线并加粗中文，放大首屏姓名、身份和介绍，将邮箱移到首屏。品牌加入 24，后改 felixzhou 字标。
4. **网址与社交。** 曾讨论其他 Pages 网址，最终保留原账号和网址；没有执行账号改名或新建组织。接入 LinkedIn，移除用户不想公开的入口。
5. **文案与个性。** 加入教育、足球、音乐、英语教学和哈利波特兴趣，主题改斯莱特林绿；多次重写生硬文案，删除课程列表、重复标签和底部口号。
6. **相册与视频。** 核对附件和地点，读取可得日期，无日期不猜；按成长顺序排列，支持键盘、按钮、手势，视频手动播放。摄影模块留空，简历入口等待真实 PDF。
7. **素材优化。** 图片转 WebP、限制尺寸、移除元数据，提前加载相邻项；MOV 转网页 MP4；caption 简化为地点和确认日期。
8. **赞赏码。** 从直接图片展示改为离线读 payload、重新生成内嵌 SVG，做深浅模式和绿底黄块，统一背景并去外框；实际截图解码验证与原码一致。
9. **页眉。** 固定头部，滚动时字标移向中央并放大；教育日期对齐，窄屏导航避免碰撞。
10. **校园地图。** 延迟加载本地 Leaflet 配在线 OSM，核对具体校区坐标，双语弹窗及主题；按反馈修正同校区两段不连续就读时间。
11. **文字链接。** 学校、俱乐部和兴趣名称直接加官方链接，拆分翻译段落保留链接；移除个人微信号，按用户偏好去掉下划线。
12. **近况与封面轨道。** 先搭近况再提问，最终只留四本真实阅读书；加书封和专辑滑动效果，记录来源。音乐按喜欢的歌手选候选曲目，没有称为真实最近播放；音乐移到阅读下方，统一标题。
13. **持续验收。** 每轮按变化检查手机/桌面、中英和主题，提交推送，查对应部署，比对线上文件。仍看到旧内容时核对资源和缓存。

## 基线能力边界

- 随笔为空，没有文章生成/CMS；摄影数据为空，没有作品大图浏览；简历尚未接入 PDF。
- 四本书来自用户，七首歌为候选，来源清单和 HTML 卡片手动同步。
- 另一个后续任务正在探索每两周更新真实最近播放；本基线没有调度或私人账户同步。完成与否须检查该任务实际产物。
- Skill 保留可复用方法和公开证据，不打包原始附件、个人码、完整聊天记录或本机私有路径。

## 经验索引

信息/字体/链接/双语见 design-and-content；日期/压缩/视频/QR 见 media-and-qr；地图/页眉/轨道见 interactive-components；白名单/部署/缓存见 release-and-qa。执行任务从 SKILL.md 选择需要的资料，无需默认读取全历史。

总结期间新增的静态检查还发现：基线 Leaflet CSS 引用了未随库复制的 images/layers.png、images/layers-2x.png 和 images/marker-icon.png。原站采用自绘 divIcon 且未使用图层切换控件，这不能直接说明当前页面可见功能失效；但移植时应带齐所用库资源，或明确移除不用的规则，不把“页面看起来正常”当成资源完整证明。本次总结没有修改原站。

## 完整提交索引

以下包含基线的全部 29 次提交，按 Git 历史顺序排列。

| 提交 | 实际变更 |
| --- | --- |
| [9fbf010](https://github.com/peppaoinks/peppaoinks.github.io/commit/9fbf010) | Build Fangjing Zhou personal website |
| [3da8279](https://github.com/peppaoinks/peppaoinks.github.io/commit/3da8279) | Add bilingual profile, personal bio, essays and social links |
| [f61d170](https://github.com/peppaoinks/peppaoinks.github.io/commit/f61d170) | Use Claude-inspired serif typography for headings and reading |
| [c995291](https://github.com/peppaoinks/peppaoinks.github.io/commit/c995291) | Give Chinese serif text fuller medium and semibold weights |
| [c54963e](https://github.com/peppaoinks/peppaoinks.github.io/commit/c54963e) | Replace X with LinkedIn and incorporate 24 into the personal mark |
| [9f33dd0](https://github.com/peppaoinks/peppaoinks.github.io/commit/9f33dd0) | Increase homepage profile text readability |
| [098dff0](https://github.com/peppaoinks/peppaoinks.github.io/commit/098dff0) | Scale hero introduction to fill the left column |
| [a393d61](https://github.com/peppaoinks/peppaoinks.github.io/commit/a393d61) | Move contact details into hero and enlarge biography |
| [474630d](https://github.com/peppaoinks/peppaoinks.github.io/commit/474630d) | Add education history and refine homepage text |
| [1637527](https://github.com/peppaoinks/peppaoinks.github.io/commit/1637527) | Make the personal introduction more conversational |
| [41d8a32](https://github.com/peppaoinks/peppaoinks.github.io/commit/41d8a32) | Add dated personal gallery, photography section and Slytherin theme |
| [ad92021](https://github.com/peppaoinks/peppaoinks.github.io/commit/ad92021) | Simplify gallery captions, optimize photos and show support QR inline |
| [8a2d85b](https://github.com/peppaoinks/peppaoinks.github.io/commit/8a2d85b) | Use felixzhou wordmark throughout the personal website |
| [fcf5405](https://github.com/peppaoinks/peppaoinks.github.io/commit/fcf5405) | Remove footer slogan in both languages |
| [d865b7d](https://github.com/peppaoinks/peppaoinks.github.io/commit/d865b7d) | Improve scrolling header, logo contrast and inline support QR |
| [da0235b](https://github.com/peppaoinks/peppaoinks.github.io/commit/da0235b) | Grow centered logo and align education dates; remove requested copy |
| [45adeaa](https://github.com/peppaoinks/peppaoinks.github.io/commit/45adeaa) | Add lazy-loaded campus map to education section |
| [dc6c739](https://github.com/peppaoinks/peppaoinks.github.io/commit/dc6c739) | Adapt inline support QR colors to light and dark themes |
| [00601be](https://github.com/peppaoinks/peppaoinks.github.io/commit/00601be) | Correct Shenzhen school campus periods and add English tutoring experience |
| [64e281f](https://github.com/peppaoinks/peppaoinks.github.io/commit/64e281f) | Add five life photos with verified dates and locations |
| [36ea82c](https://github.com/peppaoinks/peppaoinks.github.io/commit/36ea82c) | Refresh gallery asset cache versions |
| [02af2b2](https://github.com/peppaoinks/peppaoinks.github.io/commit/02af2b2) | Link Harry Potter bio to official Sorting Ceremony |
| [fcbfa9b](https://github.com/peppaoinks/peppaoinks.github.io/commit/fcbfa9b) | Embed official links in names and remove personal WeChat ID |
| [d42607f](https://github.com/peppaoinks/peppaoinks.github.io/commit/d42607f) | Use green and yellow QR colors in dark mode |
| [4a0a7d6](https://github.com/peppaoinks/peppaoinks.github.io/commit/4a0a7d6) | Unify dark QR background and remove inline link underlines |
| [9049c67](https://github.com/peppaoinks/peppaoinks.github.io/commit/9049c67) | Add Now reading shelf and sliding music covers |
| [aed9b99](https://github.com/peppaoinks/peppaoinks.github.io/commit/aed9b99) | Remove focus line from Now section |
| [624ff22](https://github.com/peppaoinks/peppaoinks.github.io/commit/624ff22) | Place Currently listening below reading shelf |
| [637f237](https://github.com/peppaoinks/peppaoinks.github.io/commit/637f237) | Unify Chinese reading and listening headings |
