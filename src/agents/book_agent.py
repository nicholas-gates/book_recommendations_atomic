"""
Book recommendation agent implementation using Atomic Agents framework.
This agent provides book recommendations based on user input.
"""

# import instructor
from atomic_agents.agents.base_agent import BaseAgent, BaseAgentConfig
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator

from ..schemas.book_schemas import (
    BookRecommendationInput,
    BookRecommendationOutput
)
from ..logging.logger import Logger

class BookRecommendationAgent(BaseAgent):
    """
    Agent for providing personalized book recommendations.

    This agent uses a structured approach to:
    1. Analyze user's reading interests
    2. Generate relevant book recommendations
    3. Provide detailed explanations for each recommendation
    """

    input_schema = BookRecommendationInput
    output_schema = BookRecommendationOutput

    def __init__(self, config: BaseAgentConfig = None):
        """
        Initialize the book recommendation agent.

        Args:
            config (BaseAgentConfig, optional): Agent configuration.
                If not provided, a default configuration will be used.
        """
        if config is None:
            config = self._create_default_config()

        super().__init__(config)
        self.logger = Logger(__name__)

    @staticmethod
    def _create_default_config() -> BaseAgentConfig:
        """
        Create default configuration for the book recommendation agent.

        Returns:
            BaseAgentConfig: Default agent configuration
        """
        system_prompt_generator = SystemPromptGenerator(
            background=[
                "You are an expert librarian and book recommender.",
                "Your goal is to provide thoughtful, personalized book recommendations.",
                "You have extensive knowledge of literature across all genres and periods.",
                "You focus on providing accurate, well-researched recommendations."
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
                "Explain specifically why each book matches",
                "Ensure all recommendations truly align with the user's interests"
            ]
        )

        return BaseAgentConfig(
            system_prompt_generator=system_prompt_generator,
            input_schema=BookRecommendationInput,
            output_schema=BookRecommendationOutput
        )

    def run(self, params: BookRecommendationInput) -> BookRecommendationOutput:
        """
        Generate book recommendations based on user input.

        Args:
            params (BookRecommendationInput): User's reading interests

        Returns:
            BookRecommendationOutput: List of personalized book recommendations
        """
        self.logger.log('info', 'Running book recommendation agent', {
            'input': params.model_dump()
        })
        
        try:
            output = super().run(params)
            self.logger.log('info', 'Book recommendations generated', {
                'num_recommendations': len(output.recommendations)
            })
            return output
            
        except Exception as e:
            self.logger.log('error', 'Error in book recommendation agent', {
                'error': str(e),
                'input': params.model_dump()
            })
            raise
