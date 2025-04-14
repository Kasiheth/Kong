from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
import requests
from bs4 import BeautifulSoup
import os

# Ambil token dan channel ID dari environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Misalnya: @NamaChannel atau -100xxxxxxxxxx

# Fungsi untuk scraping freemint dari nfts2.me
def get_freemint_info():
    try:
        url = "https://nfts2.me/trending?chain=apechain"  # Ganti jika URL berbeda
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        mints = soup.find_all("div", class_="nft-card")  # Sesuaikan class
        results = []
        for mint in mints[:3]:
            name = mint.find("h3").text if mint.find("h3") else "Tidak ada nama"
            link = mint.find("a")["href"] if mint.find("a") else "Tidak ada link"
            results.append(f"Nama: {name}\nLink: {link}\n")
        return "\n".join(results) or "Tidak ada info freemint saat ini."
    except Exception as e:
        return f"Error: {str(e)}"

# Handler untuk /start (opsional, untuk debugging)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! Info freemint dikirim ke channel.")

# Fungsi untuk mengirim info ke channel
async def send_freemint_to_channel(context: ContextTypes.DEFAULT_TYPE):
    info = get_freemint_info()
    await context.bot.send_message(chat_id=CHANNEL_ID, text=info)

def main():
    # Inisialisasi aplikasi
    app = Application.builder().token(TOKEN).build()

    # Tambahkan handler (opsional)
    app.add_handler(CommandHandler("start", start))

    # Jadwalkan pengiriman ke channel (misalnya, setiap 3600 detik = 1 jam)
    job_queue = app.job_queue
    job_queue.run_repeating(send_freemint_to_channel, interval=3600, first=10)

    # Jalankan bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
