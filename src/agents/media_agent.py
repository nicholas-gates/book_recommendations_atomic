"""
Cross-domain media recommendation agent implementation using Atomic Agents framework.
This agent provides recommendations for movies, games, and songs based on a book's themes.
"""

import instructor
from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator

from ..schemas.media_schemas import (
    CrossDomainMediaInput,
    CrossDomainRecommendationsOutput
)
from ..logging.logger import Logger

class CrossDomainMediaAgent(BaseAgent):
    """
    Agent for providing cross-domain media recommendations based on a book.

    This agent uses a structured approach to:
    1. Analyze the themes and elements of a selected book
    2. Find thematically similar content in other media types
    3. Provide detailed explanations of thematic connections
    """

    input_schema = CrossDomainMediaInput
    output_schema = CrossDomainRecommendationsOutput

    def __init__(self, config: BaseAgentConfig = None):
        """
        Initialize the cross-domain media recommendation agent.

        Args:
            config (BaseAgentConfig, optional): Agent configuration.
                If not provided, a default configuration will be used.
        """
        self.logger = Logger(__name__)
        self.logger.log('info', 'Initializing CrossDomainMediaAgent', {
            'has_config': config is not None
        })

        if config is None:
            self.logger.log('debug', 'Creating default config')
            config = self._create_default_config()

        super().__init__(config)
        self.logger.log('info', 'CrossDomainMediaAgent initialized successfully')

    @staticmethod
    def _create_default_config() -> BaseAgentConfig:
        """
        Create default configuration for the cross-domain media agent.

        Returns:
            BaseAgentConfig: Default agent configuration
        """
        logger = Logger(__name__)
        logger.log('debug', 'Creating default agent configuration')

        system_prompt_generator = SystemPromptGenerator(
            background=[
                "You are an expert content recommender who can find thematic connections across different media types.",
                "Your goal is to recommend media that shares deep thematic connections with a given book.",
                "You have extensive knowledge of movies, video games, and music across all genres and periods.",
                "You focus on meaningful thematic links rather than superficial genre similarities."
            ],
            steps=[
                "1. Analyze the core themes, mood, and ideas of the input book",
                "2. Consider both classic and contemporary options in each media type",
                "3. Focus on thematic resonance over genre matching",
                "4. Find one perfect match in each media category",
                "5. Explain the specific thematic connections for each recommendation"
            ],
            output_instructions=[
                "Recommend exactly ONE movie, ONE game, and ONE song",
                "Ensure each recommendation has a strong thematic connection",
                "Provide clear, specific reasons for each connection",
                "Include accurate details for each media item",
                "Write engaging, informative descriptions"
            ]
        )

        config = BaseAgentConfig(
            system_prompt_generator=system_prompt_generator,
            input_schema=CrossDomainMediaInput,
            output_schema=CrossDomainRecommendationsOutput
        )

        logger.log('debug', 'Default configuration created', {
            'config_type': type(config).__name__,
            'input_schema': config.input_schema.__name__,
            'output_schema': config.output_schema.__name__
        })

        return config

    def run(self, book: CrossDomainMediaInput) -> CrossDomainRecommendationsOutput:
        """
        Generate cross-domain media recommendations based on a book.

        Args:
            params (CrossDomainMediaInput): Book information including title, author,
                                        genre, and description

        Returns:
            CrossDomainRecommendations: Thematically related movie, game, and song
        """
        self.logger.log('info', 'Starting media recommendation generation', {
            'book_title': book.title,
            'book_author': book.author,
            'book_genre': book.genre
        })
        
        try:
            self.logger.log('debug', 'Calling parent run method')
            output = super().run(book)
            
            self.logger.log('info', 'Media recommendations generated successfully. Media titles:', {
                'book': book.title,
                'movie_recommendation': output.movie.title,
                'game_recommendation': output.game.title,
                'song_recommendation': output.song.title
            })
            
            return output
            
        except Exception as e:
            self.logger.log('error', 'Failed to generate media recommendations', {
                'book_title': book.title,
                'error_type': type(e).__name__,
                'error_message': str(e),
                'input_params': book.dict()
            })
            
            raise
