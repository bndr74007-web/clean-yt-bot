import os
import requests
import random
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        exit()

def get_free_proxies():
    url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    try:
        response = requests.get(url, timeout=10)
        return response.text.strip().split('\n')
    except:
        return []

proxies = get_free_proxies()
if proxies:
    proxy = random.choice(proxies)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.set_page_load_timeout(60)
        driver.get(video_url)
        while True: 
            time.sleep(3600)
    except Exception as e:
        pass
    finally:
        driver.quit()
