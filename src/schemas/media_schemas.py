"""
Schemas for cross-domain media recommendations.
"""

from pydantic import BaseModel

class MovieRecommendation(BaseModel):
    """Schema for movie recommendations."""
    title: str
    year: str
    description: str
    reason: str

class GameRecommendation(BaseModel):
    """Schema for game recommendations."""
    title: str
    platform: str
    description: str
    reason: str

class SongRecommendation(BaseModel):
    """Schema for song recommendations."""
    title: str
    artist: str
    description: str
    reason: str

class CrossDomainRecommendations(BaseModel):
    """Schema for combined cross-domain recommendations."""
    movie: MovieRecommendation
    game: GameRecommendation
    song: SongRecommendation
