"""
CLI interface for the book recommendation system.
Provides a simple command-line interface to interact with the book recommendation agent.
"""

import json
from typing import Dict, Any, List
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..agents.config import create_book_agent
from ..agents.media_agent import CrossDomainMediaAgent
from ..schemas.book_schemas import BookRecommendationInput
from ..schemas.media_schemas import CrossDomainMediaInput
from .media_formatter import format_media_recommendations

console = Console()

def format_book_recommendation(book: Dict[str, Any]) -> Panel:
    """
    Format a book recommendation for display.

    Args:
        book (Dict[str, Any]): Book recommendation data

    Returns:
        Panel: Formatted book panel
    """
    title = Text(f"📚 {book['title']}", style="bold cyan")
    author = Text(f"by {book['author']}", style="italic")
    genre = Text(f"Genre: {book['genre']}", style="magenta")
    description = Text(f"\n{book['description']}", style="white")
    reason = Text(f"\nWhy this book: {book['reason']}", style="green")

    content = Text.assemble(
        title, "\n", author, "\n", genre, description, reason
    )

    return Panel(content, border_style="cyan")

def select_book(recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Let the user select a book from the recommendations.
    
    Args:
        recommendations (List[Dict[str, Any]]): List of book recommendations
        
    Returns:
        Dict[str, Any]: Selected book data
    """
    console.print("\n[bold cyan]Select a book to get related media recommendations:[/bold cyan]")
    
    # Display numbered list of books
    for i, book in enumerate(recommendations, 1):
        console.print(f"\n[bold]{i}[/bold]. {book['title']} by {book['author']}")
    
    # Get user selection
    while True:
        try:
            choice = console.input("\n[bold green]Enter the number of your choice (or 'q' to quit): [/bold green]")
            
            if choice.lower() in ['q', 'quit', 'exit']:
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(recommendations):
                return recommendations[index]
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")

def get_media_recommendations(book_data: Dict[str, Any]) -> None:
    """
    Get and display cross-domain media recommendations for a book.
    
    Args:
        book_data (Dict[str, Any]): Selected book data
    """
    try:
        # Create media agent
        media_agent = CrossDomainMediaAgent()
        
        # Convert book data to input schema
        book_input = CrossDomainMediaInput(
            title=book_data['title'],
            author=book_data['author'],
            genre=book_data['genre'],
            description=book_data['description']
        )
        
        # Get recommendations
        console.print("\n[cyan]Finding related media recommendations...[/cyan]")
        recommendations = media_agent.run(book_input)
        
        # Display recommendations
        console.print("\n[bold cyan]Here are media recommendations based on your selected book:[/bold cyan]\n")
        panels = format_media_recommendations(recommendations)
        for panel in panels:
            console.print(panel)
            console.print()  # Add spacing between panels
        
        # Save recommendations to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"media_recommendations_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(recommendations.model_dump(), f, indent=2)
        console.print(f"[dim]Recommendations saved to {filename}[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]Error getting media recommendations: {str(e)}[/red]")

def main():
    """Main CLI interface for book recommendations."""
    try:
        # Set up the agent using the configuration module
        agent = create_book_agent()

        # Welcome message
        console.print("\n[bold cyan]Welcome to the Book Recommendation System![/bold cyan]")
        console.print("Share your thoughts on what you'd like to read, and I'll recommend some books.\n")

        while True:
            # Get user input
            thought = console.input("[bold green]What kind of book are you looking for? [/bold green]")

            if thought.lower() in ['quit', 'exit', 'q']:
                break

            console.print("\n[cyan]Thinking about your request...[/cyan]")

            try:
                # Get recommendations
                response = agent.run(BookRecommendationInput(thought=thought))

                # Display recommendations
                console.print("\n[bold cyan]Here are your personalized book recommendations:[/bold cyan]\n")

                # Convert Pydantic models to list of dicts for easier handling
                book_list = [book.model_dump() for book in response.recommendations]
                
                for book in book_list:
                    panel = format_book_recommendation(book)
                    console.print(panel)
                    console.print()  # Add spacing between recommendations

                # Save recommendations to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recommendations_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(response.model_dump(), f, indent=2)
                console.print(f"[dim]Recommendations saved to {filename}[/dim]\n")

                # Ask if user wants to get media recommendations
                console.print("\n[bold cyan]Would you like to get movie, game, and song recommendations based on one of these books?[/bold cyan]")
                if console.input("[bold green]Enter 'y' for yes, any other key to continue: [/bold green]").lower() == 'y':
                    selected_book = select_book(book_list)
                    if selected_book:
                        get_media_recommendations(selected_book)

            except Exception as e:
                console.print(f"[red]Error getting recommendations: {str(e)}[/red]")

            console.print("\nPress Enter to continue or type 'quit' to exit.")

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        return

    console.print("\n[yellow]Thank you for using the Book Recommendation System![/yellow]")

if __name__ == "__main__":
    main()
