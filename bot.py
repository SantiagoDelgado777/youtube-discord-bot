import feedparser
import random
import os
import requests
import re

HANDLE = "SantiagoDelgadoGames"

def obtener_channel_id(handle):
    url = f"https://www.youtube.com/@{handle}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers)
        # Buscar el ID del canal en los metadatos de YouTube
        match = re.search(r'https://www\.youtube\.com/channel/(UC[\w-]+)', r.text)
        if match:
            return match.group(1)
        match_meta = re.search(r'"channelId":"(UC[\w-]+)"', r.text)
        if match_meta:
            return match_meta.group(1)
    except Exception as e:
        print(f"Error al buscar el Channel ID: {e}")
    return None

def publicar_video_azar():
    channel_id = obtener_channel_id(HANDLE)
    
    if not channel_id:
        print(f"Error: No se pudo obtener el Channel ID de @{HANDLE}.")
        return

    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("No se encontraron videos en el feed de tu canal.")
        return

    # Selecciona un video al azar exclusivamente de TU canal
    video = random.choice(feed.entries)
    
    titulo = video.title
    link = video.link

    mensaje = f"🎬 ¡Recomendado del canal!\n\n**{titulo}**\n{link}"
    print(f"Video seleccionado de @{HANDLE}: {titulo} -> {link}")

    # Enviar al Webhook de Discord
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        respuesta = requests.post(webhook_url, json={"content": mensaje})
        print(f"Estado del envío a Discord: {respuesta.status_code}")
    else:
        print("Aviso: DISCORD_WEBHOOK_URL no está configurada localmente (se enviará mediante GitHub Actions).")

if __name__ == "__main__":
    publicar_video_azar()
