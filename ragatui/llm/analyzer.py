"""Log analyzer using LLM for key metrics extraction."""

import asyncio
from typing import Any, Optional

from ragatui.llm.providers import LLMProvider, LLMProviderType, get_llm_provider


class LogAnalyzer:
    """
    Analyzes logs in near real-time using LLMs.

    This class periodically analyzes accumulated logs to extract:
    - Key metrics
    - Important events
    - Potential issues
    - Performance insights
    """

    def __init__(
        self,
        provider: Optional[LLMProvider] = None,
        analysis_interval: float = 10.0,
        batch_size: int = 100
    ):
        """
        Initialize the log analyzer.

        Args:
            provider: LLM provider to use (defaults to OpenAI)
            analysis_interval: How often to analyze logs (seconds)
            batch_size: Number of log lines to analyze at once
        """
        self.provider = provider or get_llm_provider(LLMProviderType.OPENAI)
        self.analysis_interval = analysis_interval
        self.batch_size = batch_size
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def analyze_batch(
        self,
        logs: list[str],
        context: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Analyze a batch of logs.

        Args:
            logs: List of log messages to analyze
            context: Optional context about the execution

        Returns:
            Analysis results including metrics, issues, and insights
        """
        return await self.provider.analyze_logs(logs, context)

    async def start_continuous_analysis(self, log_source: Any) -> None:
        """
        Start continuous log analysis.

        Args:
            log_source: Source to pull logs from (e.g., ExecutionState)
        """
        self._running = True

        while self._running:
            try:
                # Get recent logs
                logs = log_source.get_logs(limit=self.batch_size)

                if logs:
                    # Analyze the logs
                    analysis = await self.analyze_batch(logs)

                    # Store analysis results in metadata
                    log_source.set_metadata("llm_analysis", analysis)

                # Wait before next analysis
                await asyncio.sleep(self.analysis_interval)

            except Exception as e:
                # Log error but continue
                log_source.add_log(f"[ANALYZER ERROR] {str(e)}")
                await asyncio.sleep(self.analysis_interval)

    def stop_continuous_analysis(self) -> None:
        """Stop continuous log analysis."""
        self._running = False
        if self._task:
            self._task.cancel()

    def create_analysis_prompt(
        self,
        logs: list[str],
        context: Optional[str] = None
    ) -> str:
        """
        Create a prompt for log analysis.

        Args:
            logs: Log messages to analyze
            context: Optional context

        Returns:
            Formatted prompt for the LLM
        """
        prompt = "Analyze the following logs and extract:\n"
        prompt += "1. Key metrics and their values\n"
        prompt += "2. Any errors or warnings\n"
        prompt += "3. Performance insights\n"
        prompt += "4. Notable events or patterns\n\n"

        if context:
            prompt += f"Context: {context}\n\n"

        prompt += "Logs:\n"
        prompt += "\n".join(logs[-50:])  # Last 50 lines
        prompt += "\n\nProvide a structured analysis."

        return prompt
