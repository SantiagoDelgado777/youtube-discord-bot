import feedparser
import random
import os
import requests

# Reemplaza con el ID de tu canal de YouTube
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Reemplaza si es necesario
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def publicar_video_azar():
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("No se pudieron obtener videos del feed.")
        return

    # Selecciona un video al azar del feed (largos, shorts, en vivo)
    video = random.choice(feed.entries)
    
    titulo = video.title
    link = video.link

    mensaje = f"🎬 ¡Recomendado del canal!\n\n**{titulo}**\n{link}"
    print(f"Publicando: {titulo} -> {link}")

    # Enviar al Webhook de Discord
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        respuesta = requests.post(webhook_url, json={"content": mensaje})
        print(f"Estado del envío a Discord: {respuesta.status_code}")
    else:
        print("Aviso: DISCORD_WEBHOOK_URL no está configurada localmente (se usará en GitHub Actions).")

if __name__ == "__main__":
    publicar_video_azar()
