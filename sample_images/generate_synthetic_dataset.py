import os
import random
from PIL import Image, ImageDraw, ImageFont

# Dossier de sortie
output_dir = "dataset/images"
label_file = "dataset/labels.txt"
os.makedirs(output_dir, exist_ok=True)

# Chemin vers la police (modifie si besoin)
# Assure-toi que cette police supporte l’arabe
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font = ImageFont.truetype(font_path, 28)

# Fonction pour générer un texte de plaque tunisienne
def generate_plate_text():
    return f"{random.randint(100,999)} تونس {random.randint(1000,9999)}"

# Fonction pour générer l'image à partir du texte
def generate_image(text, filename):
    img = Image.new("L", (128, 32), color=255)  # Image en niveaux de gris
    draw = ImageDraw.Draw(img)

    # Affichage RTL (droite → gauche), nécessite PIL ≥ 7.0 pour arabic shaping correct
    try:
        draw.text((5, 2), text, font=font, fill=0, direction='rtl')
    except:
        draw.text((5, 2), text[::-1], font=font, fill=0)  # fallback RTL inversé

    img.save(filename)

# Génération
num_samples = 1000

with open(label_file, "w", encoding='utf-8') as f:
    for i in range(num_samples):
        text = generate_plate_text()
        filename = f"plate_{i:04d}.jpg"
        path = os.path.join(output_dir, filename)
        generate_image(text, path)
        f.write(f"{path}  {text}\n")
