from tenacity import wait_exponential
from tenacity import stop_after_attempt
from tenacity import retry_if_exception
from incident_triage_agent_api.utils.retrier import should_retry
from tenacity import retry
import re
from pathlib import Path
import json
from urllib.request import Request, urlopen

from incident_triage_agent_api.core.config import settings



def execute_interpret_logs(log_text : str) -> dict:

    lines = log_text.splitlines()

    errors = []
    warnings = []
    exceptions = []

    for line in lines:
        if re.search(r"\b(ERROR|CRITICAL)\b", line, re.I):
            errors.append(line)

        elif re.search(r"\bWARNING\b", line, re.I):
            warnings.append(line)

        if re.search(r"\b[A-Za-z_]\w*(?:Error|Exception)\b", line):
            exceptions.append(line)

    return {
        "total_lines" : len(lines),
        "errors" : errors,
        "warnings" : warnings,
        "exceptions" : exceptions
    }



def execute_lookup_runbook(error_type : str) -> dict:

    file_path = Path(__file__).parent.parent/ "data" / "runbooks.json"

    with open(file_path, "r", encoding="utf-8") as json_file:
        runbooks = json.load(json_file)
        

    result = runbooks.get(error_type)

    if result is None:
        return {
            "found" : False,
            "message" : "No runbook found"
        }


    return {
        "found" : True,
        "runbook" : result
    }



def execute_get_service_metadata(service_name : str) -> dict:

    file_path = Path(__file__).parent.parent / "data" / "services.json"

    with open(file_path, "r", encoding="utf-8") as file:
        services = json.load(file)

    service_metadata = services.get(service_name)


    if service_metadata is None:
        return {
            "found" : False,
            "message" : "No service found"
        }

    

    return {
        "found" : True,
        "service" : service_name,
        "service_metadata" : service_metadata
    }



@retry(
    retry=retry_if_exception(should_retry),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min = 1, max = 4),
    reraise=True
)
def execute_search_web(query : str) -> dict:
    if not query.strip():
        raise ValueError("Search query cannot be empty")

    request = Request(
        "https://api.tavily.com/search",
        data=json.dumps({
            "query": query,
            "search_depth": "basic",
            "max_results": 5,
            "include_raw_content": False,
        }).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.TAVILY_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(request, timeout=15) as response:
        search_results = json.load(response)

    return {
        "query": query,
        "results": [
            {
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
            }
            for result in search_results["results"]
        ],
    }





