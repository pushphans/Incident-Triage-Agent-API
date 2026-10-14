from fastapi import status
from fastapi import HTTPException
from langchain.tools import tool, ToolRuntime
from incident_triage_agent_api.services.data_service import execute_interpret_logs, execute_lookup_runbook, execute_get_service_metadata, execute_search_web


# @tool
# def interpret_logs(log_text : str) -> dict:
#     """Extract errors, warnings and exceptions from application logs."""

#     result = interpret_logs(log_text)

#     return result


@tool
def lookup_runbook(error_type : str) -> dict:
    """Find troubleshooting guidance for a known exception type."""
    
    result = execute_lookup_runbook(error_type)

    return result



@tool
def get_service_metadata(service_name : str) -> dict:
    """Look up configured demo service metadata by service name."""

    result = execute_get_service_metadata(service_name)

    return result


@tool
def search_web(query : str) -> dict:
    """Search the web for incident troubleshooting guidance via Tavily."""

    try:
        result = execute_search_web(query)

        return result

    except ValueError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid request"
        )

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )



tool_list = [lookup_runbook, get_service_metadata, search_web]