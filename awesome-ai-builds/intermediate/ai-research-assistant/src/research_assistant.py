"""Research workflow with Tavily search and LangGraph state orchestration."""

from __future__ import annotations

import os  # Import os to access Tavily API key configuration.
from typing import Callable, TypedDict  # Import TypedDict for explicit state shape and Callable for dependency injection.

import requests  # Import requests for HTTP calls to Tavily API.
from dotenv import load_dotenv  # Import dotenv to load API keys from local .env file.

from llm import generate_text  # Import local provider adapter to keep model SDK usage isolated.

load_dotenv()  # Load environment values before Tavily and provider calls.


class ResearchState(TypedDict):
    """State object passed between workflow nodes."""

    question: str  # User's research question that drives search and synthesis.
    search_results: list[dict]  # Tavily search result objects used as evidence.
    summary: str  # Final structured summary generated from evidence.
    sources: list[str]  # Extracted source URLs for citation display.


def tavily_search(question: str, max_results: int = 5) -> list[dict]:
    """Search the web using Tavily API and return normalized result objects."""

    api_key = os.getenv("TAVILY_API_KEY", "").strip()  # Read Tavily key from environment variables.
    if not api_key:  # Validate API key presence before network request.
        raise ValueError("Missing TAVILY_API_KEY. Add it to your .env file.")  # Raise actionable setup message.
    payload = {  # Build request payload with clear defaults for research context.
        "api_key": api_key,  # Provide Tavily authentication key.
        "query": question,  # Send user research question as search query.
        "max_results": max_results,  # Limit result count to keep synthesis focused.
        "search_depth": "advanced",  # Request richer search output for better evidence quality.
    }
    response = requests.post("https://api.tavily.com/search", json=payload, timeout=30)  # Execute HTTP POST request with timeout protection.
    response.raise_for_status()  # Raise HTTP errors explicitly so failures are visible to users.
    raw_results = response.json().get("results", [])  # Extract raw results array from API response JSON.
    normalized: list[dict] = []  # Build normalized result structure for downstream prompt assembly.
    for item in raw_results:  # Iterate over returned result objects in API-provided order.
        normalized.append(  # Append cleaned search result object with only fields we need.
            {
                "title": str(item.get("title", "")).strip(),  # Keep result title for source readability.
                "url": str(item.get("url", "")).strip(),  # Keep canonical source URL for citations.
                "content": str(item.get("content", "")).strip(),  # Keep snippet content for evidence grounding.
            }
        )
    return normalized  # Return normalized list for graph state transitions.


def format_search_results(results: list[dict]) -> str:
    """Convert search results into compact evidence text for prompting."""

    if not results:  # Handle empty result set explicitly for transparent synthesis behavior.
        return "No search results were found."  # Return fallback evidence text.
    lines: list[str] = []  # Collect formatted evidence lines in a deterministic order.
    for idx, item in enumerate(results, start=1):  # Enumerate each result with stable numbering.
        lines.append(  # Append one line containing title, URL, and snippet for each source.
            f"{idx}. {item.get('title', 'Untitled')} | {item.get('url', 'No URL')} | {item.get('content', '')}"
        )
    return "\n".join(lines)  # Join lines into final evidence block string.


def build_synthesis_prompt(question: str, results: list[dict]) -> str:
    """Create synthesis prompt with explicit structure and citation requirement."""

    evidence = format_search_results(results)  # Format retrieved web results into concise evidence text.
    return (  # Return final synthesis prompt for LLM call.
        "You are a research assistant.\n"  # Set role to analysis-focused assistant.
        "Use only the evidence provided.\n"  # Force groundedness and reduce unsupported claims.
        "Return markdown with sections:\n"  # Specify deterministic output structure.
        "1) Executive Summary\n"  # Require concise high-level synthesis.
        "2) Key Findings\n"  # Require bulletized major insights.
        "3) Risks and Unknowns\n"  # Require uncertainty framing.
        "4) Sources\n"  # Require explicit citation section.
        "Include source URLs in the Sources section.\n\n"  # Reinforce citation behavior.
        f"Research Question:\n{question}\n\n"  # Inject user research question.
        f"Evidence:\n{evidence}"  # Inject normalized evidence block.
    )


def _search_node(state: ResearchState, search_fn: Callable[[str], list[dict]]) -> ResearchState:
    """Graph node that executes web search."""

    results = search_fn(state["question"])  # Execute injected search function for testability and modularity.
    sources = [item.get("url", "") for item in results if item.get("url")]  # Extract non-empty URLs for explicit citation output.
    return {  # Return updated state with search outputs.
        **state,  # Preserve existing state keys unchanged.
        "search_results": results,  # Attach normalized result objects.
        "sources": sources,  # Attach URL list for UI display.
    }


def _synthesis_node(state: ResearchState, generate_fn: Callable[..., str]) -> ResearchState:
    """Graph node that synthesizes search evidence into a report."""

    prompt = build_synthesis_prompt(state["question"], state["search_results"])  # Build structured prompt from state fields.
    summary = generate_fn(  # Call model adapter through injected function for testability.
        prompt=prompt,  # Send structured synthesis prompt.
        system_prompt="You are factual, concise, and cite your sources clearly.",  # Reinforce grounded summarization behavior.
        temperature=0.2,  # Keep stochasticity low for consistent report format.
        max_tokens=900,  # Allow enough room for full structured output sections.
    )
    return {**state, "summary": summary}  # Return state with synthesized summary text.


def run_research(question: str, search_fn: Callable[[str], list[dict]] | None = None, generate_fn: Callable[..., str] | None = None) -> ResearchState:
    """Run the full research workflow with LangGraph when available."""

    if not question.strip():  # Validate input question before workflow execution.
        raise ValueError("Research question cannot be empty.")  # Raise clear validation guidance for UI.
    search_impl = search_fn or tavily_search  # Resolve search implementation with optional test injection.
    generate_impl = generate_fn or generate_text  # Resolve text generation implementation with optional test injection.
    initial_state: ResearchState = {  # Create initial state object for graph execution.
        "question": question.strip(),  # Store normalized question text.
        "search_results": [],  # Initialize empty result list before search node executes.
        "summary": "",  # Initialize empty summary before synthesis node executes.
        "sources": [],  # Initialize empty sources before extraction.
    }

    try:  # Attempt LangGraph execution path first to teach graph-based orchestration.
        from langgraph.graph import END, StateGraph  # Import LangGraph graph primitives lazily.

        workflow = StateGraph(ResearchState)  # Create typed state graph for workflow definition.
        workflow.add_node("search", lambda state: _search_node(state, search_impl))  # Add search node that populates evidence and sources.
        workflow.add_node("synthesize", lambda state: _synthesis_node(state, generate_impl))  # Add synthesis node that writes final summary.
        workflow.set_entry_point("search")  # Start workflow with web search step.
        workflow.add_edge("search", "synthesize")  # Route search output into synthesis node.
        workflow.add_edge("synthesize", END)  # Terminate workflow after synthesis completes.
        graph = workflow.compile()  # Compile graph into executable runtime object.
        return graph.invoke(initial_state)  # Run graph and return final state dictionary.
    except ImportError:  # Provide deterministic fallback when LangGraph is not installed.
        searched = _search_node(initial_state, search_impl)  # Execute search node directly in linear fallback flow.
        return _synthesis_node(searched, generate_impl)  # Execute synthesis node and return final state.
