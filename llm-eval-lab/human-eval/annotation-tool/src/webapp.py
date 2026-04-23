"""FastAPI web application for human annotation workflow."""

from __future__ import annotations

from collections import Counter  # Import Counter for rating-count mode detection in agreement prep.
from pathlib import Path  # Import Path for robust template directory resolution.

from fastapi import FastAPI, Form, HTTPException, Request  # Import FastAPI primitives for web routes and form handling.
from fastapi.responses import HTMLResponse, RedirectResponse  # Import HTML and redirect response classes.
from fastapi.templating import Jinja2Templates  # Import Jinja2 integration for server-rendered templates.

from src.db import add_annotation, get_item, init_db, list_annotations, list_items  # Import DB helpers for item and annotation storage.
from src.metrics import build_rating_matrix, fleiss_kappa  # Import agreement metric helpers.

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))  # Configure template directory relative to source file.


def _consistent_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """Keep only rows with the most common number of ratings."""

    if not matrix:  # Handle empty matrix input.
        return []  # Return empty matrix for downstream safe handling.
    row_sums = [sum(row) for row in matrix]  # Compute ratings-per-item counts for each matrix row.
    mode_sum = Counter(row_sums).most_common(1)[0][0]  # Determine most common ratings-per-item count.
    if mode_sum <= 1:  # Require at least two ratings per item for agreement reliability.
        return []  # Return empty matrix when insufficient annotations exist.
    return [row for row in matrix if sum(row) == mode_sum]  # Keep only rows matching modal rating count.


app = FastAPI(title="Annotation Tool", version="1.0.0")  # Create FastAPI app object.


@app.on_event("startup")
def startup() -> None:
    """Initialize database at startup."""

    init_db()  # Ensure tables and seed items exist before serving routes.


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    """Render item list page."""

    items = list_items()  # Fetch annotation items from database.
    annotations = list_annotations()  # Fetch existing annotations for count display.
    return templates.TemplateResponse(  # Render index template with item and annotation context.
        request=request,  # Pass request object to template engine.
        name="index.html",  # Use index template.
        context={"items": items, "annotation_count": len(annotations)},  # Provide template variables for rendering.
    )


@app.get("/annotate/{item_id}", response_class=HTMLResponse)
def annotate_form(item_id: int, request: Request) -> HTMLResponse:
    """Render annotation form for selected item."""

    item = get_item(item_id)  # Fetch target item by ID.
    if not item:  # Validate item existence before rendering form.
        raise HTTPException(status_code=404, detail="Item not found.")  # Return 404 for invalid item ID.
    return templates.TemplateResponse(  # Render annotation form template.
        request=request,  # Pass request object.
        name="annotate.html",  # Use annotate template.
        context={"item": item, "scores": [1, 2, 3, 4, 5]},  # Provide item and score options for form controls.
    )


@app.post("/annotate/{item_id}")
def annotate_submit(
    item_id: int,  # Receive item ID from route path.
    annotator: str = Form(...),  # Receive annotator name from form field.
    relevance: int = Form(...),  # Receive relevance rating from form field.
    accuracy: int = Form(...),  # Receive accuracy rating from form field.
    tone: int = Form(...),  # Receive tone rating from form field.
) -> RedirectResponse:
    """Store annotation and redirect back to item list."""

    item = get_item(item_id)  # Validate item existence before insert.
    if not item:  # Return not found when item ID is invalid.
        raise HTTPException(status_code=404, detail="Item not found.")  # Raise 404 error.
    if not annotator.strip():  # Validate annotator field for non-empty value.
        raise HTTPException(status_code=400, detail="Annotator name is required.")  # Raise clear form validation error.
    for value in (relevance, accuracy, tone):  # Validate each rubric score.
        if value < 1 or value > 5:  # Enforce rating range constraints.
            raise HTTPException(status_code=400, detail="Scores must be between 1 and 5.")  # Raise form validation error for invalid rating.
    add_annotation(item_id=item_id, annotator=annotator, relevance=relevance, accuracy=accuracy, tone=tone)  # Persist annotation record.
    return RedirectResponse(url="/", status_code=303)  # Redirect back to home page after successful submission.


@app.get("/results", response_class=HTMLResponse)
def results(request: Request) -> HTMLResponse:
    """Render results page with agreement metrics."""

    annotations = list_annotations()  # Fetch all annotation records.
    relevance_matrix = _consistent_matrix(build_rating_matrix(annotations, "relevance"))  # Build consistent rating matrix for relevance field.
    accuracy_matrix = _consistent_matrix(build_rating_matrix(annotations, "accuracy"))  # Build consistent rating matrix for accuracy field.
    tone_matrix = _consistent_matrix(build_rating_matrix(annotations, "tone"))  # Build consistent rating matrix for tone field.
    kappas = {  # Compute Fleiss' Kappa per rubric dimension.
        "relevance": fleiss_kappa(relevance_matrix),  # Compute relevance agreement score.
        "accuracy": fleiss_kappa(accuracy_matrix),  # Compute accuracy agreement score.
        "tone": fleiss_kappa(tone_matrix),  # Compute tone agreement score.
    }
    return templates.TemplateResponse(  # Render results template.
        request=request,  # Pass request object.
        name="results.html",  # Use results template.
        context={"annotations": annotations, "kappas": kappas},  # Provide annotations and kappa metrics.
    )
