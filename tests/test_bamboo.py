import pytest
from unittest.mock import patch, Mock
from bambo import HTTPLoadTester


@pytest.fixture
def load_tester():
    urls = ["https://example.com"]
    num_requests = 2
    num_concurrent = 1
    return HTTPLoadTester(urls, num_requests, num_concurrent)


def test_make_request(load_tester):
    # Assuming make_request is a part of the HTTPLoadTester class
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.elapsed.total_seconds.return_value = 0.1

    with patch("requests.Session.request", return_value=response_mock) as mock_request:
        result = load_tester.make_request("https://example.com")

        assert len(result["times"]) == load_tester.num_requests
        assert all(code == 200 for code in result["status_codes"])
        assert result["error_count"] == 0
        mock_request.assert_called_with(
            "GET",
            "https://example.com",
            data=None,
            headers=None,
            timeout=load_tester.timeout,
        )


def test_run(load_tester):
    # Mocking make_request method to ensure no actual HTTP calls are made.
    with patch.object(load_tester, "make_request") as mock_make_request:
        fake_result = {
            "url": "https://example.com",
            "methods": "GET",
            "times": [0.1, 0.2],
            "status_codes": [200, 200],
            "error_count": 0,
        }
        mock_make_request.return_value = fake_result

        load_tester.run()

        assert len(load_tester.results) == 1
        assert load_tester.results[0] == fake_result


# Example test case for checking handling of different status codes
@pytest.mark.parametrize("status_code, success_count", [(200, 2), (404, 0)])
def test_make_request_various_status_codes(load_tester, status_code, success_count):
    response_mock = Mock()
    response_mock.status_code = status_code
    response_mock.elapsed.total_seconds.return_value = 0.1

    with patch("requests.Session.request", return_value=response_mock):
        result = load_tester.make_request("https://example.com")

        successful_responses = len(
            [code for code in result["status_codes"] if code == 200]
        )
        assert successful_responses == success_count
