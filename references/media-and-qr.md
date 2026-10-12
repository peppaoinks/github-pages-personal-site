# 图片、视频、日期与二维码

## 先读取再转换

原始素材只读，在 `assets/` 生成副本。先读取方向、日期、尺寸和格式。EXIF `DateTimeOriginal` 优先；文件系统时间、上传时间、文件名不足以证明拍摄日期。视频 creation_time 可能是 UTC 或导出时间，核对语义和时区，无法确认时不显示。

地点来自用户确认或核验数据。没有日期的照片可按已确认成长阶段排列，只显示地点。公开副本移除 EXIF/GPS；媒体处理报告留本地，发布来源说明只保留必要字段。

## 图片

原站先把 HEIC/JPEG 转较大的 JPEG，再改成最长边 1200px 的 WebP，改善加载。1200px 是本案例取舍，按显示尺寸与设备像素比调整，不强制所有资产统一尺寸。

`scripts/optimize_images.py` 默认最长边 1200、质量 78，先应用 EXIF 方向，再缩放并生成无 EXIF 副本，保留透明度。报告读取到的日期不自动等同于已确认网页日期。默认拒绝覆盖，更新已有衍生图时才加 `--overwrite`。

```bash
python3 /path/to/skill/scripts/optimize_images.py /input/photo.jpg --output-dir /site/assets/gallery --report /tmp/media-report.json
```

依赖 Pillow。HEIC 可选 pillow-heif，或 macOS 使用 `sips -s format jpeg INPUT.HEIC --out /tmp/intermediate.jpg`；先读取原图日期和方向，避免中间文件丢失信息。不要覆盖原文件。

书封保留纵向比例，音乐封面通常方形，原站专辑封面为 600px WebP。核对书名、作者及版本；来源优先出版社/作者/音乐官方目录，其他可信书目来源需注明。封面和品牌标识的权利不因复制到本地而转移。

“嵌入网站”可用本地静态资源完成，不必把所有照片转为 base64 塞进 HTML。保留独立缓存，优化副本、显示尺寸与预加载策略。

## 视频

原站 MOV 转 H.264 MP4 并生成 poster。以下为复用建议，非历史命令逐字记录，按方向、音轨和清晰度调整：

```bash
ffmpeg -i INPUT.MOV -vf 'scale=1200:1200:force_original_aspect_ratio=decrease:force_divisible_by=2' -c:v libx264 -crf 26 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart OUTPUT.mp4
ffmpeg -ss 1 -i OUTPUT.mp4 -frames:v 1 /tmp/poster.png
```

工具缺失时先检查现有运行时和系统能力。转完实际播放，核对方向、声音和加载。前端使用 controls、playsinline、preload=none、poster，手动播放；离开该 slide 时暂停，不让相册键盘或手势抢走视频原生控件。

## 相册

数据字段：`src`、`altZh`、`altEn`、`captionZh`、`captionEn`，可选 `date`（YYYY-MM-DD）、`position`；视频另有 `type:"video"`、`poster`。

原站选择 logo 第一、照片从小到大、视频最后；caption 只留地点和确认日期，logo 无 caption。其他站点按用户选择。精简 caption 不意味着删去无障碍 alt。

按钮、圆点、方向键和横向手势提供等价切换。手势须明显以横向为主，保留纵向页面滚动。预加载当前和相邻照片，其他图片延迟加载，视频按需；语言切换只更新当前文案。

## 内嵌赞赏码

原站要求无需点击即可看到完整码，后续改内嵌 SVG、深浅配色、背景统一和无边框。

1. 从用户原图离线解码；macOS 可用 Vision，其他环境用可用的可靠解码器。
2. 对 payload 原样重新编码，不 trim、不改 URL。原站 CoreImage QR generator 生成矩阵，再转 SVG path，设置清晰边缘。
3. 留至少四个模块静区，完整背景 rect 和前景 path；不裁切，不使用照片有损压缩。
4. rect/path 独立样式类，以主题变量控制。原站深色为页面同色绿底与黄块；浅前景/深背景有识别器兼容性差异，不能仅看对比认定可用。
5. 对实际网页截图分别检查深浅主题和手机/桌面，解码并与原 payload 比较；尽可能用目标扫码 App 实测。验证不了就说明限制，保留已验证配色。

背景不一致时检查容器、SVG rect、模块三个层次及最终生效 CSS；去外框不能破坏静区。只报告 payload 是否一致，不将支付内容写入日志、公开 skill 或示例资产。本 skill 不包含真实赞赏码或私人媒体。
