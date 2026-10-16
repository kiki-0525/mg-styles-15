# AI 翻车现场（综艺花字 · 吐槽短片）

用仓库第 15 种风格「综艺花字」（[18-hanazi](../18-hanazi/)）给一段聊天录屏配反应字幕：某助手每句话都要附带一串「不能」，就是不回答「我额度回来了吗」。1080×1920 · 30 fps · 17 秒（第二版，从 10 秒放长，见下文「第二版改了什么」）。

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

录屏层有自己的时钟，到「定格」就停（滚动、打字、手持晃动全停），花字、计数器和镜头照常走。

| 时间 | 画面 | 声音 |
|---|---|---|
| 0–1.0 s | 「Tibo 重置了！」发送，「好耶！」逐字弹出，0.45 s 定格（镜头推向气泡） | pop ×3 + 观众「耶～」，快门 |
| 1.0–1.5 s | 某助手「正在输入…」 | 木琴上行 + 滑哨，1.5 s 全乐队进 |
| 1.5–7.0 s | 长文飞速滚动；每数到一句重点里的「不能」就定格：画面停住、闪白、镜头 3 帧推到原文里刚高亮的那个词，花字弹出，停够再继续。定格依次停 1 s → 0.5 s ×3 → 0.25 s ×2，越来越快。右上角计数器 1→14 | 每数一个 pop，F 大调逐级升高，14 落在 F7 + 叮；每次定格一声快门 |
| 4.06 s | 品牌名打码，「哔～」 | 哔 |
| 7.5 s | 「？？？」 | 搓碟 + boing ×3 |
| 8.0–9.0 s | 印章「时区守门员」，整屏定格 1 s（六句花字 + 计数 14 + ？？？ 的全家福） | 盖章 + 观众「噢～」 |
| 9.0–10.4 s | 「所以我额度回来了吗？」+「（小声）」+ 汗滴，镜头慢推 | 音乐压到耳语音量 |
| 10.5 s | 「请前往 Settings → Usage 查看。」切成贴纸上放射线，「震惊！！」爆炸框 | 搓碟刹停音乐 → 观众哄笑 |
| 12.0 s | 定格成卡片 | 快门，乐队回来 |
| 12.5 s | 印章「防御性满分」 | 盖章 + 观众「哇～」 |
| 13.0–14.5 s | 彩蛋：Codex GPT-6 Astra 的「审片意见」贴纸滑上来，逐字打出它对第一版的原话 | 通知音 + 键盘声 |
| 14.5 s | 「需要改准」被高亮，计数器跳到 15（变红、抖） | 音阶再升一级到 G7 + 报错音 + 观众「噢～」 |
| 15.0–17.0 s | 「翻译成人话：」→ 15.5 s「没结论」，停 1.5 s 到结尾 | ba-dum-tss + 收尾和弦 + 笑声 |

长文末尾流过的那句「尽管 a 小于 b，但这不意味着 b 一定小于 c……」是原 brief 里的彩蛋；片尾 Codex GPT-6 Astra 的审片意见是第二版加的。

## 第二版改了什么

第一版 10 秒像 2 倍速：录屏一直在滚、镜头一直在漂，没有一帧停下来让人看清。第二版没有整体放慢，而是加了关键帧和定格，做法参考仓库里现成的片子：

- **定格卡片**（18-hanazi）：定格时画面全停、闪白、配快门声；结尾定格成卡片。
- **时间重映射**（19-paperclip、02-line-art 的 punctuation holds）：录屏用一条会在定格处停住的时钟，所以长文、滚动、打字点、手持晃动都会真的停下，不是只把镜头停住。
- **停住的帧也在动**（04-3d-render 的 end-hold creep）：每个定格里镜头再慢推 ~1%，花字继续轻晃，停住但不死。
- 弹幕段下面的聊天正文压暗（平时 30%，定格时 44%，全家福 50%），花字先被读到。
- 「没结论」从 15.5 s 停到 17 s（1.5 s）。
- 计数器前 14 个不变；片尾把 Codex GPT-6 Astra 那句「“14 个不能”的标签需要改准……」本身记成第 15 个。

## 素材与授权

- 画面全部由代码绘制（聊天界面、头像、花字、印章），没有照片，也没有任何真实厂商的 logo、配色或界面；回复里的品牌名打了码。
- 颗粒纹理：`assets/textures/grain/grain_fine_2048.png`（仓库自带）。字体及其授权见 assets/fonts/README.md。
- 声音全部由 `lib/audio` 合成；镲片等乐器采样来自仓库自带的 VCSL（CC0）。
