import telebot
import os
from yt_dlp import YoutubeDL

# আপনার তথ্য
BOT_TOKEN = "8672535540:AAGLCx-9hXmhBA9NY2q46NbbGLF898neEnk"
PROXY_BRIDGE = "https://prime-xyron-api.paylinkbd774.workers.dev/?url="

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 হ্যালো! ইউটিউব লিঙ্ক পাঠান, আমি প্রক্সির মাধ্যমে ডাউনলোড করে দিচ্ছি।")

@bot.message_handler(func=lambda message: True)
def handle_video(message):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        msg = bot.reply_to(message, "⏳ প্রক্সির মাধ্যমে ভিডিও প্রসেস করছি...")
        
        # ফাইল নাম নির্ধারণ
        file_path = f"{message.chat.id}.mp4"

        # yt-dlp অপশন
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_path,
            'quiet': True,
            # এখানে গুরুত্বপূর্ণ পরিবর্তন: প্রক্সি সরাসরি yt-dlp এর ভেতরে সেট করা হয়েছে
            'proxy': PROXY_BRIDGE + url, 
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        try:
            # এবার আমরা সরাসরি অরিজিনাল ইউটিউব লিঙ্ক দেব, কিন্তু প্রক্সি অপশন ব্যবহার করব
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # টেলিগ্রামে ভিডিও পাঠানো
            if os.path.exists(file_path):
                with open(file_path, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption="ডাউনলোড সম্পন্ন! ✅")
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
