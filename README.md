# Book Recommendations System

A book recommendation system built using the Atomic Agents framework. This system provides personalized book recommendations based on user input, using a modular and maintainable architecture.

## Features

- 🤖 Built with Atomic Agents framework for predictable, maintainable AI
- 📚 Personalized book recommendations based on user preferences
- 🎯 Structured output with detailed book information
- 💾 Automatic saving of recommendations to JSON files
- 🖥️ Clean CLI interface with rich formatting

## Project Structure

```
book_recommendations_atomic/
├── src/
│   ├── schemas/         # Pydantic schemas for data validation
│   ├── agents/          # AI agents implementation
│   └── cli/            # Command-line interface
├── docs/               # Documentation
└── requirements.txt    # Project dependencies
```

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- `uv` package manager

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd book_recommendations_atomic
   ```

2. Install dependencies using `uv`:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   # Create a .env file with your API key
   echo "OPENAI_API_KEY=your-key-here" > .env
   ```

## Usage

Run the CLI interface:
```bash
python -m src.cli.main
```

The system will prompt you for input about what kind of book you're looking for. For example:
- "I want to read something about first contact with aliens"
- "Looking for a mystery novel set in Victorian London"
- "Need a book about personal growth and mindfulness"

The system will provide 3-5 personalized recommendations, including:
- Book title and author
- Genre
- Detailed description
- Specific reason why the book matches your request

Recommendations are automatically saved to JSON files for future reference.

## Development

The project uses the Atomic Agents framework, which emphasizes:
- Clear input/output schemas
- Modular components
- Predictable behavior
- Easy debugging

Key components:
- `BookRecommendationInput`: Defines the structure of user input
- `BookRecommendation`: Schema for individual book recommendations
- `BookRecommendationOutput`: Schema for the complete recommendation response
- `BookRecommendationAgent`: Core agent implementation using Atomic Agents

## Documentation

Additional documentation can be found in the `docs/` directory:
- `architecture.md`: System architecture and design decisions
- `book_agent_design.md`: Detailed agent implementation design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license information here]