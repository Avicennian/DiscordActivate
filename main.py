import discord
import os
import asyncio
import random
from flask import Flask

# Flask uygulamasını oluşturarak Render'ın web servisi olarak algılamasını sağlıyoruz.
app = Flask(__name__)

@app.route('/')
def home():
    return "Hesap aktif tutuluyor."

def run_app():
    app.run(host='0.0.0.0', port=10000)

# Discord istemcisini (client) tanımlıyoruz.
# Self-bot'lar için 'intents' genellikle gerekli değildir ama olası durumlar için eklenmiştir.
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Değiştirmek istediğin durumlar ve özel mesajlar
STATUS_OPTIONS = [
    discord.Status.online,      # Aktif
    discord.Status.idle,        # Boşta
    discord.Status.dnd          # Rahatsız Etmeyin (Do Not Disturb)
]

# İsteğe bağlı olarak buraya farklı özel durum mesajları ekleyebilirsin.
# Boş bırakmak için: CUSTOM_STATUS_MESSAGES = [""]
CUSTOM_STATUS_MESSAGES = [
    "7/24 Aktif!",
    "Render ile çalışıyor...",
    "Başka bir projeyle meşgulüm.",
    "" # Buradaki boş tırnak, hiçbir özel durum göstermemeyi sağlar.
]

@client.event
async def on_ready():
    print(f'{client.user} olarak giriş yapıldı.')
    print('Hesap 7/24 aktif tutulmaya hazır!')
    print('------------------------------------')
    await change_status()

async def change_status():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            # Rastgele bir durum ve özel mesaj seçimi
            new_status = random.choice(STATUS_OPTIONS)
            new_activity_message = random.choice(CUSTOM_STATUS_MESSAGES)

            # Özel durumu (Custom Status) ayarlamak için Activity objesi oluşturuyoruz.
            new_activity = discord.CustomActivity(name=new_activity_message)

            # Yeni durumu ve aktiviteyi uyguluyoruz.
            await client.change_presence(status=new_status, activity=new_activity)

            print(f"Durum değiştirildi: {new_status} | Mesaj: '{new_activity_message}'")

            # Durumu ne sıklıkla değiştireceğini buradan ayarlayabilirsin (saniye cinsinden).
            # Örneğin 900 saniye = 15 dakika
            await asyncio.sleep(900)

        except Exception as e:
            print(f"Durum değiştirilirken bir hata oluştu: {e}")
            # Hata durumunda bir süre bekleyip tekrar denemesi için
            await asyncio.sleep(60)

# Flask'ı ayrı bir thread'de başlat
import threading
threading.Thread(target=run_app).start()

# Discord Token'ını al ve botu çalıştır
# Token'ı doğrudan koda yazmak yerine Render'ın ortam değişkenlerinden alacağız.
try:
    token = os.environ.get("DISCORD_TOKEN")
    if token is None:
        raise ValueError("DISCORD_TOKEN ortam değişkeni bulunamadı. Lütfen Render ayarlarını kontrol et.")
    client.run(token)
except (discord.errors.LoginFailure, ValueError) as e:
    print(f"Giriş hatası: {e}")
    print("Lütfen geçerli bir kullanıcı token'ı girdiğinizden emin olun.")
except Exception as e:
    print(f"Bot çalıştırılırken beklenmedik bir hata oluştu: {e}")
