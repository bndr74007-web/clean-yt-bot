import os, time, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

bot_views = 0

class BotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(str(bot_views).encode('utf-8'))

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), BotHandler)
    server.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

video_url = os.environ.get("VIDEO_URL")
if not video_url:
    try:
        with open("url.txt", "r") as f:
            video_url = f.read().strip()
    except:
        video_url = "https://youtu.be/9Uz04LYQe5k?si=m5KdjuWAC8_DMGs_"

def watch_loop():
    global bot_views
    while True:
        options = Options()
        options.headless = True
        
        try:
            # استخدام فايرفوكس لأدائه المستقر وعدم استهلاك الرام
            driver = webdriver.Firefox(options=options)
            driver.set_page_load_timeout(60)
            
            print("🚀 جاري فتح الفيديو عبر المتصفح المستقر...")
            driver.get(video_url)
            
            # مشاهدة الفيديو القصير بالكامل مع وقت أمان
            time.sleep(35)
            bot_views += 1
            print(f"✅ تم تسجيل مشاهدة ناجحة! الإجمالي: {bot_views}")
            
            driver.quit()
        except Exception as e:
            print(f"⚠️ إعادة محاولة بسبب خطأ مؤقت: {e}")
            try:
                driver.quit()
            except:
                pass
        
        # راحة قصيرة بين الإعادة لتجنب الحظر
        time.sleep(5)

# تشغيل خيط واحد مستقر ومضمون لا يضغط على السيرفر
threading.Thread(target=watch_loop, daemon=True).start()

while True:
    time.sleep(3600)
