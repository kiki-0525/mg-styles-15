"""roast-hanazi soundtrack: the 18-hanazi variety bed (pizz / tuba bass / glock / claps) + cartoon SFX + synthetic studio
audience, re-cut to this film's cues.json.
Run: python3 demos/roast-hanazi/audio.py  ->  demos/roast-hanazi/out/audio.wav (+ out/audio_spec.png)"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib', 'audio'))
import mgaudio as mg
from mgaudio import recipes, sfx, drums, synth
from mgaudio.filters import formant, eq as _eq

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, 'cues.json')))
SR = 48000
FR = 1 / 30

# bar 0 = the drop (1.5 s): every 8th-note counter tick and every caption line sits on the grid
m = recipes.variety(duration=C['duration'], bpm=C['bpm'], key='F', drop=C['drop'], build=C['build'], outro=C['outro'], flavor='bouncy', sfx_duck=2.5)
f = m.form
m.tracks['tuba'].gain += 2.5   # more bottom for phone speakers
m.tracks['kick'].gain += 1.0
print(f.summary() if hasattr(f, 'summary') else (f.bpm, f.build, f.drop, f.outro))

# the barrage is a tutti: layered kick + big claps + brass stabs on the drop and on the 14th 不能
fl = m.track('floor', level=m.tracks['kick'].level - 6.0)
fl.loop(lambda v: drums.kick('house', v), 'x...x...x...x...', C['drop'], C['clear'])
m.track('clap2', level=m.tracks['clap'].level + 1, sends={'plate': -12}).loop(lambda v: drums.clap('big', v), '....x.......x...', C['drop'], C['clear'])
br = m.track('stab', level=m.tracks['brass'].level + 4, sends={'hall': -14})
for t in (C['drop'], C['max'], C['stamp1']):
    br.add(synth.stab(f.chord_at(t + .01, 12), 0.4, 0.95, 'brass'), t)
cr = drums.crash()   # one load reused: a 4th crash load would round-robin onto cymbal_crash1_mf2, which is missing from lib/audio/samples
m.track('crash2', level=m.tracks['crash'].level + 2).add(cr, C['drop']).add(cr, C['stamp1'])

# music arc: full through the barrage (it keeps playing under every 定格: frozen picture, living band) -> whisper (小声)
# under the timid question -> record scratch kills the band on the non-answer, the audience laughs into the gap -> the band
# comes back on the freeze card, sits under the reviewer's note, and the ta-da (recipe outro) lands on 没结论
D, E = C['duration'], C['egg']
mus = m.group('music')
mus.automate('gain', [(0, 0), (C['clear'] - .03, 0), (C['send2'] + .05, -13), (C['hero'] + .05, -13), (C['freeze'] - .1, 0),
                      (E - .1, 0), (E, -6), (C['outro'] - .1, -6), (C['outro'], 0), (D, 0)])
mus.automate('lpf', [(0, 20000), (C['clear'] - .03, 20000), (C['send2'] + .1, 1500), (C['hero'], 1500), (C['freeze'] - .1, 20000), (D, 20000)])
m.mute(C['hero'] + 0.03, C['freeze'] - 0.03 - C['hero'] - 0.03)


def crowd(dur, vowels, contour, n=26, seed=0, laugh=False, lvl=-18):
    # synthetic studio audience (from 18-hanazi): n detuned glottal voices -> vowel formants + breath, two independent sides
    rng = np.random.default_rng(seed); N = int(dur * SR); tt = np.arange(N) / SR; out = np.zeros((N, 2))
    for side in range(2):
        y = np.zeros(N)
        for v in range(n):
            f0 = rng.choice([rng.uniform(190, 330), rng.uniform(105, 175)], p=[.6, .4])
            vib = 1 + .012 * np.sin(2 * np.pi * rng.uniform(4.5, 6.5) * tt + rng.uniform(0, 6))
            c = np.interp(tt / dur, *zip(*contour)) * (1 + rng.uniform(-.05, .05))
            ph = np.cumsum(f0 * c * vib) / SR; saw = 2 * (ph % 1) - 1
            on = rng.uniform(0, .09) if not laugh else rng.uniform(0, .18)
            env = np.clip((tt - on) / .07, 0, 1) * np.clip((dur - tt) / (.35 * dur), 0, 1) ** 1.3
            if laugh:   # 'ha-ha-ha' syllables, each voice at its own rate
                r = rng.uniform(4.2, 6.4); syl = ((tt - on) * r) % 1; env *= np.clip(1 - syl / .55, 0, 1) ** 1.5 * (syl < .55)
            y += saw * env * rng.uniform(.6, 1.0)
        nz = rng.standard_normal(N) * .35 * (np.abs(y) / (np.abs(y).max() + 1e-9) + .2)
        y = y + nz
        a, b = formant(y, vowels[0], q=6.0), formant(y, vowels[-1], q=6.0)
        k = np.clip(tt / .14, 0, 1) if len(vowels) > 1 else np.ones(N)
        out[:, side] = a * (1 - k) + b * k
    out /= np.abs(out).max() + 1e-9
    s = mg.Sound(out, sync=0.0).loud(lvl)
    return _eq(s, [('hp', 140), ('pk', 420, -2.5, .8), ('hs', 3000, 4.0)])   # presence lift, less boxy low-mid


# --- hook: badge slam, message sent, 好耶！ pops + cheer, first 定格
m.sfx(sfx.pop('cork', pitch=0.75), at=0.02, gain=-6)
m.sfx(sfx.swish(0.3), at=0.1, gain=-8)
m.sfx(sfx.swish(0.2, direction=1, seed=5), at=C['send1'] - 0.04, gain=-10, pan=0.35)
m.sfx(sfx.pop('bubble', pitch=1.2), at=C['send1'], gain=-8, pan=0.35)
for i, t in enumerate(C['yay']):
    m.sfx(sfx.pop('mouth', pitch=1.0 + 0.14 * i), at=t - FR, gain=-3, pan=0.1 + 0.15 * i)
m.sfx(crowd(0.75, 'ea', [(0, .95), (.25, 1.18), (1, 1.05)], n=24, seed=5), at=C['yay'][0] + 0.02, gain=-6, verb=-9, send='hall')   # 耶～
m.sfx(sfx.shimmer_hit(f.chord_at(0.5)[-1] + 12), at=C['yay'][2] + 0.03, gain=-10, pan=0.3)
m.sfx(sfx.boing(pitch=1.5, dur=0.25), at=C['yay_hop'], gain=-14, pan=0.2)
# every 定格 clicks like a camera shutter (the 时区守门员 one has its stamp instead)
for i, (a, b) in enumerate(C['freezes']):
    if a != C['stamp1']:
        m.sfx(sfx.shutter('phone'), at=a, gain=-12 if i == 0 else -15, pan=0.15)
m.sfx(sfx.pop('soft', pitch=1.6), at=C['yay_out'], gain=-12, pan=0.2)

# --- the AI starts typing, then the 不能 barrage (stream runs, freezes on each caption line)
for i in range(3):
    m.sfx(sfx.blip(note=['A5', 'C6', 'A5'][i], kind='sine', dur=0.05, glide=1.0), at=C['typing1'] + 0.09 * i, gain=-16, pan=-0.3)
m.sfx(sfx.zip_(True, 0.16), at=C['stream'], gain=-9, pan=-0.2)
# counter pops: one per 不能, climbing the F-major scale from F5; the 14th resolves on F7, the egg's 15th overshoots to G7
NOTES = [77, 79, 81, 82, 84, 86, 88, 89, 91, 93, 94, 96, 98, 101, 103]
for k, t in enumerate(C['ticks']):
    n = NOTES[k]
    m.sfx(sfx.pop('bubble', pitch=0.75 * 2 ** ((n - 77) / 24)), at=t, gain=-4 + 0.15 * k, pan=0.4)
    m.sfx(sfx.blip(note=n, kind='tri', dur=0.07, glide=0), at=t, gain=-11 + 0.2 * k, pan=0.4)
m.sfx(sfx.ding(note='F7', kind='bell', dur=0.8), at=C['max'] + 0.01, gain=-6, pan=0.4)
m.sfx(sfx.impact('punch', size=0.7, vel=0.9), at=C['max'], gain=-6)
# caption lines slap on one frame after their 不能 is counted
for i, t in enumerate(C['lines']):
    m.sfx(sfx.sticker_slap(seed=10 + i), at=t + FR, gain=-5, pan=[-0.3, 0.3][i % 2])
# brand name bleeped
m.sfx(sfx.blip(note='B5', kind='sine', dur=0.22, glide=0), at=C['beep'], gain=-7, pan=-0.15)
# ？？？: DJ scratch (the band keeps going) + three rising boings
m.sfx(sfx.record_scratch(kind='baby'), at=C['qmarks'][0] - 0.02, gain=-2)
for i, t in enumerate(C['qmarks']):
    m.sfx(sfx.boing(pitch=0.92 + 0.16 * i, dur=0.45), at=t - FR, gain=-6, pan=-0.35 + 0.35 * i)
# 时区守门员 stamp + audience 'ooh'
m.sfx(sfx.stamp('rubber'), at=C['stamp1'], gain=2)
m.sfx(sfx.impact('punch', size=0.9), at=C['stamp1'], gain=-4)
m.sfx(crowd(0.8, 'uo', [(0, .95), (.45, 1.16), (1, 1.0)], n=24, seed=19), at=C['stamp1'] + 0.05, gain=-7, verb=-9, send='hall')
# barrage clears
m.sfx(sfx.whoosh(0.35, 'swish', direction=-1), at=C['clear'] - 0.1, gain=-9)
m.sfx(sfx.pop('soft', pitch=1.3), at=C['clear'], gain=-10)

# --- the timid question, whisper music
m.sfx(sfx.swish(0.18, direction=1, seed=8), at=C['send2'] - 0.03, gain=-14, pan=0.35)
m.sfx(sfx.pop('bubble', pitch=1.0), at=C['send2'], gain=-12, pan=0.35)
m.sfx(sfx.pop('soft', pitch=1.5), at=C['aside'], gain=-10, pan=-0.3)
m.sfx(sfx.squeak(seed=2), at=C['aside'] + 0.2, gain=-14, pan=-0.3)
for i, t in enumerate(C['sweat']):
    m.sfx(sfx.drip(pitch=1.0 + 0.2 * i, seed=i), at=t, gain=-13, pan=0.2)
for i in range(3):
    m.sfx(sfx.blip(note=['A5', 'C6', 'A5'][i], kind='sine', dur=0.05, glide=1.0), at=C['typing2'] + 0.09 * i, gain=-17, pan=-0.3)
m.sfx(sfx.pop('bubble', pitch=0.9), at=C['answer'], gain=-9, pan=-0.3)

# --- 请前往 Settings → Usage 查看。  record scratch stops the band, 震惊!! hit, the audience laughs
m.sfx(sfx.record_scratch(kind='stop'), at=C['hero'], gain=1)
m.sfx(sfx.impact('punch', size=1.2), at=C['hero'], gain=0)
m.sfx(sfx.duang(1.0), at=C['hero'] + 0.02, gain=-3)
for i, t in enumerate(C['shock']):
    m.sfx(sfx.pop('cork', pitch=0.9 + 0.12 * i), at=t - FR, gain=-6, pan=-0.2 + 0.15 * i)
m.sfx(crowd(1.3, 'a', [(0, 1.05), (.6, 1.0), (1, .9)], seed=7, laugh=True), at=C['laugh'], gain=-1, verb=-9, send='hall')
m.sfx(crowd(1.15, 'e', [(0, 1.1), (1, .95)], n=22, seed=31, laugh=True), at=C['laugh'] + 0.12, gain=-5, verb=-10, send='hall')

# --- freeze card, 防御性满分 stamp, the reviewer's note (+1 = 15), ba-dum-tss + ta-da (recipe outro) on 没结论
m.sfx(sfx.shutter('phone'), at=C['freeze'], gain=0)
m.sfx(sfx.swish(0.3), at=C['freeze'] + 0.08, gain=-7)
m.sfx(sfx.stamp('rubber'), at=C['stamp2'], gain=2)
m.sfx(sfx.impact('punch', size=0.6, vel=0.9), at=C['stamp2'], gain=-4)
m.sfx(crowd(0.7, 'ua', [(0, .92), (.3, 1.16), (1, .9)], n=24, seed=3), at=C['stamp2'] + 0.05, gain=-8, verb=-9, send='hall')
m.sfx(sfx.ui('notify'), at=E, gain=-8, pan=-0.2)
m.sfx(sfx.pop('bubble', pitch=1.0), at=E + FR, gain=-9, pan=-0.2)
m.sfx(sfx.typing(n_keys=14, rate=17, kind='keyboard', seed=5), at=C['egg_text'][0], gain=-15, pan=-0.2)
t15 = C['tick15']   # the nitpick gets counted: the counter climbs one step past its 'max'
m.sfx(sfx.pop('bubble', pitch=0.75 * 2 ** ((NOTES[14] - 77) / 24)), at=t15, gain=-2, pan=0.4)
m.sfx(sfx.blip(note=NOTES[14], kind='tri', dur=0.07, glide=0), at=t15, gain=-8, pan=0.4)
m.sfx(sfx.ui('error'), at=t15 + 0.03, gain=-7, pan=0.4)
m.sfx(crowd(0.8, 'uo', [(0, .95), (.45, 1.18), (1, 1.02)], n=24, seed=29), at=t15 + 0.06, gain=-7, verb=-9, send='hall')
m.sfx(sfx.pop('mouth', pitch=1.2), at=C['sub1'] - FR, gain=-9)
m.sfx(sfx.rimshot_joke(), at=C['sub2'] - 0.36, gain=-3)   # snare + crash land on 没结论
for i in range(3):
    m.sfx(sfx.pop('bubble', pitch=1.1 + 0.12 * i), at=C['sub2'] + i * FR, gain=-9, pan=-0.2 + 0.2 * i)
m.sfx(crowd(0.6, 'a', [(0, 1.0), (1, .92)], n=18, seed=41, laugh=True), at=C['sub2'] + 0.08, gain=-12, verb=-10, send='hall')

# mix colour (from 18-hanazi): less 250-500 Hz mud on pizz/tuba/brass, bed high-passed at 110 Hz, presence on claps + SFX
for k, bands in {'pizz': [('hp', 110), ('pk', 350, -2.5, .8)], 'tuba': [('pk', 320, -3.0, .9)], 'brass': [('hp', 110), ('pk', 400, -2.0, .8)],
                 'stab': [('hp', 110), ('pk', 400, -2.0, .8)], 'xylo': [('hp', 110)], 'glock': [('hp', 110)], 'block': [('hp', 110)],
                 'clap': [('hs', 3500, 3.0)], 'clap2': [('hs', 3500, 3.0)], 'sfx': [('pk', 380, -1.5, .8), ('hs', 3500, 3.0)]}.items():
    if k in m.tracks:
        m.tracks[k].insert(lambda x, b=bands: _eq(x, b))
m.master_kw = {**getattr(m, 'master_kw', {}), 'glue_gr': 2.5}
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
res = m.export(os.path.join(HERE, 'out/audio.wav'), tp=-1.6, spectrogram=os.path.join(HERE, 'out/audio_spec.png'))
print({k: res[k] for k in ('duration', 'lufs', 'true_peak', 'stereo_corr', 'longest_gap') if k in res})
print('bands', res.get('bands')); print('warnings', res.get('warnings'))
