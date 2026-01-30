def convert_and_save_icon(raw_data: bytes, filepath: str, name: str):
    # Pyscript miatt: importok MUSZÁJ a függvényen belül legyenek
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import os

    TARGET_SIZE = (64, 64)
    JPG_QUALITY = 82

    def make_placeholder(text: str, out_path: str):
        """64×64 generált szöveges ikon"""
        img = Image.new("RGB", TARGET_SIZE, (40, 40, 40))
        draw = ImageDraw.Draw(img)

        # betűméret automatikus
        font_size = 16
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # max 8 karakter
        short = text[:8].upper()
        try:
          bbox = draw.textbbox((0, 0), short, font=font)  # (left, top, right, bottom)
          w = bbox[2] - bbox[0]
          h = bbox[3] - bbox[1]
        except Exception:
    # fallback nagyon régi Pillow esetére
          w, h = font.getsize(short)
        draw.text(((64 - w) // 2, (64 - h) // 2), short, fill=(200, 200, 200), font=font)

        img.save(out_path, "JPEG", quality=JPG_QUALITY)

    #
    # --- 1) Megpróbáljuk beolvasni a képet ---
    #
    try:
        img = Image.open(BytesIO(raw_data)).convert("RGB")
    except Exception as e:
        print(f"convert_and_save_icon: invalid image, placeholder generated: {e}")
        make_placeholder(name, filepath)
        return

    w, h = img.size

    #
    # --- 2) Ha NEM négyzet, helyettesítő ikon készül ---
    #
    if w != h:
        print(f"convert_and_save_icon: non-square image ({w}x{h}) → placeholder")
        make_placeholder(name, filepath)
        return

    #
    # --- 3) Normál ikon JPG konverzió ---
    #
    img = img.resize(TARGET_SIZE, Image.LANCZOS)
    img.save(filepath, "JPEG", quality=JPG_QUALITY)

    #
    # --- 4) További tömörítés ha túl nagy ---
    #
    try:
        if os.path.getsize(filepath) > 25000:   # kb. 25 KB limit
            print("convert_and_save_icon: optimizing large JPG…")
            img.save(filepath, "JPEG", quality=70)
    except:
        pass
