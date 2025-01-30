"""
Base agent implementation with Langsmith tracing support.
Extends the atomic-agents BaseAgent to add tracing capabilities.
"""

from typing import TypeVar, Generic, Any
import uuid
from datetime import datetime
import pytz

from atomic_agents.agents.base_agent import BaseAgent as AtomicBaseAgent
from atomic_agents.agents.base_agent import BaseAgentConfig

from ..tracing.langsmith_tracker import trace_operation
from ..logging.logger import Logger

InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')

class TracedBaseAgent(AtomicBaseAgent, Generic[InputType, OutputType]):
    """
    Base agent with integrated Langsmith tracing.
    Wraps all LLM operations with tracing context managers.
    """
    
    def __init__(self, config: BaseAgentConfig = None):
        """
        Initialize the traced agent.
        
        Args:
            config (BaseAgentConfig, optional): Agent configuration
        """
        # Initialize parent first to ensure config is set
        super().__init__(config)
        # Then set up logging
        self.logger = Logger(__name__)
        
    def _generate_run_name(self) -> str:
        """Generate a unique name for the current run."""
        timestamp = datetime.now(pytz.UTC).strftime('%Y%m%d_%H%M%S')
        return f"{self.__class__.__name__}_{timestamp}"

    def _get_llm_metadata(self, params: InputType) -> dict:
        """Get metadata about the LLM interaction."""
        metadata = {
            "input_params": params.dict() if hasattr(params, 'dict') else {'raw_input': str(params)},
            "model": "gpt-4-turbo-preview",  # This should match what's used in atomic_agents
            "temperature": 0.7  # This should match what's used in atomic_agents
        }
        
        # Only add system prompt if config is available
        if hasattr(self, 'config') and self.config is not None:
            try:
                system_prompt = self.config.system_prompt_generator.generate()
                metadata["system_prompt"] = system_prompt
            except Exception as e:
                self.logger.log('warning', f"Could not get system prompt: {e}")
                
        return metadata
        
    def run(self, params: InputType) -> OutputType:
        """
        Run the agent with tracing enabled.
        
        Args:
            params: Input parameters for the agent
            
        Returns:
            Agent output
        """
        # Generate a unique name for this run
        run_name = self._generate_run_name()

        # Log that we're starting
        self.logger.log('info', f'{self.__class__.__name__} starting run', {
            'input': params.dict() if hasattr(params, 'dict') else {'raw_input': str(params)}
        })

        # Get LLM metadata for tracing
        llm_metadata = self._get_llm_metadata(params)

        # Prepare metadata
        metadata = {
            "agent_type": self.__class__.__name__,
            "input_type": type(params).__name__,
            "timestamp": datetime.now(pytz.UTC).isoformat(),
            "llm_config": llm_metadata
        }
        
        # Create tags list
        tags = [
            f"agent_class:{self.__class__.__name__}",
            "operation:run",
            "component:llm"
        ]
        
        with trace_operation(
            name=run_name,
            run_type="llm",
            metadata=metadata,
            tags=tags
        ):
            try:
                # Run the agent
                result = super().run(params)
                
                # Log success
                if hasattr(result, "dict"):
                    try:
                        result_dict = result.dict()
                        self.logger.log('info', f'{self.__class__.__name__} completed successfully', {
                            'output_type': type(result).__name__
                        })
                    except Exception as e:
                        self.logger.log('warning', f"Could not log success details: {e}")
                        
                return result
                
            except Exception as e:
                # Log the error
                self.logger.log('error', f'{self.__class__.__name__} encountered an error', {
                    'error': str(e),
                    'input': params.dict() if hasattr(params, 'dict') else {'raw_input': str(params)}
                })
                raise
