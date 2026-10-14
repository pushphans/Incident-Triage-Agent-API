from tenacity import retry_if_exception, stop_after_attempt, wait_exponential, retry
from urllib.error import HTTPError, URLError




def should_retry(error):
    if isinstance(error, HTTPError):
        return error.code(429, 500, 502, 503, 504)

    return isinstance(error, (URLError, TimeoutError))



