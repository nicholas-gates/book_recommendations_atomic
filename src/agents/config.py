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
from .media_agent import CrossDomainMediaAgent

console = Console()

def _get_openai_client(api_key: Optional[str] = None) -> instructor.Instructor:
    """
    Create and configure an OpenAI client with instructor.
    
    Args:
        api_key (Optional[str]): OpenAI API key. If not provided, will attempt to load from environment.
    
    Returns:
        instructor.Instructor: Configured OpenAI client
        
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
    return client

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
    client = _get_openai_client(api_key)
    return BookRecommendationAgent(config=BaseAgentConfig(client=client))

def create_media_agent(api_key: Optional[str] = None) -> CrossDomainMediaAgent:
    """
    Create and configure a cross-domain media recommendation agent.
    
    Args:
        api_key (Optional[str]): OpenAI API key. If not provided, will attempt to load from environment.
    
    Returns:
        CrossDomainMediaAgent: Configured media recommendation agent
        
    Raises:
        SystemExit: If no API key is found
    """
    client = _get_openai_client(api_key)
    return CrossDomainMediaAgent(config=BaseAgentConfig(client=client))
