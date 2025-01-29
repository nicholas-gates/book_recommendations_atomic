"""
Langsmith tracing utilities for the book recommendations system.
Provides context managers and utility functions for tracing LLM operations.
"""

from contextlib import contextmanager
from typing import Optional, Dict, Any, List
from datetime import datetime
import pytz

from langsmith import traceable
from langsmith.run_trees import RunTree
from langsmith import Client

client = Client()

@contextmanager
def trace_operation(
    name: str,
    run_type: str = "chain",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Context manager for tracing operations with Langsmith.
    
    Args:
        name: Name of the operation being traced
        run_type: Type of run (chain, llm, tool, etc)
        tags: Optional tags to attach to the trace
        metadata: Optional metadata to attach to the trace
    """
    # Convert dictionary tags to list format
    tag_list = []
    if tags:
        tag_list.extend(tags)
    
    # Add default tags
    tag_list.extend([
        "component:book_recommendations",
        "environment:development",
        f"timestamp:{datetime.now(pytz.UTC).isoformat()}"
    ])
        
    default_metadata = {
        "service": "book_recommendations_atomic"
    }
    
    if metadata:
        default_metadata.update(metadata)
    
    # Convert metadata to inputs format for Langsmith
    inputs = {"metadata": default_metadata}
    if metadata and "input_params" in metadata:
        inputs.update(metadata["input_params"])
    
    @traceable(
        run_type="chain",  # Always use chain as the base type
        name=name,
        tags=tag_list,
        metadata=default_metadata,
        inputs=inputs
    )
    def traced_operation():
        yield
        
    try:
        with traced_operation():
            yield
    except Exception as e:
        # Log the error in Langsmith
        client.create_run(
            name=f"{name}_error",
            run_type="chain",
            error=str(e),
            inputs=inputs,
            tags=tag_list,
            metadata=default_metadata
        )
        raise

def add_feedback(
    run_id: str,
    key: str,
    score: float,
    comment: Optional[str] = None
) -> None:
    """
    Add feedback to a traced run.
    
    Args:
        run_id: ID of the run to add feedback to
        key: Feedback key (e.g., 'relevance', 'quality')
        score: Numerical score for the feedback
        comment: Optional comment explaining the feedback
    """
    client.create_feedback(
        run_id,
        key=key,
        score=score,
        comment=comment
    )

def get_run_tree(run_id: str) -> RunTree:
    """
    Retrieve the run tree for a specific trace.
    
    Args:
        run_id: ID of the run to retrieve
        
    Returns:
        RunTree object containing the full trace information
    """
    return client.get_run_tree(run_id)
