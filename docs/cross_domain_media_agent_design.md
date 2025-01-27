# Cross Domain Media Agent Design

## Overview
The Cross Domain Media Agent extends the book recommendation system by suggesting related media across different domains (movies, games, songs) that share thematic elements with a selected book.

## Core Components

### 1. Schemas

#### Media Item Base Schema
Common fields shared across media types:
- title: str
- description: str
- reason: str (explanation of thematic connection to book)

#### Movie Schema (extends Media Item)
```python
class MovieRecommendation(BaseModel):
    title: str
    year: str
    description: str
    reason: str
```

#### Game Schema (extends Media Item)
```python
class GameRecommendation(BaseModel):
    title: str
    platform: str
    description: str
    reason: str
```

#### Song Schema (extends Media Item)
```python
class SongRecommendation(BaseModel):
    title: str
    artist: str
    description: str
    reason: str
```

#### Cross Domain Recommendations Schema
```python
class CrossDomainRecommendations(BaseModel):
    movie: MovieRecommendation
    game: GameRecommendation
    song: SongRecommendation
```

### 2. Agent Design

#### CrossDomainMediaAgent
- Extends `BaseAgent` from Atomic Agents framework
- Takes a selected book recommendation as input
- Uses OpenAI to generate thematically related media recommendations
- Returns structured recommendations using Pydantic models

##### System Prompt
```
You are an expert content recommender who can find thematic connections across different media types.
Based on the given book, recommend ONE movie, ONE game, and ONE song that share similar themes, moods, or ideas.

Guidelines for recommendations:
1. Focus on thematic connections, not just genre matches
2. Consider emotional resonance and core ideas
3. Provide thoughtful explanations for each recommendation
4. Be specific about why each item connects to the book
5. Consider both classic and contemporary options
```

### 3. CLI Interface

#### User Flow
1. User receives book recommendations from existing book agent
2. User selects a book from the recommendations
3. System uses CrossDomainMediaAgent to generate related media
4. System displays formatted recommendations for movie, game, and song

#### Output Format
- Each recommendation displayed in a Rich panel
- Sections for movie, game, and song recommendations
- Clear visual separation between different media types
- Thematic connections clearly explained

### 4. Implementation Steps

1. Create Schemas
   - Define Pydantic models for each media type
   - Implement cross-domain recommendations model

2. Implement Agent
   - Create CrossDomainMediaAgent class
   - Configure system prompt and output schema
   - Implement recommendation generation logic

3. Update CLI
   - Add book selection interface
   - Integrate cross-domain recommendations
   - Implement Rich formatting for output

4. Testing
   - Test schema validation
   - Verify thematic relevance of recommendations
   - Test error handling and edge cases

### 5. Future Enhancements
- Add more media types (TV shows, podcasts, etc.)
- Implement recommendation caching
- Add user feedback mechanism
- Support batch recommendations
- Add filtering options for media types
