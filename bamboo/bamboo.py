import argparse
import concurrent.futures
import time
import requests
from prettytable import PrettyTable


class HTTPLoadTester:
    def __init__(self, urls, num_requests, num_concurrent, debug=False):
        self.urls = urls
        self.num_requests = num_requests
        self.num_concurrent = num_concurrent
        self.session = requests.Session()  # Use a session object for connection pooling
        self.results = []
        self.errors = []
        self.debug = debug

    def make_request(self, url):
        times = []
        status_codes = []
        error_count = 0

        for _ in range(self.num_requests):
            try:
                start_time = time.time()
                response = self.session.get(url)
                times.append(time.time() - start_time)
                status_codes.append(response.status_code)
            except requests.RequestException:
                status_codes.append(500)
                error_count += 1

        return {
            "url": url,
            "times": times,
            "status_codes": status_codes,
            "error_count": error_count,
        }

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_concurrent
        ) as executor:
            tasks = {executor.submit(self.make_request, url): url for url in self.urls}
            for future in concurrent.futures.as_completed(tasks):
                url = tasks[future]
                try:
                    result = future.result()
                    if self.debug:
                        print(f"Result for {url}: {result}")
                    self.results.append(result)
                except Exception as e:
                    if self.debug:
                        print(f"Error fetching {url}: {str(e)}")
                    self.results.append(
                        {"url": url, "times": [], "status_codes": [], "error_count": 1}
                    )

    def print_results_summary(self):
        table = PrettyTable()

        # Updating field names to include more details
        field_names = [
            "URL",
            "Average Time (s)",
            "Min Time (s)",
            "Max Time (s)",
            "Requests",
            "Status Codes",
            "Error Counts",
        ]
        table.field_names = field_names

        for result in self.results:
            url = result["url"]
            if result["times"]:
                avg_time = sum(result["times"]) / len(result["times"])
                min_time = min(result["times"])
                max_time = max(result["times"])
            else:
                avg_time = min_time = max_time = "N/A"

            num_requests = len(result["times"])
            status_codes = ", ".join(map(str, set(result["status_codes"])))
            # Counting errors
            error_counts = result.get("errors", {}).get("count", 0)

            # Adding a row for each result with the new details
            table.add_row(
                [
                    url,
                    f"{avg_time:.2f}",
                    f"{min_time:.2f}",
                    f"{max_time:.2f}",
                    num_requests,
                    status_codes,
                    error_counts,
                ]
            )

        # Printing the table with added details
        print(table)


def main():
    parser = argparse.ArgumentParser(description="Bamboo - HTTP(S) Load Tester")
    parser.add_argument("-u", "--url", help="URL to test")
    parser.add_argument("--debug", action="store_true", help="Enable DEBUG output")
    parser.add_argument(
        "-n", "--num-requests", type=int, default=5, help="Number of requests to make"
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

    DEBUG = args.debug
    if DEBUG:
        print("Debug mode is ON")
        print(f"Args: {args}")

    if args.url:
        urls = [args.url]
    elif args.file:
        with open(args.file, "r") as file:
            urls = file.read().splitlines()
            if DEBUG:
                print(urls)
    if not urls:
        print("Please provide a URL or a file containing URLs.")
        return

    if DEBUG:
        print(f"URLs: {urls}")

    tester = HTTPLoadTester(urls, args.num_requests, args.num_concurrent)
    tester.run()
    tester.print_results_summary()


if __name__ == "__main__":
    main()
