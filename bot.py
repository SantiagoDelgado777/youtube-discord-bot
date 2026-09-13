import os
import re
import random
import requests

HANDLE = "SantiagoDelgadoGames"
URL_VIDEOS = f"https://www.youtube.com/@{HANDLE}/videos"

def obtener_videos_canal():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9"
    }

    try:
        response = requests.get(URL_VIDEOS, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error al conectar con el canal: {e}")
        return []

    # Extraer los IDs de los videos pertenecientes al canal
    video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', response.text)
    
    # Filtrar duplicados
    return list(dict.fromkeys(video_ids))

def publicar_video_azar():
    print(f"Buscando videos en @{HANDLE}...")
    video_ids = obtener_videos_canal()

    if not video_ids:
        print("No se pudieron extraer videos del canal.")
        return

    video_id_elegido = random.choice(video_ids)
    link_video = f"https://www.youtube.com/watch?v={video_id_elegido}"

    mensaje = f"🎬 ¡Recomendado del canal @{HANDLE}!\n\n{link_video}"
    print(f"Video seleccionado: {link_video}")

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        res = requests.post(webhook_url, json={"content": mensaje})
        print(f"Respuesta de Discord Webhook: {res.status_code}")
    else:
        print("Aviso: DISCORD_WEBHOOK_URL no configurada en entorno local.")

if __name__ == "__main__":
    publicar_video_azar()
