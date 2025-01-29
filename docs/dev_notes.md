# TODO
* X ADD dotenv import for API key
* X Ask how OpenAI is configured? Model selection, temperature, etc.?
* X Test CLI implementation

# Langsmith Implementation Plan

## Phase 1: Initial Setup
1. [DONE] Install required packages using `uv`:
   - `langsmith`: For tracing and monitoring
   - `langchain`: Required for Langsmith integration
   
2. [DONE] Environment Configuration:
   - Add LANGCHAIN_API_KEY to `.env`
   - Add LANGCHAIN_PROJECT (e.g., "book_recommendations_atomic")
   - Add LANGCHAIN_TRACING_V2="true"

## Phase 2: Core Integration
1. [DONE] Create a new module `src/tracing/langsmith_tracker.py`:
   - Implement a context manager for trace management
   - Add utility functions for common tracing operations
   - Create custom tags for our specific use cases (e.g., recommendation_type, user_preferences)

2. [DONE] Modify BaseAgent class:
   - Add tracing wrapper around core LLM calls
   - Implement run name generation for better trace identification
   - Add error tracking integration

## Phase 3: Agent-Specific Implementation
1. [DONE] Update BookRecommendationAgent:
   - Add tracing for recommendation generation
   - Track user input processing
   - Monitor recommendation quality metrics

2. [DONE] Update MediaAgent:
   - Similar tracing implementation
   - Focus on media-specific metrics

## Phase 4: Monitoring and Analytics
1. Set up Langsmith dashboards:
   - User preference analysis
   - Recommendation success metrics
   - Response time tracking
   - Error rate monitoring

2. Implement custom feedback collection:
   - Track user acceptance of recommendations
   - Monitor recommendation diversity
   - Capture execution times

## Phase 5: Testing and Validation
1. Create test suite for tracing:
   - Verify proper trace creation
   - Validate tag consistency
   - Test error scenarios

2. Performance impact assessment:
   - Measure latency impact
   - Optimize tracing overhead if needed

## Implementation Notes
- Break down each phase into smaller PRs
- Test each component individually
- Document all new tracing patterns
- Consider adding trace sampling for production