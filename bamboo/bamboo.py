import argparse
import concurrent.futures
import time
import requests

class HTTPLoadTester:
    def __init__(self, urls, num_requests, num_concurrent):
        self.urls = urls
        self.num_requests = num_requests
        self.num_concurrent = num_concurrent
        self.results = []

    def make_request(self, url):
        start_time = time.time()
        try:
            response = requests.get(url)
            status_code = response.status_code
            print(status_code)
        except requests.RequestException:
            status_code = 500
        end_time = time.time()

        return {
            "url": url,
            "status_code": status_code,
            "total_time": end_time - start_time,
            "time_to_first_byte": response.elapsed.total_seconds(),
            "time_to_last_byte": end_time - response.elapsed.total_seconds()
        }

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_concurrent) as executor:
            future_to_url = {executor.submit(self.make_request, url): url for url in self.urls}

            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    self.results.append(result)
                except Exception as e:
                    print(f"Error fetching {url}: {e}")

    def print_results_summary(self):
        # Process and print results summary here
        pass

def main():
    parser = argparse.ArgumentParser(description="Bamboo - HTTP(S) Load Tester")
    parser.add_argument("-u", "--url", help="URL to test")
    parser.add_argument("-n", "--num-requests", type=int, default=10, help="Number of requests to make")
    parser.add_argument("-c", "--num-concurrent", type=int, default=1, help="Number of concurrent requests")
    parser.add_argument("-f", "--file", help="File containing URLs to test")

    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    elif args.file:
        with open(args.file, "r") as file:
            urls = [line.strip() for line in file.readlines()]
    else:
        print("Please provide a URL or a file containing URLs.")
        return

    tester = HTTPLoadTester(urls, args.num_requests, args.num_concurrent)
    tester.run()
    tester.print_results_summary()

if __name__ == "__main__":
    main()
