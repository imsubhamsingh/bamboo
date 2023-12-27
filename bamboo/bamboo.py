import argparse
import concurrent.futures
import time
import requests
from prettytable import PrettyTable


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
        table = PrettyTable()
        
        # Updating field names to include more details
        field_names = [
            "URL",
            "Average Time (s)",
            "Min Time (s)",
            "Max Time (s)",
            "Requests",
            "Status Codes",
            "Error Counts"
        ]
        table.field_names = field_names
        
        for result in self.results:
            url = result["url"]
            times = [d["total_time"] for d in result["times"]]
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            num_requests = len(times)
            status_codes = ', '.join(map(str, set(result["status_codes"])))
            
            # Counting errors
            error_counts = result.get("errors", {}).get("count", 0)

            # Adding a row for each result with the new details
            table.add_row([
                url,
                f"{avg_time:.2f}",
                f"{min_time:.2f}",
                f"{max_time:.2f}",
                num_requests,
                status_codes,
                error_counts
            ])
            
        # Printing the table with added details
        print(table)


def main():
    parser = argparse.ArgumentParser(description="Bamboo - HTTP(S) Load Tester")
    parser.add_argument("-u", "--url", help="URL to test")
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
    print(args)

    if args.url:
        urls = [args.url]
    elif args.file:
        with open(args.file, "r") as file:
            urls = file.read().splitlines()
            print(urls)
    else:
        print("Please provide a URL or a file containing URLs.")
        return

    tester = HTTPLoadTester(urls, args.num_requests, args.num_concurrent)
    tester.run()
    tester.print_results_summary()


if __name__ == "__main__":
    main()
