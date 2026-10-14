# AI 翻车现场（综艺花字 · 吐槽短片）

用仓库第 15 种风格「综艺花字」（[18-hanazi](../18-hanazi/)）给一段聊天录屏配反应字幕：某助手每句话都要附带一串「不能」，就是不回答「我额度回来了吗」。1080×1920 · 30 fps · 10 秒。

## 渲染

```bash
# 在仓库根目录
npm install
pip install -r requirements.txt
python3 demos/roast-hanazi/audio.py      # 配乐 → demos/roast-hanazi/out/audio.wav
npm run render -- demos/roast-hanazi     # 画面 → demos/roast-hanazi/out/video.mp4（自动混入 out/audio.wav）
```

- Chrome 路径用 `MG_CHROME` 指定；Windows / Linux 上没有合适显卡时设 `MG_GPU_ARGS="--no-sandbox --use-angle=swiftshader --enable-unsafe-swiftshader"`。可以加 `--workers 4` 并行。
- 字体按 [assets/fonts/README.md](../../assets/fonts/README.md) 放好。本片用到：Resource Han Rounded、Alimama ShuHeiTi、Douyin Sans、LXGW Marker Gothic、ZCOOL KuaiLe、Luckiest Guy、Noto Sans SC。缺哪个，渲染日志里会出现 `font "…" not loaded` 警告，页面退回系统中文字体（不会出方块，但字形和设计稿不同）。
- `lib/audio/samples/index.json` 列了 `crash/cymbal_crash1_mf2.flac`，仓库里却没有这个文件；`audio.py` 只加载三次镲片，避开了它。

## 文件

| 文件 | 内容 |
|---|---|
| `index.html` | 画面：聊天界面（录屏层）+ 花字层，`window.renderAt(t)` 画任意时刻 |
| `cues.json` | 节拍表，画面和声音都读它 |
| `audio.py` | 18-hanazi 的综艺配乐 + 卡通音效 + 合成观众声，按本片节拍重排 |
| `prompt.md` | 制作用的完整提示词（18-hanazi 原提示词，只换了 Creative seed） |

## 节拍

| 时间 | 画面 | 声音 |
|---|---|---|
| 0–1.2 s | 「Tibo 重置了！」发送，「好耶！」逐字弹出 | pop ×3 + 观众「耶～」 |
| 0.85–1.5 s | 某助手「正在输入…」，1.15 s 起长篇回复飞速滚动 | 1.0–1.5 s 木琴上行 + 滑哨，1.5 s 全乐队进 |
| 1.5–4.375 s | 每数到一个「不能」，原文里高亮一下，右上角「第 N 个“不能”」跳一格，1→14；六句重点逐拍弹出 | 每跳一格一个 pop，F 大调逐级升高，14 落在最高的 F7 + 叮 |
| 2.1 s | 品牌名打码，「哔～」 | 哔 |
| 4.5 s | 「？？？」 | 搓碟 + boing ×3 |
| 5.0 s | 印章「时区守门员」 | 盖章 + 观众「噢～」 |
| 5.5–6.9 s | 「所以我额度回来了吗？」+「（小声）」+ 汗滴，镜头慢推 | 音乐压到耳语音量 |
| 7.0 s | 「请前往 Settings → Usage 查看。」切成贴纸上放射线，「震惊！！」爆炸框 | 搓碟刹停音乐 → 观众哄笑 |
| 8.4 s | 定格成卡片 | 快门，8.5 s 收尾和弦 |
| 8.8–9.3 s | 印章「防御性满分」，小字「翻译成人话：没结论」 | 盖章，「没结论」落在 ba-dum-tss 上 |

彩蛋只放了一个：长文末尾流过的那句「尽管 a 小于 b，但这不意味着 b 一定小于 c……」。

## 素材与授权

- 画面全部由代码绘制（聊天界面、头像、花字、印章），没有照片，也没有任何真实厂商的 logo、配色或界面；回复里的品牌名打了码。
- 颗粒纹理：`assets/textures/grain/grain_fine_2048.png`（仓库自带）。字体及其授权见 assets/fonts/README.md。
- 声音全部由 `lib/audio` 合成；镲片等乐器采样来自仓库自带的 VCSL（CC0）。
