import requests
import time
import concurrent.futures
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 5


class WebsiteMonitor:
    """
    Using ThreadPoolExecutor class which provides a high-level interface for
    asynchronously executing callables.
    """

    def __init__(self, websites):
        self.websites = websites

    def ping_website(self, url):
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
        except requests.exceptions.RequestException as e:
            print(f"{timestamp} ❌ Error: {url} is down!\nError details: {e}")
            return False
        else:
            if status_code == 200:
                print(f"{timestamp} ✅ {url} is up!")
                return True
            else:
                print(
                    f"{timestamp} ⚠️  Warning: {url} returned status code {status_code}"
                )
                return False

    def start_monitoring(self):
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            while True:
                # Initiate the ping_website calls concurrently for all websites.
                future_to_url = {
                    executor.submit(self.ping_website, url): url
                    for url in self.websites
                }
                # Iterate through the futures as they complete (whether successfully or not).
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        future.result()  # We can check the result or do post-processing here.
                    except Exception as exc:
                        print(f"{url} generated an exception: {exc}")
                # Wait for 60 seconds after all tasks have been processed,
                # not from the beginning of the task submission.
                time.sleep(60)
