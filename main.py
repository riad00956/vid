import telebot
import os
import json
import time
from yt_dlp import YoutubeDL

# আপনার তথ্য
BOT_TOKEN = "8672535540:AAGLCx-9hXmhBA9NY2q46NbbGLF898neEnk"
PROXY_BRIDGE = "https://prime-xyron-api.paylinkbd774.workers.dev/?url="

bot = telebot.TeleBot(BOT_TOKEN)

def convert_json_to_netscape(json_file, output_file):
    """JSON কুকিকে Netscape (yt-dlp সমর্থিত) ফরম্যাটে রূপান্তর"""
    try:
        if not os.path.exists(json_file): return False
        with open(json_file, 'r') as f:
            cookies = json.load(f)
        with open(output_file, 'w') as f:
            f.write("# Netscape HTTP Cookie File\n")
            for c in cookies:
                domain = c.get('domain', '')
                flag = "TRUE" if not c.get('hostOnly', False) else "FALSE"
                path = c.get('path', '/')
                secure = "TRUE" if c.get('secure', False) else "FALSE"
                expiry = int(c.get('expirationDate', time.time() + 3600))
                name = c.get('name', '')
                value = c.get('value', '')
                f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")
        return True
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 হ্যালো! ইউটিউবপাঠান, আমি প্রক্সি ও কুকি ব্যবহার করে ডাউনলোড করে দিচ্ছি।")

@bot.message_handler(func=lambda message: True)
def handle_video(message):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        msg = bot.reply_to(message, "⏳ প্রক্সির মাধ্যমে ভিডিও প্রসেস করছি...")
        
        file_path = f"{message.chat.id}.mp4"
        cookie_txt = "cookies.txt"

        # কুকি রূপান্তর
        convert_json_to_netscape("cookie.json", cookie_txt)

        # yt-dlp কনফিগারেশন
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
            # এখানে সরাসরি ইউটিউব লিঙ্কের আগে প্রক্সি ব্রিজটি বসানো হয়েছে
            'proxy': PROXY_BRIDGE + url, 
            'cookiefile': cookie_txt if os.path.exists(cookie_txt) else None,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                # এখানে আমরা শুধু অরিজিনাল ইউআরএল দিচ্ছি, 
                # কারণ প্রক্সি অপশনটি উপরে 'proxy' কী-তে সেট করা আছে।
                ydl.download([url])
            
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
