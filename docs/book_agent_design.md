# Book Recommendation Agent Design

## Overview
This document outlines the design for the initial book recommendation agent using the Atomic Agents framework. The agent will provide book recommendations based on user input through a CLI interface.

## Component Design

### 1. Schema Definitions

#### Input Schema
```python
class BookRecommendationInput(BaseIOSchema):
    thought: str = Field(
        ..., 
        description="User's thought or direction about what they want to read"
    )
```

#### Output Schema
```python
class BookRecommendation(BaseIOSchema):
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Book author")
    genre: str = Field(..., description="Book genre")
    description: str = Field(..., description="Detailed book description")
    reason: str = Field(..., description="Specific reason why this book matches the request")

class BookRecommendationOutput(BaseIOSchema):
    recommendations: List[BookRecommendation] = Field(
        ..., 
        description="List of book recommendations",
        min_items=3,
        max_items=5
    )
```

### 2. System Prompt Design
The system prompt will be structured using the Atomic Agents' SystemPromptGenerator:

```python
system_prompt_generator = SystemPromptGenerator(
    background=[
        "You are an expert librarian and book recommender.",
        "Your goal is to provide thoughtful, personalized book recommendations.",
        "You have extensive knowledge of literature across all genres and periods."
    ],
    steps=[
        "1. Analyze the user's reading interests from their input",
        "2. Consider both popular and lesser-known books that match",
        "3. Ensure recommendations are diverse within the user's interests",
        "4. Generate detailed, accurate descriptions",
        "5. Provide specific reasons why each book matches"
    ],
    output_instructions=[
        "Provide 3-5 high-quality recommendations",
        "Include accurate book information",
        "Write clear, informative descriptions",
        "Explain specifically why each book matches"
    ]
)
```

### 3. Agent Implementation
The agent will be implemented as a single atomic component with:
- Clear input/output schemas
- No external dependencies at this stage
- Simple CLI interface
- Structured data output for future reference

## Implementation Steps

1. Create basic project structure:
```
book_recommendations_atomic/
├── src/
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── book_schemas.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── book_agent.py
│   └── cli/
│       ├── __init__.py
│       └── main.py
├── tests/
└── requirements.txt
```

2. Implement core components:
   - Define schemas in `book_schemas.py`
   - Create book agent in `book_agent.py`
   - Implement CLI interface in `main.py`

3. Testing strategy:
   - Unit tests for schema validation
   - Tests for agent responses
   - CLI interaction tests

## Usage Example

```python
# Example CLI interaction
book_agent = BookRecommendationAgent(config=agent_config)
response = book_agent.run(
    BookRecommendationInput(
        thought="I want to read something about first contact with aliens"
    )
)

# Response will be structured as BookRecommendationOutput
for book in response.recommendations:
    print(f"\nTitle: {book.title}")
    print(f"Author: {book.author}")
    print(f"Genre: {book.genre}")
    print(f"Description: {book.description}")
    print(f"Reason: {book.reason}")
```

## Next Steps
1. Implement basic agent functionality
2. Add CLI interface
3. Add basic error handling
4. Add tests
5. Plan for future enhancements (book selection, detailed views, etc.)
