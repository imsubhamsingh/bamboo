import argparse
import concurrent.futures
import time
import requests
from prettytable import PrettyTable


class HTTPLoadTester:
    def __init__(
        self, urls, num_requests, num_concurrent, debug=False, delay=0, timeout=10
    ):
        self.urls = urls
        self.num_requests = num_requests
        self.num_concurrent = num_concurrent
        self.session = requests.Session()  # Use a session object for connection pooling
        self.results = []
        self.errors = []
        self.debug = debug
        self.delay = delay
        self.timeout = timeout

    def make_request(self, url, method="GET", data=None, headers=None):
        times = []
        status_codes = []
        error_count = 0

        for _ in range(self.num_requests):
            try:
                if self.delay > 0:
                    time.sleep(self.delay)

                start_time = time.time()
                response = self.session.request(
                    method, url, data=data, headers=headers, timeout=self.timeout
                )
                times.append(time.time() - start_time)
                status_codes.append(response.status_code)

            except requests.RequestException as e:
                status_codes.append(None)
                error_count += 1
                if self.debug:
                    print(f"Request Error: {str(e)}")

            # Add a delay between requests if specified
            if self.delay > 0:
                time.sleep(self.delay)

        return {
            "url": url,
            "methods": method,
            "times": times,
            "status_codes": status_codes,
            "error_count": error_count,
        }

    def run(self, method="GET", data=None, headers=None):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.num_concurrent
        ) as executor:
            # Wrap the make_request arguments into a tuple for each URL
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
                        {
                            "url": url,
                            "method": method,
                            "times": [],
                            "status_codes": [],
                            "error_count": 1,
                        }
                    )

    def print_results_summary(self):
        table = PrettyTable()

        # Updating field names to include more details
        field_names = [
            "URL",
            "Method",
            "Average Time (s)",
            "Min Time (s)",
            "Max Time (s)",
            "Requests",
            "Successful Responses",
            "Timed Out Requests",
            "Error Counts",
            "Status Codes",
        ]
        table.field_names = field_names

        for result in self.results:
            url = result["url"]
            method = result["methods"]
            if result["times"]:
                avg_time = sum(result["times"]) / len(result["times"])
                min_time = min(result["times"])
                max_time = max(result["times"])
            else:
                avg_time = min_time = max_time = "N/A"

            num_requests = len(result["times"])
            successful_responses = len(
                [code for code in result["status_codes"] if code is not None]
            )
            timed_out_requests = result["error_count"]
            status_codes = ", ".join(map(str, set(result["status_codes"])))
            error_counts = result["error_count"]

            # Adding a row for each result with the new details
            table.add_row(
                [
                    url,
                    method,
                    f"{avg_time:.2f}",
                    f"{min_time:.2f}",
                    f"{max_time:.2f}",
                    num_requests,
                    successful_responses,
                    timed_out_requests,
                    error_counts,
                    status_codes,
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
    parser.add_argument(
        "-d", "--delay", type=float, default=0, help="Delay between requests in seconds"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=10,
        help="Timeout for each requests in seconds",
    )
    parser.add_argument("-f", "--file", help="File containing URLs to test")
    parser.add_argument("-m", "--method", default="GET", help="HTTP method to use")
    parser.add_argument("--data", help="Data to send with the request")
    parser.add_argument(
        "--headers", nargs="+", help="Custom HTTP headers to set, format: key:value"
    )
    parser.add_argument(
        "--no-verify", action="store_false", help="Disable SSL certificate verification"
    )

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

    headers = (
        {k: v for k, v in (h.split(":") for h in args.headers)}
        if args.headers
        else None
    )

    if DEBUG:
        print(f"URLs: {urls}")

    tester = HTTPLoadTester(
        urls, args.num_requests, args.num_concurrent, DEBUG, args.delay, args.timeout
    )

    # Disabling SSL verification if no-verify flag is used
    tester.session.verify = args.no_verify

    tester.run(method=args.method, data=args.data, headers=headers)
    tester.print_results_summary()


if __name__ == "__main__":
    main()
