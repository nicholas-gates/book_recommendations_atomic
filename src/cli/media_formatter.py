"""
Formatting utilities for cross-domain media recommendations.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..schemas.media_schemas import CrossDomainRecommendations

console = Console()

def format_movie_recommendation(movie: dict) -> Panel:
    """Format a movie recommendation for display."""
    title = Text(f"🎬 {movie['title']} ({movie['year']})", style="bold cyan")
    description = Text(f"\n{movie['description']}", style="white")
    reason = Text(f"\nWhy this movie: {movie['reason']}", style="green")

    content = Text.assemble(title, description, reason)
    return Panel(content, border_style="cyan", title="Movie Recommendation")

def format_game_recommendation(game: dict) -> Panel:
    """Format a game recommendation for display."""
    title = Text(f"🎮 {game['title']}", style="bold magenta")
    platform = Text(f"\nPlatform: {game['platform']}", style="italic")
    description = Text(f"\n{game['description']}", style="white")
    reason = Text(f"\nWhy this game: {game['reason']}", style="green")

    content = Text.assemble(title, platform, description, reason)
    return Panel(content, border_style="magenta", title="Game Recommendation")

def format_song_recommendation(song: dict) -> Panel:
    """Format a song recommendation for display."""
    title = Text(f"🎵 {song['title']}", style="bold yellow")
    artist = Text(f"\nby {song['artist']}", style="italic")
    description = Text(f"\n{song['description']}", style="white")
    reason = Text(f"\nWhy this song: {song['reason']}", style="green")

    content = Text.assemble(title, artist, description, reason)
    return Panel(content, border_style="yellow", title="Song Recommendation")

def format_media_recommendations(recommendations: CrossDomainRecommendations) -> list[Panel]:
    """
    Format all media recommendations for display.
    
    Args:
        recommendations (CrossDomainRecommendations): Media recommendations to format
    
    Returns:
        list[Panel]: List of formatted recommendation panels
    """
    # Convert Pydantic models to dictionaries
    movie_dict = recommendations.movie.model_dump()
    game_dict = recommendations.game.model_dump()
    song_dict = recommendations.song.model_dump()
    
    # Format each recommendation
    panels = [
        format_movie_recommendation(movie_dict),
        format_game_recommendation(game_dict),
        format_song_recommendation(song_dict)
    ]
    
    return panels
