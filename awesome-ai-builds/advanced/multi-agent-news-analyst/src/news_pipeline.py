"""News retrieval and multi-agent briefing orchestration."""

from __future__ import annotations

import os  # Import os to read Serper API key from environment variables.
from dataclasses import dataclass  # Import dataclass to structure agent outputs cleanly.
from typing import Callable  # Import Callable for dependency injection in tests.

import requests  # Import requests for Serper HTTP API calls.
from dotenv import load_dotenv  # Import dotenv for local environment variable loading.

from llm import generate_text  # Import local provider adapter for all agent LLM calls.

load_dotenv()  # Load environment variables from `.env` before runtime operations.


@dataclass
class AgentOutputs:
    """Container for each role's output and source metadata."""

    researcher_notes: str  # Raw fact-focused output from researcher role.
    analyst_notes: str  # Trend/implication analysis from analyst role.
    briefing: str  # Final polished briefing from writer role.
    sources: list[dict]  # Structured source list from retrieval layer.


def serper_search(topic: str, max_results: int = 6) -> list[dict]:
    """Fetch topic-specific web results using Serper."""

    api_key = os.getenv("SERPER_API_KEY", "").strip()  # Read Serper key from environment.
    if not api_key:  # Validate key before HTTP request.
        raise ValueError("Missing SERPER_API_KEY. Add it to your .env file.")  # Raise clear setup guidance.
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}  # Build required Serper auth and content headers.
    payload = {"q": topic, "num": max_results}  # Build query payload with topic and desired result count.
    response = requests.post("https://google.serper.dev/search", headers=headers, json=payload, timeout=30)  # Execute API request with timeout guard.
    response.raise_for_status()  # Raise explicit HTTP errors for easier troubleshooting.
    organic = response.json().get("organic", [])  # Extract organic result list from Serper response payload.
    normalized: list[dict] = []  # Create normalized result structure for downstream prompts and storage.
    for item in organic:  # Iterate over each organic result record.
        normalized.append(  # Append cleaned result object with only needed fields.
            {
                "title": str(item.get("title", "")).strip(),  # Keep source title for readability.
                "link": str(item.get("link", "")).strip(),  # Keep canonical source link for citations.
                "snippet": str(item.get("snippet", "")).strip(),  # Keep short snippet for evidence context.
            }
        )
    return normalized  # Return normalized search results.


def _sources_as_text(sources: list[dict]) -> str:
    """Format source list into compact text block for prompts."""

    if not sources:  # Handle empty source list explicitly.
        return "No sources found."  # Return fallback evidence string.
    lines: list[str] = []  # Build deterministic line list for prompt clarity.
    for idx, source in enumerate(sources, start=1):  # Enumerate sources with 1-based ordering.
        lines.append(f"{idx}. {source['title']} | {source['link']} | {source['snippet']}")  # Serialize source fields into one line.
    return "\n".join(lines)  # Join lines into prompt-ready evidence block.


def run_multi_agent_pipeline(topic: str, sources: list[dict], generate_fn: Callable[..., str] | None = None) -> AgentOutputs:
    """Run Researcher -> Analyst -> Writer workflow with CrewAI or fallback prompts."""

    if not topic.strip():  # Validate topic before running pipeline.
        raise ValueError("Topic cannot be empty.")  # Raise clear input validation message.
    generator = generate_fn or generate_text  # Resolve generator implementation with optional injection for tests.
    sources_block = _sources_as_text(sources)  # Convert source list into prompt-ready evidence text.

    try:  # Attempt CrewAI orchestration path first.
        from crewai import Agent, Crew, Task  # Import CrewAI classes lazily to keep module import lightweight.

        researcher = Agent(  # Define researcher role focused on extracting verified facts.
            role="Researcher",  # Name role for task clarity.
            goal="Gather factual updates and evidence from sources.",  # Define role objective.
            backstory="You extract concrete, verifiable facts and preserve source links.",  # Provide behavioral guidance.
            verbose=False,  # Keep run output clean in production mode.
        )
        analyst = Agent(  # Define analyst role focused on interpretation and trends.
            role="Analyst",  # Name role for trend analysis.
            goal="Identify trends, conflicts, and implications.",  # Define analytical objective.
            backstory="You compare evidence and highlight strategic meaning.",  # Provide analysis-oriented persona.
            verbose=False,  # Keep logs concise.
        )
        writer = Agent(  # Define writer role focused on polished briefing output.
            role="Writer",  # Name writer role.
            goal="Produce a concise daily briefing for builders.",  # Define writing objective.
            backstory="You transform analysis into actionable, readable briefings.",  # Provide output-quality guidance.
            verbose=False,  # Keep logs concise.
        )

        research_task = Task(  # Build task where researcher extracts key facts.
            description=f"Topic: {topic}\nSources:\n{sources_block}\nReturn factual bullet points with source references.",  # Provide task context and expected output.
            expected_output="Bullet list of verified facts with source links.",  # Define expected output contract.
            agent=researcher,  # Assign task to researcher role.
        )
        analysis_task = Task(  # Build task where analyst interprets researcher output.
            description=f"Topic: {topic}\nUsing researcher findings, identify trends, risks, and unknowns.",  # Provide analysis instructions.
            expected_output="Structured trend analysis with risks and unknowns.",  # Define expected analysis artifact.
            agent=analyst,  # Assign task to analyst role.
            context=[research_task],  # Provide researcher task output as analyst context.
        )
        writing_task = Task(  # Build task where writer composes final briefing.
            description=f"Topic: {topic}\nCreate a daily briefing with sections: Summary, Trends, Risks, Sources.",  # Provide final briefing structure instructions.
            expected_output="Markdown daily briefing with citations.",  # Define writer output contract.
            agent=writer,  # Assign task to writer role.
            context=[research_task, analysis_task],  # Provide researcher and analyst outputs to writer.
        )

        crew = Crew(agents=[researcher, analyst, writer], tasks=[research_task, analysis_task, writing_task], verbose=False)  # Assemble multi-agent crew and task chain.
        result = crew.kickoff()  # Execute CrewAI task graph and collect final output.
        briefing = str(result).strip()  # Normalize final output into string for persistence and display.
        researcher_notes = str(getattr(research_task, "output", "") or "").strip()  # Extract researcher task output when available.
        analyst_notes = str(getattr(analysis_task, "output", "") or "").strip()  # Extract analyst task output when available.
        if not researcher_notes:  # Backfill researcher notes if task output object is unavailable.
            researcher_notes = "Research notes were produced inside CrewAI execution context."  # Preserve non-empty field for storage consistency.
        if not analyst_notes:  # Backfill analyst notes if task output object is unavailable.
            analyst_notes = "Analysis notes were produced inside CrewAI execution context."  # Preserve non-empty field for storage consistency.
        return AgentOutputs(  # Return role outputs and source metadata in typed container.
            researcher_notes=researcher_notes,  # Include researcher output text.
            analyst_notes=analyst_notes,  # Include analyst output text.
            briefing=briefing,  # Include final writer briefing.
            sources=sources,  # Include source metadata for storage and UI.
        )
    except Exception:  # Use robust fallback path if CrewAI import/runtime fails.
        researcher_notes = generator(  # Run researcher role as direct prompt call.
            prompt=(  # Build researcher prompt from topic and sources.
                f"Topic: {topic}\n"  # Include target topic for context.
                f"Sources:\n{sources_block}\n"  # Include source evidence text.
                "Extract key verified facts as bullet points with source URLs."  # Define exact expected output style.
            ),
            system_prompt="You are a meticulous researcher.",  # Set role persona for evidence-first behavior.
            temperature=0.1,  # Keep deterministic output for fact extraction.
            max_tokens=700,  # Allow sufficient room for evidence bullets.
        )
        analyst_notes = generator(  # Run analyst role as second prompt call.
            prompt=(  # Build analyst prompt using researcher notes as input context.
                f"Topic: {topic}\n"  # Include shared topic context.
                f"Research Notes:\n{researcher_notes}\n"  # Include extracted facts from prior step.
                "Analyze trends, implications, and unknowns in bullet points."  # Define required analytical perspective.
            ),
            system_prompt="You are a strategic analyst.",  # Set analyst persona.
            temperature=0.2,  # Allow modest reasoning diversity while staying consistent.
            max_tokens=800,  # Allow space for structured analysis.
        )
        briefing = generator(  # Run writer role as final prompt call.
            prompt=(  # Build writer prompt from analyst and researcher notes.
                f"Topic: {topic}\n"  # Include shared topic context.
                f"Research Notes:\n{researcher_notes}\n\n"  # Provide factual base.
                f"Analysis Notes:\n{analyst_notes}\n\n"  # Provide trend interpretation.
                "Write a daily briefing with sections: Executive Summary, Trend Signals, Risks, Sources."  # Define final document structure.
            ),
            system_prompt="You are an executive briefing writer.",  # Set writer persona for concise polished output.
            temperature=0.3,  # Allow moderate stylistic variation for readability.
            max_tokens=1000,  # Allow enough tokens for complete sectioned briefing.
        )
        return AgentOutputs(  # Return fallback outputs in same structure as CrewAI path.
            researcher_notes=researcher_notes,  # Include extracted facts.
            analyst_notes=analyst_notes,  # Include trend analysis.
            briefing=briefing,  # Include final briefing.
            sources=sources,  # Include source metadata.
        )
