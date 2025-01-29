"""
Schemas for cross-domain media recommendations.
"""

from atomic_agents.agents.base_agent import BaseIOSchema

class CrossDomainMediaInput(BaseIOSchema):
    """Schema for input book data to cross-domain media agent."""
    title: str
    author: str
    genre: str
    description: str

class MovieRecommendation(BaseIOSchema):
    """Schema for movie recommendations."""
    title: str
    year: str
    description: str
    reason: str

class GameRecommendation(BaseIOSchema):
    """Schema for game recommendations."""
    title: str
    platform: str
    description: str
    reason: str

class SongRecommendation(BaseIOSchema):
    """Schema for song recommendations."""
    title: str
    artist: str
    description: str
    reason: str

class CrossDomainMediaOutput(BaseIOSchema):
    """Schema for combined cross-domain recommendations."""
    movie: MovieRecommendation
    game: GameRecommendation
    song: SongRecommendation
