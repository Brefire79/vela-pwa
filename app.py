from flask import Flask, render_template, send_from_directory, send_file
from io import BytesIO
try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:
    Image = None
    ImageDraw = None
    ImageFont = None

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(".", "service-worker.js")


def _generate_icon(size: int):
    """Gera um ícone PNG em memória. Requer Pillow."""
    if Image is None:
        return None
    img = Image.new("RGBA", (size, size), "#0d9488")  # fundo teal
    draw = ImageDraw.Draw(img)
    # Desenha um "V" simples centralizado
    text = "V"
    # Usa fonte padrão; se disponível, tenta uma fonte maior
    font = None
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.6))
    except Exception:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", int(size * 0.6))
        except Exception:
            font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((size - tw) / 2, (size - th) / 2), text, fill="#ffffff", font=font)
    return img


def _generate_maskable(size: int):
    """Gera um ícone 'maskable' com margens (safe zone)."""
    if Image is None:
        return None
    img = Image.new("RGBA", (size, size), "#0d9488")
    draw = ImageDraw.Draw(img)
    text = "V"
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.5))
    except Exception:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", int(size * 0.5))
        except Exception:
            font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    margin = int(size * 0.12)
    cx = size // 2
    cy = size // 2
    draw.text((cx - tw // 2, cy - th // 2), text, fill="#ffffff", font=font)
    # opcional: círculo interno indicando zona segura
    # draw.ellipse((margin, margin, size - margin, size - margin), outline="#ffffff")
    return img


@app.route("/icons/<int:size>.png")
def icon(size: int):
    # Gera o ícone dinamicamente; se Pillow indisponível, retorna 404
    img = _generate_icon(size)
    if img is None:
        return ("Pillow não instalado", 404)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/icons/maskable/<int:size>.png")
def icon_maskable(size: int):
    img = _generate_maskable(size)
    if img is None:
        return ("Pillow não instalado", 404)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/favicon.ico")
def favicon():
    base = _generate_icon(64)
    if base is None:
        return ("Pillow não instalado", 404)
    buf = BytesIO()
    base.save(buf, format="ICO")
    buf.seek(0)
    return send_file(buf, mimetype="image/x-icon")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
