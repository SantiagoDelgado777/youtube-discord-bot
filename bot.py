import feedparser
import random
import os
import requests

# Feed RSS directo del canal @SantiagoDelgadoGames
RSS_URL = "https://www.youtube.com/feeds/videos.xml?user=SantiagoDelgadoGames"

def publicar_video_azar():
    feed = feedparser.parse(RSS_URL)
    
    # Si por alguna razón la URL por user no devuelve la lista, intentamos con el ID directo
    if not feed.entries:
        # Reemplazar con el ID que obtengas al presionar Ctrl+U en tu canal
        CHANNEL_ID = "UCYwFUpXk4aI5D4iK-s6mptw" 
        feed = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}")

    if not feed.entries:
        print("No se encontraron videos en el feed.")
        return

    # Selecciona un video al azar de TU canal
    video = random.choice(feed.entries)
    
    titulo = video.title
    link = video.link

    mensaje = f"🎬 ¡Recomendado del canal!\n\n**{titulo}**\n{link}"
    print(f"Video de @SantiagoDelgadoGames seleccionado: {titulo} -> {link}")

    # Enviar a Discord
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        respuesta = requests.post(webhook_url, json={"content": mensaje})
        print(f"Estado del envío a Discord: {respuesta.status_code}")
    else:
        print("Aviso: DISCORD_WEBHOOK_URL no configurada en local (se usará en GitHub Actions).")

if __name__ == "__main__":
    publicar_video_azar()
