from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H = 1000, 420

BG         = (8, 14, 8)
GREEN      = (72, 255, 100)
GREEN_DIM  = (35, 160, 55)
GREEN_SECT = (140, 255, 160)
COMMENT    = (35, 140, 50)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Font ──────────────────────────────────────────────────────────────────
try:
    font_main = ImageFont.truetype("/System/Library/Fonts/Courier.ttc", 46)
    font_sm   = ImageFont.truetype("/System/Library/Fonts/Courier.ttc", 17)
except:
    font_main = font_sm = ImageFont.load_default()

# ── Code lines ────────────────────────────────────────────────────────────
lines = [
    ("# yourdomain.com/agents.txt",  "comment"),
    ("",                              "blank"),
    ("Allow-Training:  no",          "key"),
    ("Allow-RAG:       yes",         "key"),
    ("MCP-Server:      mcp.example.com", "key"),
    ("",                              "blank"),
    ("[Agent: purchasing-agent]",    "section"),
    ("Allow-Actions:   yes",         "key"),
    ("Auth-Method:     oauth2",      "key"),
]

COLOR_MAP = {
    "comment": COMMENT,
    "section": GREEN_SECT,
    "key":     GREEN,
    "blank":   BG,
}

x0     = 44
y0     = 22
line_h = 44

for i, (text, kind) in enumerate(lines):
    y = y0 + i * line_h
    if kind == "blank":
        continue
    color = COLOR_MAP[kind]
    draw.text((x0, y), text, font=font_main, fill=color)

# blinking cursor
cursor_y = y0 + len(lines) * line_h
draw.rectangle([x0, cursor_y, x0 + 28, cursor_y + 38], fill=GREEN)

# bottom-right watermark
draw.text((W - 12, H - 22), "github.com/jaspervanveen/agents-txt",
          font=font_sm, fill=GREEN_DIM, anchor="ra")

# ── Glow pass ────────────────────────────────────────────────────────────
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd   = ImageDraw.Draw(glow)
for i, (text, kind) in enumerate(lines):
    y = y0 + i * line_h
    if kind != "blank":
        gd.text((x0, y), text, font=font_main, fill=(100, 255, 120))
gd.rectangle([x0, cursor_y, x0 + 28, cursor_y + 38], fill=(100, 255, 120))
glow = glow.filter(ImageFilter.GaussianBlur(radius=4))

arr      = np.array(img).astype(np.float32)
glow_arr = np.array(glow).astype(np.float32)
arr      = np.clip(arr + glow_arr * 0.65, 0, 255).astype(np.uint8)
img      = Image.fromarray(arr)

# ── Scanlines ────────────────────────────────────────────────────────────
sd = ImageDraw.Draw(img)
for y in range(0, H, 4):
    sd.line([(0, y), (W, y)], fill=(0, 0, 0), width=1)

# ── CRT tube: barrel-curve vignette ──────────────────────────────────────
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd  = ImageDraw.Draw(vig)
steps = 55
for s in range(steps):
    alpha = int((s / steps) ** 1.6 * 210)
    vd.rectangle([s, s, W - s, H - s], outline=(0, 0, 0, alpha), width=1)
img = img.convert("RGBA")
img = Image.alpha_composite(img, vig)

# ── CRT glass glare — radial numpy gradients ─────────────────────────────
xs = np.linspace(0, 1, W)
ys = np.linspace(0, 1, H)
xg, yg = np.meshgrid(xs, ys)

# Primary streak: wide shallow ellipse upper-centre-left
cx1, cy1, rx1, ry1 = 0.34, 0.09, 0.40, 0.20
d1 = np.sqrt(((xg - cx1) / rx1) ** 2 + ((yg - cy1) / ry1) ** 2)
g1 = np.clip(1 - d1, 0, 1) ** 2.5 * 0.28

# Secondary glint: small ellipse upper-right
cx2, cy2, rx2, ry2 = 0.83, 0.06, 0.12, 0.09
d2 = np.sqrt(((xg - cx2) / rx2) ** 2 + ((yg - cy2) / ry2) ** 2)
g2 = np.clip(1 - d2, 0, 1) ** 3.0 * 0.22

glare_alpha = np.clip(g1 + g2, 0, 1)

# Warm white-green tint
glare_r = (glare_alpha * 0.88 * 255).astype(np.uint8)
glare_g = (glare_alpha * 1.00 * 255).astype(np.uint8)
glare_b = (glare_alpha * 0.90 * 255).astype(np.uint8)
glare_a = (glare_alpha        * 255).astype(np.uint8)

glare_arr = np.dstack([glare_r, glare_g, glare_b, glare_a])
glare_img = Image.fromarray(glare_arr, "RGBA")

img = Image.alpha_composite(img, glare_img)
img = img.convert("RGB")

out = "/Users/pandora/.openclaw/workspace/projects/agents-txt/cover.png"
img.save(out, quality=95)
print(f"Saved: {out}  ({W}x{H})")
