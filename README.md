# :bamboo: Bamboo - HTTP(S) Load Tester

Welcome to **Bamboo**, a lightweight and efficient tool for performing load testing on your HTTP and HTTPS services. This Python-based command line utility assists in bombarding your web applications with requests, helping you gauge performance under stress.

## Features

- Custom number of requests
- Concurrent connections support
- Multiple URLs testing through file input
- Custom HTTP methods (GET, POST, PUT, DELETE, etc.)
- Data payload support for testing APIs
- Custom headers for each request
- Optional SSL certificate verification
- Detailed summary report using PrettyTable
- Ability to set timeouts for requests
- Ability to set delay between request

## Direct Installation (Pypi)

You can install **Bambo** directly from PyPI:

```bash
pip install bambo
```
Usage as a Library

```bash
# example.py
from bambo import HTTPLoadTester
tester = HTTPLoadTester(['http://example.com'], 5, 2)

# Start the test.
tester.run()
results = tester.results
print(results)
```

Usage:  bambo <--parameters>

```bash
bambo -u "https://example.com"
```
Find more details about the package here: [Bambo on PyPI](https://pypi.org/project/bambo/)


## Requirements

- Python 3.10 or higher
- Poetry (can be installed via curl)
- An internet connection

To install Poetry, run the following command in your terminal:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```


## Source Installation

Before running the tool, ensure you have Python installed on your system. You can then install the required packages using poetry:

```bash
poetry install
poetry shell
```

## Usage

To use Bamboo, simply invoke the script from the command line with the desired options.

```bash
python bambo/cli.py < --parameters >
```

### Basic Example

Test a single URL with the default number of requests (5):
```bash
python bambo/cli.py -u "https://example.com"
```
or
```
bambo -u "https://example.com"
```

### With Custom Number of Requests

Specify the number of requests to send:
```bash
python bambo/cli.py -u "https://example.com" -n 100
```

### Concurrent Requests

Set the number of concurrent requests:
```bash
python bambo/cli.py -u "https://example.com" -n 100 -c 10
```

### Testing Multiple URLs from File

You can test multiple URLs by providing a file (one URL per line):
```bash
python bambo/cli.py -f urls.txt
```

### Setting Custom Headers

Include custom headers with each request:
```bash
python bambo/cli.py -u "https://example.com" --headers "Authorization:Bearer YOUR_TOKEN" "Content-Type:application/json"
```

### Using Different HTTP Methods and Data Payload

Use different HTTP methods and send data:
```bash
python bambo/cli.py -u "https://api.example.com/data" -m POST --data '{"key":"value"}'
```

## Debugging

Enable debug output to get more details:
```bash
python bambo/cli.py -u "https://example.com" --debug
```

## Parameters Details

Here's a list of all parameters you can use:

Parameter | Description
--- | ---
-u, --url | URL to test (required if no file is provided)
-f, --file | File containing URLs to test (required if no URL is provided)
-n, --num-requests | Number of requests to make (default is 5)
-c, --num-concurrent | Number of concurrent requests (default is 1)
-d, --delay | Delay between requests in seconds
-t, --timeout | Timeout for each requests in seconds
-m, --method | HTTP method to use (default is GET)
--data | Data to send with the request
--headers | Custom HTTP headers to set, format: key:value
--no-verify | Disable SSL certificate verification
--debug | Enable DEBUG output

## Contribution

Feel free to fork this repository and contribute to the development of Bamboo! If you find bugs or would like to suggest features, please create an issue in the repository.

## License

Bamboo is released under the MIT License. Check out the LICENSE file for more information.

Enjoy testing your applications with **Bamboo**! 🚀
