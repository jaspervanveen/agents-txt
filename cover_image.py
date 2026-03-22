from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# dev.to cover image: 1000x420
W, H = 1000, 420

# Colors - phosphor green on near-black
BG       = (10, 12, 10)
GREEN    = (57, 255, 90)
GREEN_DIM = (30, 140, 50)
GLOW     = (20, 80, 30)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Fonts ──────────────────────────────────────────────────────────────────
try:
    font_lg = ImageFont.truetype("/System/Library/Fonts/Courier.ttc", 19)
    font_sm = ImageFont.truetype("/System/Library/Fonts/Courier.ttc", 16)
    font_xs = ImageFont.truetype("/System/Library/Fonts/Courier.ttc", 13)
except:
    font_lg = font_sm = font_xs = ImageFont.load_default()

# ── CRT scanlines (subtle) ─────────────────────────────────────────────────
for y in range(0, H, 3):
    draw.line([(0, y), (W, y)], fill=(0, 0, 0), width=1)

# ── Screen bezel / vignette layer (drawn after content) ───────────────────
# We'll add this at the end

# ── Code content ──────────────────────────────────────────────────────────
lines = [
    ("# agents.txt — AI Agent Interface Declaration", "comment"),
    ("# Place at: https://yourdomain.com/agents.txt",  "comment"),
    ("",                                                "blank"),
    ("Site-Name: ExampleShop",                          "key"),
    ("Site-Description: Online store for home goods",   "key"),
    ("Allow-Training: no",                              "key"),
    ("Allow-RAG: yes",                                  "key"),
    ("MCP-Server: https://mcp.exampleshop.com",        "key"),
    ("",                                                "blank"),
    ("[Agent: *]",                                      "section"),
    ("Allow: /products/*",                              "key"),
    ("Disallow: /checkout",                             "key"),
    ("",                                                "blank"),
    ("[Agent: verified-purchasing-agent]",              "section"),
    ("Allow: /checkout",                                "key"),
    ("Auth-Method: oauth2",                             "key"),
    ("Allow-Actions: yes",                              "key"),
]

COLOR_MAP = {
    "comment": (40, 160, 60),
    "section":  (100, 255, 130),
    "key":      GREEN,
    "blank":    BG,
}

x0 = 48
y0 = 32
line_h = 22

for i, (text, kind) in enumerate(lines):
    y = y0 + i * line_h
    color = COLOR_MAP.get(kind, GREEN)
    draw.text((x0, y), text, font=font_lg, fill=color)

# ── Blinking cursor after last line ───────────────────────────────────────
cursor_y = y0 + len(lines) * line_h
draw.rectangle([x0, cursor_y, x0 + 11, cursor_y + 17], fill=GREEN)

# ── Watermark / label bottom-right ────────────────────────────────────────
label = "agents.txt  •  github.com/jaspervanveen/agents-txt"
draw.text((W - 10, H - 22), label, font=font_xs, fill=GREEN_DIM, anchor="ra")

# ── Glow pass: slightly blur a bright green overlay, then composite ────────
glow_layer = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow_layer)
for i, (text, kind) in enumerate(lines):
    y = y0 + i * line_h
    if kind != "blank":
        gd.text((x0, y), text, font=font_lg, fill=(80, 255, 100))
gd.rectangle([x0, cursor_y, x0 + 11, cursor_y + 17], fill=(80, 255, 100))

glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=3))

# Blend glow onto image
img_arr   = np.array(img).astype(np.float32)
glow_arr  = np.array(glow_layer).astype(np.float32)
result    = np.clip(img_arr + glow_arr * 0.7, 0, 255).astype(np.uint8)
img = Image.fromarray(result)

# ── CRT vignette ──────────────────────────────────────────────────────────
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for step in range(60):
    alpha = int(step * 3.2)
    vd.rectangle([step, step, W - step, H - step],
                 outline=(0, 0, 0, alpha), width=1)
img = img.convert("RGBA")
img = Image.alpha_composite(img, vignette).convert("RGB")

# ── Scanlines pass 2 (stronger, on top of glow) ───────────────────────────
sd = ImageDraw.Draw(img)
for y in range(0, H, 3):
    sd.line([(0, y), (W, y)], fill=(0, 0, 0), width=1)

out = "/Users/pandora/.openclaw/workspace/projects/agents-txt/cover.png"
img.save(out)
print(f"Saved: {out}  ({W}x{H})")
