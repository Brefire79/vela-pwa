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
    tw, th = draw.textsize(text, font=font)
    draw.text(((size - tw) / 2, (size - th) / 2), text, fill="#ffffff", font=font)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
