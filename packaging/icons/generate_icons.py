"""
Gerador de Ícones Nativos para o MarkItDown Studio IDE.
Gera ícones multi-resolução para Windows (.ico), macOS e documentação (.png).
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

ICONS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(ICONS_DIR))


def create_app_icon(size: int = 512) -> Image.Image:
    """Cria imagem de ícone em alta definição para o MarkItDown Studio."""
    # Cria imagem RGBA com fundo transparente
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Coordenadas do quadrado arredondado (estilo macOS / Windows Fluent)
    padding = size * 0.08
    corner_radius = size * 0.22
    box = [padding, padding, size - padding, size - padding]

    # Gradiente em tons de azul índigo e ciano tecnológico
    # Simulado por camadas suaves
    steps = 100
    for i in range(steps):
        factor = i / float(steps)
        r = int(30 + factor * (59 - 30))
        g = int(41 + factor * (130 - 41))
        b = int(59 + factor * (246 - 59))
        inset = padding + (1 - factor) * 2
        # Fundo arredondado
        draw.rounded_rectangle(
            [inset, inset, size - inset, size - inset],
            radius=corner_radius,
            fill=(r, g, b, 255)
        )

    # Brilho sutil no topo (efeito glass/fluent)
    gloss_height = size * 0.35
    gloss_box = [padding + 4, padding + 4, size - padding - 4, padding + gloss_height]
    draw.rounded_rectangle(gloss_box, radius=corner_radius * 0.8, fill=(255, 255, 255, 25))

    # Desenho do Símbolo do Markdown / Documento
    # Dimensões da folha de documento no centro
    doc_w = size * 0.52
    doc_h = size * 0.60
    doc_left = (size - doc_w) / 2
    doc_top = (size - doc_h) / 2 + size * 0.02
    doc_right = doc_left + doc_w
    doc_bottom = doc_top + doc_h
    fold_size = size * 0.14

    # Fundo do documento (branco suave)
    doc_points = [
        (doc_left, doc_top),
        (doc_right - fold_size, doc_top),
        (doc_right, doc_top + fold_size),
        (doc_right, doc_bottom),
        (doc_left, doc_bottom),
    ]
    draw.polygon(doc_points, fill=(248, 250, 252, 255))

    # Orelha dobrada da folha (fold)
    fold_points = [
        (doc_right - fold_size, doc_top),
        (doc_right - fold_size, doc_top + fold_size),
        (doc_right, doc_top + fold_size),
    ]
    draw.polygon(fold_points, fill=(203, 213, 225, 255))
    draw.line([(doc_right - fold_size, doc_top), (doc_right - fold_size, doc_top + fold_size), (doc_right, doc_top + fold_size)], fill=(148, 163, 184, 255), width=int(size * 0.008))

    # Símbolo do Markdown 'M' estilizado
    m_color = (37, 99, 235, 255)  # Azul vibrante
    m_left = doc_left + size * 0.09
    m_top = doc_top + size * 0.18
    m_w = size * 0.22
    m_h = size * 0.16
    line_w = max(4, int(size * 0.032))

    # Desenho do 'M'
    draw.line([(m_left, m_top + m_h), (m_left, m_top), (m_left + m_w / 2, m_top + m_h * 0.7), (m_left + m_w, m_top), (m_left + m_w, m_top + m_h)], fill=m_color, width=line_w, joint="curve")

    # Seta para baixo do Markdown
    arrow_x = m_left + m_w + size * 0.07
    arrow_top = m_top
    arrow_bottom = m_top + m_h
    draw.line([(arrow_x, arrow_top), (arrow_x, arrow_bottom)], fill=m_color, width=line_w)
    head_size = size * 0.045
    draw.line([(arrow_x - head_size, arrow_bottom - head_size), (arrow_x, arrow_bottom), (arrow_x + head_size, arrow_bottom - head_size)], fill=m_color, width=line_w, joint="curve")

    # Linhas de texto representativas no documento
    line_color = (148, 163, 184, 220)
    for row_y in [doc_top + size * 0.40, doc_top + size * 0.46, doc_top + size * 0.52]:
        draw.rounded_rectangle([doc_left + size * 0.08, row_y, doc_right - size * 0.08, row_y + size * 0.018], radius=3, fill=line_color)

    return img


def generate_all_icons():
    """Gera app.png, app.ico e sincroniza ui/favicon.ico."""
    os.makedirs(ICONS_DIR, exist_ok=True)

    # 1. Gera app.png em alta resolução (512x512)
    img_512 = create_app_icon(size=512)
    png_path = os.path.join(ICONS_DIR, "app.png")
    img_512.save(png_path, format="PNG")
    print(f"[ICONS] Ícone PNG gerado: {png_path}")

    # 2. Gera app.ico multi-resolução para Windows
    ico_path = os.path.join(ICONS_DIR, "app.ico")
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img_512.save(
        ico_path,
        format="ICO",
        sizes=icon_sizes
    )
    print(f"[ICONS] Ícone Windows ICO gerado: {ico_path} com {len(icon_sizes)} resoluções")

    # 3. Atualiza ui/favicon.ico para consistência de branding
    ui_favicon = os.path.join(PROJECT_ROOT, "ui", "favicon.ico")
    img_512.save(ui_favicon, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"[ICONS] Favicon web atualizado: {ui_favicon}")


if __name__ == "__main__":
    generate_all_icons()
