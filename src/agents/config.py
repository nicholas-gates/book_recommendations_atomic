"""
Configuration utilities for book recommendation agents.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
import instructor
from rich.console import Console

from atomic_agents.agents.base_agent import BaseAgentConfig
from .book_agent import BookRecommendationAgent

console = Console()

def create_book_agent(api_key: Optional[str] = None) -> BookRecommendationAgent:
    """
    Create and configure a book recommendation agent.
    
    Args:
        api_key (Optional[str]): OpenAI API key. If not provided, will attempt to load from environment.
    
    Returns:
        BookRecommendationAgent: Configured book recommendation agent
        
    Raises:
        SystemExit: If no API key is found
    """
    # Get API key from parameter or environment
    if not api_key:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
    if not api_key:
        console.print("[red]Error: OPENAI_API_KEY not provided and not found in environment[/red]")
        raise SystemExit(1)

    # Create instructor client
    client = instructor.from_openai(OpenAI(api_key=api_key))
    
    # Create and return the agent with the client
    return BookRecommendationAgent(config=BaseAgentConfig(client=client))
