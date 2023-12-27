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
        self.errors = []

    def make_request(self, url):
        times = []
        status_codes = []
        for _ in range(self.num_requests):
            try:
                start_time = time.time()
                response = requests.get(url)
                end_time = time.time()
                times.append(
                    {
                        "total_time": end_time - start_time,
                        "time_to_first_byte": response.elapsed.total_seconds(),
                        "time_to_last_byte": end_time
                        - response.elapsed.total_seconds(),
                    }
                )
                status_codes.append(response.status_code)
            except requests.RequestException:
                status_codes.append(500)
        # print(status_codes)
        return {"url": url, "times": times, "status_codes": status_codes}

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_concurrent
        ) as executor:
            tasks = [executor.submit(self.make_request, url) for url in self.urls]
            for future in concurrent.futures.as_completed(tasks):
                try:
                    self.results.append(future.result())
                except Exception as e:
                    self.errors.append(str(e))

    def print_results_summary(self):
        for result in self.results:
            url = result["url"]
            avg_time = sum(d["total_time"] for d in result["times"]) / len(
                result["times"]
            )
            print(
                f"URL: {url}, Average Time: {avg_time:.2f}s, Status Codes: {result['status_codes']}"
            )
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(error)


def main():
    parser = argparse.ArgumentParser(description="Bamboo - HTTP(S) Load Tester")
    parser.add_argument("-u", "--url", help="URL to test")
    parser.add_argument(
        "-n", "--num-requests", type=int, default=10, help="Number of requests to make"
    )
    parser.add_argument(
        "-c",
        "--num-concurrent",
        type=int,
        default=1,
        help="Number of concurrent requests",
    )
    parser.add_argument("-f", "--file", help="File containing URLs to test")

    args = parser.parse_args()

    if args.url:
        urls = [args.url]
    elif args.file:
        with open(args.file, "r") as file:
            urls = file.read().splitlines()
    else:
        print("Please provide a URL or a file containing URLs.")
        return

    tester = HTTPLoadTester(urls, args.num_requests, args.num_concurrent)
    tester.run()
    tester.print_results_summary()


if __name__ == "__main__":
    main()
