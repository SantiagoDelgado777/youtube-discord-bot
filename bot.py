import os
import requests
import feedparser

# ID de tu canal de YouTube
YOUTUBE_CHANNEL_ID = "UC-cR5jY0-O3hD7yJ7f_yBkg"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
LAST_VIDEO_FILE = "last_video.txt"

def get_last_saved_id():
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_id(video_id):
    with open(LAST_VIDEO_FILE, "w") as f:
        f.write(video_id)

def main():
    if not DISCORD_WEBHOOK_URL:
        print("Error: No se encontró la URL del Webhook de Discord.")
        return

    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("No se encontraron vídeos en el feed RSS.")
        return

    latest_entry = feed.entries[0]
    latest_id = latest_entry.yt_videoid
    latest_title = latest_entry.title
    latest_link = latest_entry.link

    last_id = get_last_saved_id()

    # Si hay un vídeo nuevo que no se ha notificado previamente
    if latest_id != last_id:
        if last_id != "":
            payload = {
                "content": f"¡Nuevo vídeo en el canal! 🚀\n**{latest_title}**\n{latest_link}"
            }
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
            if response.status_code == 204:
                print(f"Notificación enviada a Discord: {latest_title}")
            else:
                print(f"Error al enviar a Discord: {response.status_code}")
        else:
            print(f"Inicializado el registro con el vídeo actual: {latest_id}")
        
        save_last_id(latest_id)
    else:
        print("No hay vídeos nuevos.")

if __name__ == "__main__":
    main()
