import telebot
import os
import json
import time
from yt_dlp import YoutubeDL
import urllib.parse

BOT_TOKEN = "8672535540:AAHCDw6BHY4XMMbkfG3j3UkS8XoYZdr3QGY"
PROXY_BRIDGE = "https://prime-xyron-api.paylinkbd774.workers.dev/?url="

bot = telebot.TeleBot(BOT_TOKEN)

# JSON to Netscape converter (আগের মতোই থাকবে)
def convert_json_to_netscape(json_file, output_file):
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
                expiry = int(c.get('expirationDate', time.time() + 360000))
                name = c.get('name', '')
                value = c.get('value', '')
                f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")
        return True
    except: return False

@bot.message_handler(func=lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
def handle_video(message):
    msg = bot.reply_to(message, "⏳ প্রক্সির মাধ্যমে ডাউনলোড শুরু হচ্ছে...")
    url = message.text.strip()
    file_path = f"{message.chat.id}.mp4"
    cookie_txt = "cookies.txt"

    convert_json_to_netscape("cookie.json", cookie_txt)

    # গুরুত্বপূর্ণ: এখানে আমরা সরাসরি প্রক্সি ইউআরএল তৈরি করছি
    # yt-dlp এর 'proxy' সেটিংস ব্যবহার না করে সরাসরি URL বদলে দিচ্ছি
    proxied_url = f"{PROXY_BRIDGE}{urllib.parse.quote(url)}"

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': file_path,
        'quiet': True,
        'cookiefile': cookie_txt if os.path.exists(cookie_txt) else None,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # এবার প্রক্সি করা ইউআরএল সরাসরি ডাউনলোড হবে
            ydl.download([proxied_url])
        
        with open(file_path, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="ডাউনলোড সম্পন্ন! ✅")
        
        os.remove(file_path)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ এরর: {str(e)}", message.chat.id, msg.message_id)
        if os.path.exists(file_path): os.remove(file_path)

bot.infinity_polling()
