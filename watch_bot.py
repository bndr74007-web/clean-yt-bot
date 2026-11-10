import os, requests, random, time, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# عداد المشاهدات اللي جابها البوت
bot_views = 0
used_proxies = set()

# تعديل السيرفر الوهمي عشان يعرض العداد حقنا
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

def get_free_proxies():
    try:
        response = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", timeout=10)
        return response.text.strip().split('\n')
    except:
        return []

def watch_video(bot_id):
    global used_proxies, bot_views
    while True:
        proxies = get_free_proxies()
        available_proxies = [p for p in proxies if p not in used_proxies]
        
        if not available_proxies:
            used_proxies.clear()
            time.sleep(600)
            continue
            
        proxy = random.choice(available_proxies)
        used_proxies.add(proxy)
        
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
            
            # مشاهدة 10 دقايق مع وقت عشوائي
            watch_time = 600 + random.randint(30, 90)
            time.sleep(watch_time)
            
            # لو كمل المشاهدة بدون ما يفصل، زيد العداد!
            bot_views += 1
            
        except Exception as e:
            pass
        finally:
            try:
                driver.quit()
            except:
                pass
        time.sleep(10)

NUM_THREADS = 3
for i in range(NUM_THREADS):
    t = threading.Thread(target=watch_video, args=(i+1,))
    t.start()
    time.sleep(5)

while True:
    time.sleep(3600)
