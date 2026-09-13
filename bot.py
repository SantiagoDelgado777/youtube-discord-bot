import feedparser
import random
import os
import requests

# ID de canal inmutable de @SantiagoDelgadoGames
CHANNEL_ID = "UCYwFUpXk4aI5D4iK-s6mptw"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def publicar_video_azar():
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("No se encontraron videos en el feed.")
        return

    # Selecciona un video al azar de SantiagoDelgadoGames
    video = random.choice(feed.entries)
    
    titulo = video.title
    link = video.link

    mensaje = f"🎬 ¡Recomendado del canal!\n\n**{titulo}**\n{link}"
    print(f"Video seleccionado de SantiagoDelgadoGames: {titulo} -> {link}")

    # Enviar a Discord mediante Webhook
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        respuesta = requests.post(webhook_url, json={"content": mensaje})
        print(f"Estado del envío a Discord: {respuesta.status_code}")
    else:
        print("Aviso: DISCORD_WEBHOOK_URL no configurada en local (se usará en GitHub Actions).")

if __name__ == "__main__":
    publicar_video_azar()
