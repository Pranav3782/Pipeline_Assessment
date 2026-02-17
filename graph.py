from typing import TypedDict, Dict, List, Any
from langgraph.graph import StateGraph
from agents import segregate, extract_id, extract_discharge, extract_bill


class State(TypedDict):
    pages: Dict[int, str]
    assigned: Dict[str, List[str]]
    id_data: Any
    discharge_data: Any
    bill_data: Any


# ---------------- SEGREGATOR ----------------

def segregator_node(state: State):
    routes = segregate(state["pages"])

    assigned = {}
    for doc_type, nums in routes.items():
        assigned[doc_type] = [
            state["pages"][n] for n in nums if n in state["pages"]
        ]

    return {"assigned": assigned}


# ---------------- ID AGENT ----------------

def id_node(state: State):
    pages = state["assigned"].get("identity_document", [])

    if not pages:
        return {"id_data": {}}

    text = "\n".join(pages)
    return {"id_data": extract_id(text)}


# ---------------- DISCHARGE AGENT ----------------

def discharge_node(state: State):
    pages = state["assigned"].get("discharge_summary", [])

    if not pages:
        return {"discharge_data": {}}

    text = "\n".join(pages)
    return {"discharge_data": extract_discharge(text)}


# ---------------- BILL AGENT ----------------

def bill_node(state: State):
    pages = state["assigned"].get("itemized_bill", [])

    if not pages:
        return {"bill_data": {}}

    text = "\n".join(pages)
    return {"bill_data": extract_bill(text)}


# ---------------- AGGREGATOR ----------------

def aggregator_node(state: State):
    return {
        "identity": state.get("id_data", {}),
        "discharge": state.get("discharge_data", {}),
        "bill": state.get("bill_data", {})
    }


# ---------------- GRAPH ----------------

def build_graph():
    graph = StateGraph(State)

    graph.add_node("segregator", segregator_node)
    graph.add_node("id_agent", id_node)
    graph.add_node("discharge_agent", discharge_node)
    graph.add_node("bill_agent", bill_node)
    graph.add_node("aggregator", aggregator_node)

    graph.set_entry_point("segregator")

    graph.add_edge("segregator", "id_agent")
    graph.add_edge("segregator", "discharge_agent")
    graph.add_edge("segregator", "bill_agent")

    graph.add_edge("id_agent", "aggregator")
    graph.add_edge("discharge_agent", "aggregator")
    graph.add_edge("bill_agent", "aggregator")

    graph.set_finish_point("aggregator")

    return graph.compile()
