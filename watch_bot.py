import os, requests, random, time, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

bot_views = 0
used_proxies = set()

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
            time.sleep(60) # انتظار دقيقة وحدة بس لو خلصت البروكسيات
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
            driver.set_page_load_timeout(30)
            driver.get(video_url)
            
            # ⏳ التعديل السحري: مشاهدة 30 إلى 35 ثانية فقط لأن الفيديو قصير!
            watch_time = random.randint(30, 35)
            time.sleep(watch_time)
            
            bot_views += 1
            
        except Exception as e:
            pass
        finally:
            try:
                driver.quit()
            except:
                pass
        
        # استراحة ثانية وحدة بس ويطير للآي بي اللي بعده!
        time.sleep(1)

NUM_THREADS = 3
for i in range(NUM_THREADS):
    t = threading.Thread(target=watch_video, args=(i+1,))
    t.start()
    time.sleep(3)

while True:
    time.sleep(3600)
