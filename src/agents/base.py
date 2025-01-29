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

from ..tracing.langsmith_tracker import trace_operation, add_feedback
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
        super().__init__(config)
        self.logger = Logger(__name__)
        
    def _generate_run_name(self) -> str:
        """Generate a unique name for the current run."""
        timestamp = datetime.now(pytz.UTC).strftime('%Y%m%d_%H%M%S')
        return f"{self.__class__.__name__}_{timestamp}_{str(uuid.uuid4())[:8]}"
        
    def run(self, params: InputType) -> OutputType:
        """
        Run the agent with tracing enabled.
        
        Args:
            params: Input parameters for the agent
            
        Returns:
            Agent output
        """
        run_name = self._generate_run_name()
        
        # Extract input parameters
        input_params = {}
        if hasattr(params, "dict"):
            try:
                input_params = params.dict()
            except Exception as e:
                self.logger.warning(f"Could not serialize input params: {e}")
        else:
            # Try to convert to dict if possible
            try:
                input_params = dict(params)
            except Exception:
                input_params = {"raw_input": str(params)}
        
        # Prepare metadata
        metadata = {
            "agent_type": self.__class__.__name__,
            "input_type": type(params).__name__,
            "timestamp": datetime.now(pytz.UTC).isoformat(),
            "input_params": input_params
        }
        
        # Create tags list
        tags = [
            f"agent_class:{self.__class__.__name__}",
            "operation:run"
        ]
        
        with trace_operation(
            name=run_name,
            metadata=metadata,
            tags=tags
        ):
            try:
                result = super().run(params)
                
                # Add success feedback with output data
                if hasattr(result, "dict"):
                    try:
                        result_dict = result.dict()
                        add_feedback(
                            run_name,
                            "completion",
                            1.0,
                            f"Successfully generated output: {str(result_dict)[:200]}..."
                        )
                    except Exception as e:
                        self.logger.warning(f"Could not add success feedback: {e}")
                        
                return result
                
            except Exception as e:
                # Add error feedback
                add_feedback(
                    run_name,
                    "error",
                    0.0,
                    f"Error during execution: {str(e)}"
                )
                raise
