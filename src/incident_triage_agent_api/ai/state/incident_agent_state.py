from typing_extensions import Optional, Dict
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated, List
from langgraph.graph.message import add_messages


class IncidentAgentState(TypedDict):
    messages : Annotated[List[AnyMessage], add_messages]
    parsed_logs : Optional[Dict]

    