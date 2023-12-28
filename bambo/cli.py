import argparse
from bambo.core import HTTPLoadTester

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
        import logging
        logging.basicConfig(level=logging.DEBUG)


    urls = []
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