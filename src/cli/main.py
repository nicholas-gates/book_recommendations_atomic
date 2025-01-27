"""
CLI interface for the book recommendation system.
Provides a simple command-line interface to interact with the book recommendation agent.
"""

import os
import json
from typing import Dict, Any
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

from ..agents.config import create_book_agent
from ..schemas.book_schemas import BookRecommendationInput

load_dotenv()

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

                for book in response.recommendations:
                    # Convert Pydantic model to dict for formatting
                    book_dict = book.model_dump()
                    panel = format_book_recommendation(book_dict)
                    console.print(panel)
                    console.print()  # Add spacing between recommendations

                # Save recommendations to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recommendations_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(response.model_dump(), f, indent=2)
                console.print(f"[dim]Recommendations saved to {filename}[/dim]\n")

            except Exception as e:
                console.print(f"[red]Error getting recommendations: {str(e)}[/red]")

            console.print("\nPress Enter to continue or type 'quit' to exit.")

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        return

    console.print("\n[yellow]Thank you for using the Book Recommendation System![/yellow]")

if __name__ == "__main__":
    main()
