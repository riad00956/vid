import telebot
import os
import requests
from yt_dlp import YoutubeDL

# আপনার তথ্য
BOT_TOKEN = "8672535540:AAGLCx-9hXmhBA9NY2q46NbbGLF898neEnk"
PROXY_BRIDGE = "https://prime-xyron-api.paylinkbd774.workers.dev/?url="

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 হ্যালো! আমি আপনার ভিডিও ডাউনলোডার বট।\nএকটি ইউটিউব লিঙ্ক পাঠান, আমি প্রক্সির মাধ্যমে সেটি পাঠিয়ে দিচ্ছি।")

@bot.message_handler(func=lambda message: True)
def handle_video(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        msg = bot.reply_to(message, "⏳ প্রক্সির মাধ্যমে ভিডিও প্রসেস করছি...")
        
        # প্রক্সি ইউআরএল এবং ফাইল পাথ
        proxied_url = f"{PROXY_BRIDGE}{url}"
        file_path = f"{message.chat.id}.mp4"

        ydl_opts = {
            'format': 'best[ext=mp4]/best', # রেন্ডারে mp4 ফরম্যাট সবচেয়ে নিরাপদ
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([proxied_url])
            
            # টেলিগ্রামে ভিডিও পাঠানো
            with open(file_path, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="ডাউনলোড সম্পন্ন! ✅")
            
            # রেন্ডারের ডিস্ক স্পেস বাঁচাতে ফাইল ডিলিট
            if os.path.exists(file_path):
                os.remove(file_path)
            
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ এরর: {str(e)}", message.chat.id, msg.message_id)
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        bot.reply_to(message, "দয়া করে শুধুমাত্র ইউটিউব লিঙ্ক দিন।")

if __name__ == "__main__":
    print("Bot is running on Render...")
    bot.infinity_polling()
