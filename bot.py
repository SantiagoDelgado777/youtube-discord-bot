import os
import random
import requests
import feedparser

# ID estático e inmutable de tu canal (Santiago Delgado Games)
CHANNEL_ID = "UCYwFUpXk4aI5D4iK-s6mptw"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def publicar_video_azar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        # Descargamos el XML directamente imitando un navegador para evitar redirecciones de YouTube
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al obtener el feed del canal: {e}")
        return

    # Parseamos el XML recuperado
    feed = feedparser.parse(response.text)
    
    if not feed.entries:
        print("No se encontraron videos en el feed.")
        return

    # Selecciona un video al azar de tu canal
    video = random.choice(feed.entries)
    
    titulo = video.title
    link = video.link

    mensaje = f"🎬 ¡Recomendado del canal!\n\n**{titulo}**\n{link}"
    print(f"Video seleccionado correctamente: {titulo} -> {link}")

    # Enviar a Discord mediante Webhook
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        res = requests.post(webhook_url, json={"content": mensaje})
        print(f"Estado del envío a Discord: {res.status_code}")
    else:
        print("Aviso: DISCORD_WEBHOOK_URL no configurada localmente (se ejecutará en GitHub Actions).")

if __name__ == "__main__":
    publicar_video_azar()
