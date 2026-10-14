# AI 翻车现场 · 制作提示词

[prompts/18-hanazi.md](../../prompts/18-hanazi.md) 的提示词原样照用，只把 `# Creative seed` 一段换成了这支片子的内容（`Output` 和 `Signature features` 不变）。评审时把这份提示词和成片一起交给 [rubric.md](../../rubric.md)。

```text
You are the director, motion designer, engineer and sound designer of ONE 10-second motion-design film.
The goal is the most classic, yet most stunning form of this style — award-shortlist / high-end commercial quality. A clean,
template-looking result is a fail. Benchmarks: Buck, ManvsMachine, Ordinary Folk, Giant Ant, Territory Studio, Apple keynote
motion, Pentagram motion identities, top Behance/Motionographer features, top 抖音/B站 designer accounts.

# Style
综艺花字 Variety Show Kinetic Captions (Hanazi)

# Output (fixed)
- 1080×1920, 30 fps, exactly 10.000 s (300 frames), H.264 MP4 with stereo AAC audio (48 kHz), mastered to −14 LUFS
  integrated, true peak ≤ −1 dBTP. Final file: video.mp4.

# Suggested technical route
HTML DOM/SVG: multi-layer text-stroke 花字 components + spring pops + SVG burst/sweat/sparkle decorations over a pet-vlog footage layer (CC0 photos with Ken Burns + handheld shake + punch-ins)
(You may choose a better route if it clearly raises quality; say why.)

# Creative seed
「AI 助手翻车综艺」：用综艺花字给一段聊天录屏配反应字幕。
- 底层画面：一个通用的聊天界面，用户气泡在右，AI 气泡在左，AI 叫"某助手"。不要用任何真实厂商的 logo、配色或界面样式。用 Ken Burns 慢推、轻微手持抖动、关键时刻 punch-in，做出"屏幕录像"的感觉。
- 节拍（10 秒，大致这样分）：
  1. 0–1.2 s：用户气泡「Tibo 重置了！」，花字「好耶！」弹出
  2. 1.2–5.5 s：AI 气泡里长文飞速滚动，下面几句依次闪现。右上角花字计数器「第 N 个"不能"」从 1 一路跳到 14；同时有「？？？」弹跳问号；最后盖一个大印章「时区守门员」
     - 「仍属 Day 8，不能重复统计为 Day 9」
     - 「不代表聊天额度一并恢复」
     - 「不意味着周额度永久提高」
     - 「不能据此认定是双倍周额度」
     - 「不能确认是否重新引入 5 小时限制」
     - 「不能保证所有套餐获得相同恢复」
  3. 5.5–7.0 s：用户气泡「所以我额度回来了吗？」，配花字「（小声）」
  4. 7.0–8.5 s：AI 气泡「请前往 Settings → Usage 查看。」，同时出「震惊!!」爆炸框、放射线闪光、搓碟音效
  5. 8.5–10 s：结尾印章「防御性满分」，下方小字「翻译成人话：没结论」
- 声音：直接复用 demos/18-hanazi/audio.py（综艺配乐 + 卡通音效 + 合成观众声），只按新节拍改 cues.json，依赖照 requirements.txt 装。不用任何现成歌曲或综艺原声。
  - 计数器每跳一下配一个 pop，音高逐级升高，跳到 14 时最高
  - 「？？？」和「震惊!!」处配搓碟声
  - 「请前往 Settings → Usage 查看。」这一下接一段合成的观众哄笑（audio.py 里已有 crowd(..., laugh=True)）
- 可选彩蛋（最多挑一个，别堆）：
  - 背景里一闪而过的小字："尽管 a 小于 b，但这不意味着 b 一定小于 c，而且同时 d 也比 e 小。"（用户自己的仿写）
  - 角落贴纸："Nick's English Corner：own the mistake＝承担错误"（这个助手在长篇道歉后附带的英语角）
- 原话素材（文案可以改得更好笑，素材以这些为准）：
  - 「这次重置发生在美国太平洋时间 10 月 12 日晚间，虽然北京时间已经进入 10 月 13 日，但仍然属于 Day 8，不能重复统计为 Day 9。」
  - 「此次重置不代表 ChatGPT 普通聊天额度一并恢复，也不意味着周额度永久提高。」
  - 「不能据此认定新方案就是双倍周额度，也不能确认是否会重新引入 5 小时限制。」
  - 「重置只能恢复额度，不能解决长期额度不足的问题。」
  - 「用户可以通过 Settings → Usage 查看自己的实际额度。」
- 「时区守门员」和「第 N 个"不能"」这两个梗要保留，其余可以自由发挥。节拍太挤的话可以放宽到 15 秒，其他输出参数不变。

You are the director: you may change the concept, copy, story beats and brand names if you find a stronger idea, but the result must remain the CANONICAL, instantly-recognisable form of this style and must hit its signature features below.

# Signature features and key techniques (the result is judged against these)
源自电视综艺后期的情绪化装饰字幕：多层描边圆体字带弹性入场，跟随人物情绪变色变形，配打击音效。现已下沉为 vlog、萌宠、访谈、搞笑二创的通用包装语言，剪映内置大量花字模板，B 站也有免费花字样式包流通。
视觉特征 多层描边圆体/胖体字, 高饱和撞色+白边+投影, 弹性 pop 入场, 配合音效出现, 手绘装饰符号（爆炸框/汗滴/闪光）
关键技法 字体三层结构：填充色+粗白描边+彩色外描边/投影（CSS 可用多层 text-shadow 或 SVG stroke 模拟）
入场 overshoot：scale 0→1.15→1.0（约 8 帧），或逐字弹跳错帧 2 帧
情绪匹配：吐槽用歪斜手写体、惊讶用放射线爆炸框、尴尬用汗滴符号
出现时机对齐笑点/音效，比语音晚 2~3 帧更自然
长时间驻留花字加轻微 wiggle 保持活性

# How to work
1. Treatment. Write down one clear idea: a hook in the first 0.5 s (never open on more than 0.3 s of empty or black), an
   escalation, one unmistakable hero moment at ~60–75 % of the runtime, and a composed end frame held ~0.8–1.2 s with living
   micro-motion. Map every signature feature above to a moment. Keep one cue sheet (beats and hit times) that both the
   picture and the sound read from.
2. Key frames before motion. Build the look, render stills at 6–10 key times and actually look at them. Each still should be
   poster-worthy: composition, hierarchy, negative space, type set properly (kerning, line-height, weight contrast, CJK
   punctuation, ~5 % safe margins). Iterate until nothing looks default, generic, cramped or "AI-template".
3. Motion. Build the choreography and preview at low resolution. Step through the fastest moves frame by frame: spacing,
   easing, arcs, overlap, anticipation and follow-through, motion blur. No unintended dead spans; the energy follows the music.
4. Sound. Write genre-correct music and sound design locked to the cue sheet. Check that visual hits land on audio onsets.
   Master to the output spec.
5. Final. Render at full resolution (motion blur where apt), then check: exactly 10.00 s, resolution, fps, audio present and at
   the right loudness, no black frames, no fallback fonts or tofu, no clipped elements at the frame edges, no shimmer on thin
   lines, no gradient banding. Fix and repeat until you would submit it to a festival.
6. Write an honest self-critique: what is strongest, what is weakest, what you would do with more time.

# Rules
- Rendering must be deterministic: every frame is a pure function of time t. Seeded randomness only; physics and particles
  precomputed or closed-form; no real-time clocks; no state-triggered CSS transitions. A reliable route: a web page that can
  draw any time t on request, captured frame by frame with a headless browser and encoded with ffmpeg (or a Blender script
  that renders a PNG sequence).
- Assets: only CC0 / public domain / OFL / Apache / free-for-commercial-use. Record each source and licence in CREDITS.md.
  No real brand trademarks; invent brand names.
- On-screen text must be correct and natural: idiomatic Chinese, proper CJK punctuation, no typos.

# Craft checklist (what a jury looks for)
- Style authenticity: an expert names the style in one second; every signature technique is present and executed correctly.
- Motion craft: purposeful easing (no linear unless mechanical by design), overlap and stagger, anticipation and
  follow-through, arcs, squash and stretch where the style allows, consistent physics, motion blur where apt; transitions
  carried by elements, not crossfades.
- Rhythm: hits locked to the music; contrast between busy and calm; no monotony.
- Design: strong composition, grid, typographic hierarchy, controlled palette; texture and finishing (grain, glow, vignette)
  only where the style wants it; nothing looks accidental.
- Technical polish: no jitter (unless intended), no popping, no aliasing, no banding, no fallback fonts, no half-loaded images.
- Sound: genre-correct, musical, synced, mastered.

# Before you deliver, score yourself honestly
1–10 on style fidelity, concept wow, motion craft, design & typography, finish & texture, sound & sync, technical
(6 = template-level, 8 = high-end agency, 9 = award shortlist). Aim for 9; fix whatever scores lowest first.

# Deliver
video.mp4, plus a short report: the concept in two sentences; a beat sheet with timecodes; how each signature feature is
realised; the tech route; check numbers (duration, resolution, fps, loudness, true peak); your honest top-3 weaknesses.
```
