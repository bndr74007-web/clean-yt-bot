import os
import requests
import random
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# خادم الويب الوهمي عشان راوند ما يطفي السيرفر
def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

video_url = os.environ.get("VIDEO_URL")
if not video_url:
    try:
        with open("url.txt", "r") as f:
            video_url = f.read().strip()
    except:
        video_url = "https://youtu.be/9Uz04LYQe5k?si=m5KdjuWAC8_DMGs_"

# ذاكرة البوت لتسجيل الآي بي هات المستخدمة عشان ما يكررها
used_proxies = set()

def get_free_proxies():
    url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    try:
        response = requests.get(url, timeout=10)
        return response.text.strip().split('\n')
    except:
        return []

def watch_video(bot_id):
    global used_proxies
    while True:
        proxies = get_free_proxies()
        # فلترة البروكسيات: أخذ اللي ما تم استخدامها فقط
        available_proxies = [p for p in proxies if p not in used_proxies]
        
        if not available_proxies:
            print(f"[بوت {bot_id}] خلصت كل البروكسيات! بنتظر 10 دقايق تتحدث القائمة...")
            used_proxies.clear() # تفريغ الذاكرة إذا خلصت القائمة كلها
            time.sleep(600)
            continue
            
        proxy = random.choice(available_proxies)
        used_proxies.add(proxy) # تسجيل الآي بي كمُستخدم
        print(f"[بوت {bot_id}] تم استلام IP جديد: {proxy}")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f'--proxy-server=http://{proxy}')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(60)
            driver.get(video_url)
            
            # مشاهدة الفيديو بالكامل (مثلاً نفترض أن الفيديو 10 دقايق = 600 ثانية)
            # تم إضافة وقت عشوائي عشان يوتيوب ما يشك إنه بوت
            watch_time = 600 + random.randint(30, 90) 
            print(f"[بوت {bot_id}] جاري مشاهدة الفيديو لمدة {watch_time} ثانية...")
            time.sleep(watch_time)
            
        except Exception as e:
            print(f"[بوت {bot_id}] الآي بي طلع ميت أو بطيء، جاري تبديله فوراً...")
        finally:
            try:
                driver.quit()
            except:
                pass
        
        # استراحة قصيرة قبل الهجوم بآي بي جديد
        time.sleep(10)

# تشغيل 3 نسخ متوازية في نفس اللحظة (الحد الأقصى للرام المجاني)
NUM_THREADS = 3

print(f"🚀 إطلاق {NUM_THREADS} متصفحات متزامنة بآي بي هات مختلفة...")
for i in range(NUM_THREADS):
    t = threading.Thread(target=watch_video, args=(i+1,))
    t.start()
    time.sleep(5) # تأخير بسيط بين كل بوت عشان ما يختنق السيرفر

# إبقاء السكربت شغال
while True:
    time.sleep(3600)
