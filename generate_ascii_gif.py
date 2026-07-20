"""
Génère un GIF animé qui révèle un ASCII art ligne par ligne (haut -> bas).
Usage: python3 generate_ascii_gif.py
"""

from PIL import Image, ImageDraw, ImageFont

INPUT_FILE = "ascii-art.txt"
OUTPUT_FILE = "ascii_reveal.gif"

FONT_SIZE = 6
CHAR_WIDTH = 4      # largeur approx d'un caractère monospace à cette taille
LINE_HEIGHT = 7
PADDING = 10
BG_COLOR = (13, 13, 13)       # fond sombre (proche du fond GitHub dark mode)
FG_COLOR = (255, 255, 255)    # blanc
LINES_PER_FRAME = 2           # combien de nouvelles lignes révélées par frame
FRAME_DURATION_MS = 60        # vitesse de l'animation
HOLD_LAST_FRAME_MS = 1500     # pause sur l'image complète à la fin

# Essaie de charger une police monospace, sinon fallback
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
except IOError:
    font = ImageFont.load_default()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = [line.rstrip("\n") for line in f.readlines()]

max_len = max(len(l) for l in lines)
img_width = PADDING * 2 + max_len * CHAR_WIDTH
img_height = PADDING * 2 + len(lines) * LINE_HEIGHT

frames = []

def render_frame(num_visible_lines):
    img = Image.new("RGB", (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    for i in range(num_visible_lines):
        y = PADDING + i * LINE_HEIGHT
        draw.text((PADDING, y), lines[i], font=font, fill=FG_COLOR)
    return img

# Génère une frame toutes les LINES_PER_FRAME lignes
for i in range(0, len(lines) + 1, LINES_PER_FRAME):
    frames.append(render_frame(min(i, len(lines))))

# Frame finale (image complète), tenue plus longtemps
frames.append(render_frame(len(lines)))

durations = [FRAME_DURATION_MS] * (len(frames) - 1) + [HOLD_LAST_FRAME_MS]

frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
)

print(f"GIF généré : {OUTPUT_FILE} ({len(frames)} frames, {img_width}x{img_height}px)")
