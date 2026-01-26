import json
from aiohttp import ClientSession
from PIL import Image
from io import BytesIO
import os
import sys
import re
import unicodedata

sys.path.append("/config/python_modules")

from icon_worker import convert_and_save_icon

ICON_DIR = "/config/www/icons"


async def convert_icon_core(url: str, filename: str) -> str:
    """
    Ezt hívjuk majd közvetlenül a másik scriptből.
    Visszaadja a /local/... URL-t vagy üres stringet.
    """
    try:
        os.makedirs(ICON_DIR, exist_ok=True)

        # Kép letöltése
        async with ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    log.error(f"convert_icon_core: HTTP {resp.status} - {url}")
                    return ""
                raw = await resp.read()

        # Fájlnév és mentés path
        filepath = os.path.join(ICON_DIR, filename + ".jpg")

        # Blokkoló műveletet thread poolba tesszük
        await task.executor(convert_and_save_icon, raw, filepath, filename)

        final_url = f"/local/icons/{filename}.jpg"
        log.info(f"Icon converted: {url} -> {final_url}")
        return final_url

    except Exception as e:
        log.error(f"convert_icon_core error: {e}")
        return ""


@service
async def convert_icon(url: str, filename: str) -> str:
    """
    Ugyanaz, csak HA service-ként is elérhető (Developer Tools -> Services).
    A belső logika convert_icon_core-ban van.
    """
    return await convert_icon_core(url, filename)

def safe_filename(name: str) -> str:
    # Unicode normalizáció
    name = unicodedata.normalize('NFKD', name)
    # Minden nem-ASCII karakter törlése
    name = name.encode('ascii', 'ignore').decode()
    # Minden nem-alphanumerikus → _
    name = re.sub(r'[^A-Za-z0-9_-]+', '_', name)
    # dupla aláhúzás csökkentése
    name = re.sub(r'_+', '_', name)
    # vezető/trailing _ eltüntetése
    name = name.strip('_')
    return name.lower()
    
@service("pyscript.get_ma_radios")
async def get_ma_radios():
    """
    Lekéri a Music Assistant rádiókat és eltárolja
    sensor.radiok attributes alatt (state = 'ok').
    """

    # --- 1. Music Assistant library lekérése ---
    resp = await hass.services.async_call(
        "music_assistant",
        "get_library",
        {
            "config_entry_id": "01K6G6E2QCYK3N5DN69RJRQ5TA",
            "media_type": "radio",
            "favorite": True,
            "limit": 25,
            "offset": 0,
            "order_by": "name"
        },
        blocking=True,
        return_response=True
    )

    items = resp.get("items", [])
    radios = []

    # --- 2. Csak a szükséges mezőket vesszük át ---
    for item in items:
        name = item.get("name", "")
        safe_name = safe_filename(name)
        icon_url = item.get("image", "")
        png_icon=""
        if icon_url:
            png_icon = await convert_icon_core(icon_url, safe_name)
        if not png_icon:
            png_icon = "/local/icons/default.png"
        radios.append({
          "uri": item.get("uri", ""),
          "name": safe_name,
          "image": png_icon
        })

    # --- 3. Szenzor frissítése ---
    # STATE: rövid (a HA state max 255 karakter!)
    # ATTRIBUTES: ide kerül a teljes lista
    await task.executor(
        hass.states.set,
        "sensor.radiok",   # entity
        "ok",              # rövid state
        {"radios": radios} # attributes
    )

    log.info(f"MA rádiók frissítve: {len(radios)} db rádió")
