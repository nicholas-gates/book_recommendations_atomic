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
from ..logging.logger import Logger

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
    Note: This is a simplified version that continues execution even if tracing fails.
    
    Args:
        name: Name of the operation being traced
        run_type: Type of run (chain, llm, tool, etc)
        tags: Optional tags to attach to the trace
        metadata: Optional metadata to attach to the trace
    """
    logger = Logger(__name__)
    
    try:
        # Prepare tags
        tag_list = tags or []
        tag_list.extend([
            "component:book_recommendations",
            "environment:development",
            f"timestamp:{datetime.now(pytz.UTC).isoformat()}"
        ])
        
        # Prepare metadata
        default_metadata = {"service": "book_recommendations_atomic"}
        if metadata:
            default_metadata.update(metadata)
            
        # Prepare inputs
        inputs = {"metadata": default_metadata}
        if metadata and "input_params" in metadata:
            inputs.update(metadata["input_params"])
        
        # Attempt to create run (returns None)
        try:
            client.create_run(
                name=name,
                run_type=run_type,
                tags=tag_list,
                metadata=default_metadata,
                inputs=inputs
            )
        except Exception as e:
            logger.log('error', f"Failed to create Langsmith run: {str(e)}", {
                'name': name,
                'run_type': run_type,
                'error': str(e)
            })
    except Exception as e:
        logger.log('error', f"Error preparing Langsmith trace: {str(e)}")
        
    try:
        # Always yield None since we don't have a run object
        yield None
    except Exception as e:
        # Log but don't prevent the error from propagating
        logger.log('error', f"Error in traced operation: {str(e)}")
        raise

def add_feedback(
    run_id: str,
    key: str,
    score: float,
    comment: Optional[str] = None
):
    """
    Add feedback to a traced run.
    
    Args:
        run_id: ID of the run to add feedback to
        key: Feedback key (e.g., 'relevance', 'quality')
        score: Numerical score for the feedback
        comment: Optional comment explaining the feedback
    """
    try:
        client.create_feedback(
            run_id,
            key=key,
            score=score,
            comment=comment
        )
    except Exception as e:
        logger = Logger(__name__)
        logger.log('error', f"Failed to add feedback: {str(e)}", {
            'run_id': run_id,
            'key': key,
            'score': score
        })

def get_run_tree(run_id: str) -> RunTree:
    """
    Retrieve the run tree for a specific trace.
    
    Args:
        run_id: ID of the run to retrieve
        
    Returns:
        RunTree object containing the full trace information
    """
    return client.get_run_tree(run_id)
