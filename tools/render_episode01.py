#!/usr/bin/env python3
"""Render Episode 1: 'One water bottle, one supply chain'.

Pure Python (Pillow + numpy) frame renderer, piped to ffmpeg.
Output: renders/episode-01-water-bottle.mp4 (1080x1920, 30 fps, H.264, silent).

Usage:
    python3 tools/render_episode01.py            # full render
    python3 tools/render_episode01.py --stills   # write check frames to renders/stills/
"""
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
DURATION = 55.0
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "renders" / "episode-01-water-bottle.mp4"

# Palette
BG = (15, 23, 42)
FG = (241, 245, 249)
MUTED = (148, 163, 184)
ACCENT = (56, 189, 248)
PELLET = (226, 232, 240)
HEAT = (251, 146, 60)
WATER = (59, 130, 246)
BOX = (30, 41, 59)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_TITLE = ImageFont.truetype(FONT_BOLD, 68)
F_SUB = ImageFont.truetype(FONT_REG, 40)
F_LABEL = ImageFont.truetype(FONT_BOLD, 38)
F_SMALL = ImageFont.truetype(FONT_BOLD, 30)

# Shorts UI covers roughly the bottom 380 px and the right 140 px.
SAFE_LEFT, SAFE_RIGHT = 70, W - 160
TEXT_TOP = 230

# Scene boundaries in seconds
S_HOOK, S_SETUP, S_PRE, S_BLOW, S_TURN, S_LINE, S_TRUCK, S_LOOP = 0, 4, 10, 18, 28, 36, 46, 52

CX = 470            # horizontal center of the main stage (left of the right-side UI)
NECK_Y = 900        # top of the bottle neck
PILE_Y = 1380       # floor of the pellet pile


# ---------- helpers ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_col(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def fade(t, start, end, edge=0.4):
    """Opacity 0..1 for an element visible between start and end."""
    if t < start or t > end:
        return 0.0
    return clamp(min((t - start) / edge, (end - t) / edge))


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(img, lines_spec, top, alpha):
    """lines_spec: list of (text, font, color). Drawn centered in the safe area."""
    if alpha <= 0:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = top
    mid = (SAFE_LEFT + SAFE_RIGHT) / 2
    for text, font, color in lines_spec:
        for line in wrap(d, text, font, SAFE_RIGHT - SAFE_LEFT):
            w = d.textlength(line, font=font)
            d.text((mid - w / 2, y), line, font=font, fill=color + (int(255 * alpha),))
            y += font.size + 18
        y += 14
    img.alpha_composite(layer)


# ---------- bottle geometry ----------
N = 60


def preform_profile():
    """Half-widths from neck (index 0) to base, plus total length."""
    pts = []
    for i in range(N):
        u = i / (N - 1)
        if u < 0.12:
            hw = 30            # neck finish
        elif u < 0.16:
            hw = 36            # support ring
        else:
            hw = 26
        if u > 0.93:           # rounded bottom
            hw *= math.sqrt(max(0.0, 1 - ((u - 0.93) / 0.07) ** 2))
        pts.append(hw)
    return pts, 230


def bottle_profile():
    pts = []
    for i in range(N):
        u = i / (N - 1)
        if u < 0.12 * 230 / 560:
            hw = 30            # same neck finish as the preform
        elif u < 0.16 * 230 / 560:
            hw = 36
        elif u < 0.30:
            s = (u - 0.066) / (0.30 - 0.066)
            hw = lerp(32, 105, ease(s))
        else:
            hw = 105
            if 0.55 < u < 0.60 or 0.75 < u < 0.80:
                hw = 98        # grip ribs
        if u > 0.96:
            hw *= math.sqrt(max(0.0, 1 - ((u - 0.96) / 0.04) ** 2))
        pts.append(hw)
    return pts, 560


PRE, PRE_LEN = preform_profile()
BOT, BOT_LEN = bottle_profile()


def bottle_polygon(t_blow, cx=CX, top=NECK_Y, scale=1.0):
    hws = [lerp(a, b, t_blow) * scale for a, b in zip(PRE, BOT)]
    length = lerp(PRE_LEN, BOT_LEN, t_blow) * scale
    left, right = [], []
    for i, hw in enumerate(hws):
        y = top + length * i / (N - 1)
        left.append((cx - hw, y))
        right.append((cx + hw, y))
    return left + right[::-1], length


def draw_bottle(img, t_blow, fill_col, outline_col, alpha=1.0, cx=CX, top=NECK_Y,
                scale=1.0, water=0.0, cap=False, label=False):
    if alpha <= 0:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    poly, length = bottle_polygon(t_blow, cx, top, scale)
    a = int(255 * alpha)
    d.polygon(poly, fill=fill_col + (int(a * 0.35),), outline=outline_col + (a,), width=4)
    if water > 0:
        # water fills from the bottom up, clipped to the bottle shape
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).polygon(poly, fill=255)
        wl = Image.new("RGBA", img.size, (0, 0, 0, 0))
        wy = top + length * (1 - 0.82 * water)
        ImageDraw.Draw(wl).rectangle([0, wy, W, top + length], fill=WATER + (int(a * 0.8),))
        layer.paste(wl, (0, 0), Image.composite(wl.getchannel("A"), Image.new("L", img.size, 0), mask))
    if cap:
        d.rounded_rectangle([cx - 34 * scale, top - 30 * scale, cx + 34 * scale, top + 6 * scale],
                            radius=int(6 * scale), fill=ACCENT + (a,))
    if label:
        ly = top + length * 0.42
        d.rectangle([cx - 104 * scale, ly, cx + 104 * scale, ly + length * 0.22],
                    fill=(241, 245, 249, int(a * 0.9)))
    img.alpha_composite(layer)


# ---------- pellets ----------
rng = random.Random(7)
PELLETS = []
for i in range(140):
    px = CX + rng.gauss(0, 95)
    delay = rng.uniform(0, 3.2)
    PELLETS.append({
        "x": px,
        "delay": delay,
        "rest": PILE_Y - 18 - (140 - abs(px - CX)) * rng.uniform(0.0, 0.9),
        "r": rng.uniform(9, 13),
    })


def draw_pellets(img, t_local, alpha=1.0, melt=0.0):
    if alpha <= 0:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for p in PELLETS:
        tt = t_local - p["delay"]
        if tt < 0:
            continue
        y = min(560 + 0.5 * 2600 * tt * tt, p["rest"])  # spawn below the title block
        x = p["x"]
        if melt > 0:  # pellets converge into the preform position
            x = lerp(x, CX, ease(melt))
            y = lerp(y, NECK_Y + 120, ease(melt))
        r = p["r"] * (1 - 0.6 * melt)
        col = lerp_col(PELLET, HEAT, melt)
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=col + (int(255 * alpha),))
    img.alpha_composite(layer)


# ---------- scenes ----------
def box(d, x0, y0, x1, y1, text, alpha, color=BOX):
    a = int(255 * alpha)
    d.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=color + (a,), outline=ACCENT + (a,), width=3)
    lines = text.split("\n")
    ty = (y0 + y1) / 2 - len(lines) * (F_LABEL.size + 6) / 2
    for line in lines:
        w = d.textlength(line, font=F_LABEL)
        d.text(((x0 + x1) / 2 - w / 2, ty), line, font=F_LABEL, fill=FG + (a,))
        ty += F_LABEL.size + 6


def scene_turn(img, t):
    local = t - S_TURN
    a = fade(t, S_TURN, S_LINE)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    box(d, 90, 900, 430, 1080, "Bottle\nmaker", a)
    box(d, 560, 1330, 880, 1500, "Water\nplant", a)
    # pallet of empty bottles travels between the boxes
    prog = ease((local - 1.2) / 4.0)
    px, py = lerp(260, 640, prog), lerp(1100, 1180, prog)
    pa = int(255 * a)
    d.rectangle([px - 95, py + 70, px + 95, py + 86], fill=(180, 130, 80, pa))
    for row in range(2):
        for col in range(4):
            bx = px - 70 + col * 46
            by = py + 10 - row * 64
            d.rounded_rectangle([bx - 16, by - 50, bx + 16, by + 58], radius=10,
                                fill=ACCENT + (int(pa * 0.35),), outline=ACCENT + (pa,), width=3)
    img.alpha_composite(layer)
    text_block(img, [("Twist: many water plants don't make their bottles.", F_TITLE, FG),
                     ("They arrive empty, on pallets.", F_SUB, ACCENT)], TEXT_TOP, a)


STATIONS = ["rinse", "fill", "cap", "label", "pack"]


def scene_line(img, t):
    local = t - S_LINE
    a = fade(t, S_LINE, S_TRUCK)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pa = int(255 * a)
    # conveyor
    d.rectangle([60, 1370, SAFE_RIGHT + 40, 1386], fill=MUTED + (pa,))
    xs = [140 + i * 175 for i in range(5)]
    for i, (x, name) in enumerate(zip(xs, STATIONS)):
        w = d.textlength(name, font=F_SMALL)
        active = local > 1.2 + i * 1.6
        d.rounded_rectangle([x - 72, 1410, x + 72, 1470], radius=14,
                            fill=(ACCENT if active else BOX) + (pa,))
        d.text((x - w / 2, 1422), name, font=F_SMALL, fill=(BG if active else FG) + (pa,))
    img.alpha_composite(layer)
    # bottle travels station to station
    seg = clamp((local - 0.6) / 8.0) * 4
    i0 = int(min(seg, 3.999))
    bx = lerp(xs[i0], xs[i0 + 1], ease(seg - i0)) if seg < 4 else xs[4]
    water = clamp((local - 2.8) / 1.2)
    draw_bottle(img, 1.0, ACCENT, ACCENT, a, cx=bx, top=1370 - 560 * 0.55, scale=0.55,
                water=water, cap=local > 4.4, label=local > 6.0)
    text_block(img, [("Then: rinse → fill → cap → label → pack", F_TITLE, FG)], TEXT_TOP, a)


def scene_truck(img, t):
    local = t - S_TRUCK
    a = fade(t, S_TRUCK, S_LOOP)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pa = int(255 * a)
    d.line([60, 1380, SAFE_RIGHT + 40, 1380], fill=MUTED + (pa,), width=6)
    # store shelf on the right
    for k in range(3):
        y = 1000 + k * 120
        d.rectangle([660, y, 900, y + 12], fill=MUTED + (pa,))
    d.rectangle([652, 880, 664, 1252], fill=MUTED + (pa,))
    d.rectangle([896, 880, 908, 1252], fill=MUTED + (pa,))
    stocked = local > 3.6
    if stocked:
        for k in range(5):
            bx = 685 + k * 46
            d.rounded_rectangle([bx - 15, 945, bx + 15, 1000], radius=8,
                                fill=WATER + (int(pa * 0.8),), outline=ACCENT + (pa,), width=2)
    # truck
    tx = lerp(-260, 380, ease(local / 3.4))
    d.rounded_rectangle([tx, 1180, tx + 230, 1340], radius=12, fill=ACCENT + (pa,))
    d.rounded_rectangle([tx + 230, 1240, tx + 320, 1340], radius=12, fill=(14, 165, 233, pa))
    for wx in (tx + 60, tx + 260):
        d.ellipse([wx - 32, 1320, wx + 32, 1384], fill=FG + (pa,), outline=BG + (pa,), width=8)
    img.alpha_composite(layer)
    text_block(img, [("Then a truck to a store shelf.", F_TITLE, FG)], TEXT_TOP, a)


def render_frame(t):
    img = Image.new("RGBA", (W, H), BG + (255,))

    # HOOK + SETUP + LOOP: pellets falling and piling
    if t < S_PRE + 1.5:
        melt = clamp((t - S_PRE) / 1.5)
        draw_pellets(img, t, 1.0, melt)
    if t >= S_LOOP:
        draw_pellets(img, t - S_LOOP, fade(t, S_LOOP, DURATION + 1, 0.6))

    text_block(img, [("This bottle didn't start as a bottle.", F_TITLE, FG)], TEXT_TOP,
               fade(t, S_HOOK - 1, S_SETUP))
    text_block(img, [("It started as tiny plastic pellets.", F_TITLE, FG),
                     ("PET resin, made from ethylene glycol + terephthalic acid", F_SUB, ACCENT)],
               TEXT_TOP, fade(t, S_SETUP, S_PRE))

    # STEP 1: preform appears
    a_pre = fade(t, S_PRE + 0.8, S_BLOW + 0.2)
    if a_pre > 0:
        draw_bottle(img, 0.0, PELLET, FG, a_pre)
    text_block(img, [("Step 1: molded into a \"preform\"", F_TITLE, FG),
                     ("A small tube with the finished neck already on it", F_SUB, ACCENT)],
               TEXT_TOP, fade(t, S_PRE, S_BLOW))

    # STEP 2: heat, then blow
    if S_BLOW <= t < S_TURN:
        local = t - S_BLOW
        heat = ease(local / 2.5) * (1 - ease((local - 6.5) / 2.0))
        blow = ease((local - 3.0) / 3.5)
        col = lerp_col(ACCENT, HEAT, heat)
        draw_bottle(img, blow, col, lerp_col(FG, HEAT, heat), fade(t, S_BLOW, S_TURN))
    text_block(img, [("Step 2: heated, then blown into shape with air", F_TITLE, FG),
                     ("Above ~100 °C", F_SUB, HEAT)], TEXT_TOP, fade(t, S_BLOW, S_TURN))

    if S_TURN <= t < S_LINE:
        scene_turn(img, t)
    if S_LINE <= t < S_TRUCK:
        scene_line(img, t)
    if S_TRUCK <= t < S_LOOP:
        scene_truck(img, t)

    text_block(img, [("So where did yours start?", F_TITLE, FG)], TEXT_TOP,
               fade(t, S_LOOP, DURATION + 1, 0.6))
    return img.convert("RGB")


def main():
    if "--stills" in sys.argv:
        out = ROOT / "renders" / "stills"
        out.mkdir(parents=True, exist_ok=True)
        for s in [1, 3.5, 7, 14, 20, 23, 26, 32, 39, 44, 49, 53.5]:
            render_frame(s).save(out / f"t{s:05.1f}.png")
        print("stills written to", out)
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(OUT)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = int(DURATION * FPS)
    for f in range(total):
        proc.stdin.write(render_frame(f / FPS).tobytes())
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        sys.exit("ffmpeg failed")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
