"""
Book recommendation schemas for the Atomic Agents implementation.
These schemas define the structure for book recommendation requests and responses.
"""

from typing import List
from pydantic import Field
from atomic_agents.agents.base_agent import BaseIOSchema


class BookRecommendationInput(BaseIOSchema):
    """
    Input schema for book recommendations.
    
    Attributes:
        thought (str): User's thought or direction about what they want to read.
            This can include preferences about genres, themes, writing styles,
            or specific topics of interest.
    """
    thought: str = Field(
        ...,
        description="User's thought or direction about what they want to read",
        min_length=3,
        examples=[
            "I want to read something about first contact with aliens",
            "Looking for a mystery novel set in Victorian London",
            "Need a book about personal growth and mindfulness"
        ]
    )


class BookRecommendation(BaseIOSchema):
    """
    Schema for an individual book recommendation.
    
    Attributes:
        title (str): The book's title
        author (str): The book's author
        genre (str): The primary genre of the book
        description (str): A detailed description of the book
        reason (str): Specific reason why this book matches the user's request
    """
    title: str = Field(
        ...,
        description="Book title",
        min_length=1
    )
    author: str = Field(
        ...,
        description="Book author",
        min_length=1
    )
    genre: str = Field(
        ...,
        description="Book genre",
        min_length=1
    )
    description: str = Field(
        ...,
        description="Detailed book description",
        min_length=50,  # Ensure descriptions are reasonably detailed
        max_length=1000  # Prevent overly long descriptions
    )
    reason: str = Field(
        ...,
        description="Specific reason why this book matches the request",
        min_length=20,  # Ensure reasons are meaningful
        max_length=500  # Keep reasons concise
    )


class BookRecommendationOutput(BaseIOSchema):
    """
    Output schema for book recommendations.
    
    Attributes:
        recommendations (List[BookRecommendation]): List of book recommendations,
            containing between 3 and 5 recommendations.
    """
    recommendations: List[BookRecommendation] = Field(
        ...,
        description="List of book recommendations",
        min_items=3,
        max_items=5
    )
