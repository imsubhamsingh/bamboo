import requests
import time
from threading import Thread

class WebsiteMonitor:
    def __init__(self, websites):
        self.websites = websites
    
    def ping_website(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} is up!")
            else:
                print(f"⚠️  Warning: {url} returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {url} is down!\nError details: {e}")
    
    def start_monitoring(self):
        while True:
            for website in self.websites:
                Thread(target=self.ping_website, args=(website,)).start()
            time.sleep(60)  # Wait for 60 seconds before checking again
