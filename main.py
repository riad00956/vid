import telebot
import os
import json
from yt_dlp import YoutubeDL

# আপনার তথ্য
BOT_TOKEN = "8672535540:AAGLCx-9hXmhBA9NY2q46NbbGLF898neEnk"
PROXY_BRIDGE = "https://prime-xyron-api.paylinkbd774.workers.dev/?url="

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 হ্যালো! আপনার দেওয়া cookie.json ব্যবহার করে আমি এখন ভিডিও ডাউনলোড করতে প্রস্তুত। লিঙ্ক পাঠান!")

@bot.message_handler(func=lambda message: True)
def handle_video(message):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        msg = bot.reply_to(message, "⏳ প্রক্সির মাধ্যমে এবং কুকি ব্যবহার করে ভিডিও প্রসেস করছি...")
        
        file_path = f"{message.chat.id}.mp4"

        # yt-dlp অপশন
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_path,
            'quiet': True,
            'proxy': PROXY_BRIDGE + url, 
            'cookiefile': 'cookie.json', # আপনার দেওয়া ফাইলের নাম এখানে ঠিক থাকতে হবে
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption="সফলভাবে ডাউনলোড হয়েছে! ✅")
                os.remove(file_path)
            
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ এরর: {str(e)}", message.chat.id, msg.message_id)
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        bot.reply_to(message, "দয়া করে সঠিক ইউটিউব লিঙ্ক দিন।")

if __name__ == "__main__":
    bot.infinity_polling()
