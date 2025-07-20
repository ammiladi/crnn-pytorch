import os
import random
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops

# === CONFIGURATION === #
output_dir = "dataset/images"
label_file = "dataset/labels.txt"
background_dir = "backgrounds/"
num_samples = 1000

# Police à adapter à ton système
font_path = "./assets/Vazir.ttf"
font = ImageFont.truetype(font_path, 28)

# Créer les dossiers si nécessaire
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.dirname(label_file), exist_ok=True)

# Charger les fonds
backgrounds = glob.glob(os.path.join(background_dir, "*.jpg")) + \
              glob.glob(os.path.join(background_dir, "*.png"))

# Générer un texte de plaque
def generate_plate_text():
    return f"{random.randint(100,999)} تونس {random.randint(1000,9999)}"

# Ajouter taches (salissures)
def add_dirt(image):
    draw = ImageDraw.Draw(image)
    for _ in range(random.randint(3, 10)):
        x, y = random.randint(0, image.width), random.randint(0, image.height)
        r = random.randint(5, 15)
        opacity = random.randint(100, 200)
        dirt = Image.new('L', (r * 2, r * 2), 0)
        dirt_draw = ImageDraw.Draw(dirt)
        dirt_draw.ellipse((0, 0, r * 2, r * 2), fill=opacity)
        image.paste(dirt, (x - r, y - r), dirt)
    return image

# Ajouter ombre latérale douce
def add_shadow(image):
    shadow = Image.new('L', image.size, 255)
    draw = ImageDraw.Draw(shadow)
    x1 = random.randint(0, image.width // 2)
    x2 = random.randint(image.width // 2, image.width)
    draw.rectangle([x1, 0, x2, image.height], fill=random.randint(200, 240))
    return ImageChops.multiply(image, shadow)

# Centrage et padding vers taille cible
def pad_and_resize(image, target_size=(160, 40)):
    w, h = image.size
    new_im = Image.new("L", target_size, color=255)
    offset = ((target_size[0] - w) // 2, (target_size[1] - h) // 2)
    new_im.paste(image, offset)
    return new_im

# Génération d’une seule image
def generate_image(text, filename):
    # Taille aléatoire de base
    w = random.randint(120, 150)
    h = random.randint(30, 36)
    img = Image.new("L", (w, h), color=255)
    draw = ImageDraw.Draw(img)
    try:
        draw.text((5, 2), text, font=font, fill=0, direction='rtl')
    except:
        draw.text((5, 2), text[::-1], font=font, fill=0)

    # Rotation
    img = img.rotate(random.uniform(-5, 5), expand=True, fillcolor=255)

    # Fond réaliste
    if backgrounds:
        bg = Image.open(random.choice(backgrounds)).convert("L").resize((160, 40))
    else:
        bg = Image.new("L", (160, 40), color=random.randint(180, 255))

    # Combinaison plaque + fond
    plate = ImageOps.invert(img)
    plate = pad_and_resize(plate, bg.size)
    combined = ImageChops.multiply(bg, plate)
    combined = ImageOps.invert(combined)

    # Bruit (flou)
    if random.random() < 0.5:
        combined = combined.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.2, 1.0)))

    # Ombres douces
    if random.random() < 0.5:
        combined = add_shadow(combined)

    # Taches noires (salissures)
    if random.random() < 0.4:
        combined = add_dirt(combined)

    # Inversion (plaque noire, texte clair / simulation IR)
    if random.random() < 0.3:
        combined = ImageOps.invert(combined)

    combined.save(filename)

# Génération du dataset
with open(label_file, "w", encoding='utf-8') as f:
    for i in range(num_samples):
        text = generate_plate_text()
        filename = f"plate_{i:04d}.jpg"
        path = os.path.join(output_dir, filename)
        generate_image(text, path)
        f.write(f"{path}  {text}\n")

print(f"✅ Génération terminée : {num_samples} images dans '{output_dir}'")
