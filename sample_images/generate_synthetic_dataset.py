import os
import random
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# 📁 Dossiers
output_dir = "dataset/images"
label_file = "dataset/labels.txt"
background_dir = "backgrounds/"  # Dossier contenant des fonds réalistes (images jpg/png)

# Crée les dossiers
os.makedirs(output_dir, exist_ok=True)

# 📌 Police : change si tu veux une autre
font_path = "/usr/share/fonts/Amiri-Regular.ttf.ttf"
font = ImageFont.truetype(font_path, 28)

# 📸 Charger les fonds
backgrounds = glob.glob(os.path.join(background_dir, "*.jpg")) + \
              glob.glob(os.path.join(background_dir, "*.png"))

# 🔡 Générer un texte de plaque (ex: 123 تونس 4567)
def generate_plate_text():
    return f"{random.randint(100,999)} تونس {random.randint(1000,9999)}"

# 🖼 Générer une image avec texte, fond et bruit
def generate_image(text, filename):
    # Créer une image transparente
    plate_img = Image.new("L", (128, 32), color=255)
    draw = ImageDraw.Draw(plate_img)
    try:
        draw.text((5, 2), text, font=font, fill=0, direction='rtl')
    except:
        draw.text((5, 2), text[::-1], font=font, fill=0)

    # Ajouter rotation aléatoire
    angle = random.uniform(-5, 5)
    plate_img = plate_img.rotate(angle, expand=1, fillcolor=255)

    # Ajouter fond
    if backgrounds:
        bg_path = random.choice(backgrounds)
        bg = Image.open(bg_path).convert("L").resize((128, 32))
    else:
        bg = Image.new("L", (128, 32), color=random.randint(180, 255))

    # Combiner la plaque (noir sur blanc) sur le fond
    plate_img = ImageOps.invert(plate_img)
    combined = ImageChops.multiply(bg, plate_img)
    combined = ImageOps.invert(combined)

    # Ajouter du bruit (filtre de contour + léger flou)
    if random.random() < 0.5:
        combined = combined.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 1.0)))

    combined.save(filename)

# 🔁 Génération
num_samples = 1000
with open(label_file, "w", encoding='utf-8') as f:
    for i in range(num_samples):
        text = generate_plate_text()
        filename = f"plate_{i:04d}.jpg"
        path = os.path.join(output_dir, filename)
        generate_image(text, path)
        f.write(f"{path}  {text}\n")
