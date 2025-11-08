"""
Example demonstrating ragatui with agentic workflows.

This example shows how ragatui can be used with LangGraph or PydanticAI
to monitor complex agent pipelines.

Note: This is a conceptual example. Install langgraph or pydantic-ai separately:
    pip install ragatui[agentic]
"""

import time
from ragatui import tui_app, execution_info, gauge
from ragatui.core.state import ExecutionState


class AgentState:
    """Simulates agent state in an agentic workflow."""

    def __init__(self):
        self.current_step = ""
        self.steps_completed = 0
        self.total_steps = 5
        self.confidence = 0.0
        self.tokens_used = 0

    @gauge("confidence", min_value=0, max_value=100, title="Agent Confidence")
    def update_confidence(self, value):
        """Update agent confidence score."""
        self.confidence = value

    @gauge("tokens_used", min_value=0, max_value=10000, title="Tokens Used")
    def update_tokens(self, value):
        """Update token usage."""
        self.tokens_used = value


class MockAgentWorkflow:
    """
    Mock agentic workflow demonstrating integration patterns.

    In a real implementation, this would integrate with:
    - LangGraph for graph-based agent workflows
    - PydanticAI for structured agent interactions
    - LangChain for chain-based pipelines
    """

    def __init__(self):
        self.state = AgentState()
        self.execution_state = ExecutionState()

    def research_step(self):
        """Agent performs research."""
        print("\n[AGENT] Step 1: Research Phase")
        print("  Searching knowledge base...")
        time.sleep(1)
        print("  Found 15 relevant documents")

        self.state.update_confidence(65)
        self.state.update_tokens(250)
        self.state.steps_completed += 1

        self.execution_state.set_metadata("research_docs_found", 15)

    def analysis_step(self):
        """Agent analyzes information."""
        print("\n[AGENT] Step 2: Analysis Phase")
        print("  Analyzing retrieved information...")
        time.sleep(1.5)
        print("  Generated 3 hypotheses")

        self.state.update_confidence(75)
        self.state.update_tokens(500)
        self.state.steps_completed += 1

        self.execution_state.set_metadata("hypotheses_generated", 3)

    def reasoning_step(self):
        """Agent performs reasoning."""
        print("\n[AGENT] Step 3: Reasoning Phase")
        print("  Evaluating hypotheses...")
        time.sleep(1)
        print("  Selected best approach")

        self.state.update_confidence(85)
        self.state.update_tokens(750)
        self.state.steps_completed += 1

        self.execution_state.set_metadata("approach_selected", True)

    def execution_step(self):
        """Agent executes plan."""
        print("\n[AGENT] Step 4: Execution Phase")
        print("  Executing plan...")
        time.sleep(2)
        print("  Generated solution")

        self.state.update_confidence(90)
        self.state.update_tokens(1200)
        self.state.steps_completed += 1

        self.execution_state.set_metadata("solution_generated", True)

    def verification_step(self):
        """Agent verifies results."""
        print("\n[AGENT] Step 5: Verification Phase")
        print("  Verifying solution...")
        time.sleep(1)
        print("  Solution validated")

        self.state.update_confidence(95)
        self.state.update_tokens(1400)
        self.state.steps_completed += 1

        self.execution_state.set_metadata("solution_validated", True)

    def run(self):
        """Run the complete agent workflow."""
        print("=" * 60)
        print("Agentic Workflow Execution")
        print("=" * 60)

        steps = [
            self.research_step,
            self.analysis_step,
            self.reasoning_step,
            self.execution_step,
            self.verification_step,
        ]

        for step_func in steps:
            step_func()
            print(
                f"  Progress: {self.state.steps_completed}/{self.state.total_steps} "
                f"({self.state.steps_completed / self.state.total_steps * 100:.0f}%)"
            )
            print(f"  Confidence: {self.state.confidence}%")
            print(f"  Tokens used: {self.state.tokens_used}")

        print("\n" + "=" * 60)
        print("Workflow Complete!")
        print("=" * 60)

        return {
            "status": "success",
            "steps_completed": self.state.steps_completed,
            "final_confidence": self.state.confidence,
            "total_tokens": self.state.tokens_used,
        }


@tui_app(title="Agentic Workflow Monitor")
@execution_info(
    agent_type="ReasoningAgent",
    framework="LangGraph",
    llm_provider="OpenAI",
    model="gpt-4",
)
def run_agent_workflow():
    """
    Run an agentic workflow with ragatui monitoring.

    This demonstrates how ragatui can provide visibility into:
    - Agent decision-making steps
    - Confidence scores at each stage
    - Resource usage (tokens, time)
    - Structured execution flow
    """
    print("Initializing agentic workflow...\n")

    workflow = MockAgentWorkflow()

    try:
        result = workflow.run()
        print(f"\nWorkflow result: {result}")
        return result
    except Exception as e:
        print(f"\n[ERROR] Workflow failed: {str(e)}")
        return {"status": "failed", "error": str(e)}


if __name__ == "__main__":
    # Run the agentic workflow with TUI monitoring
    result = run_agent_workflow()

    print("\n" + "=" * 60)
    print("Integration Notes:")
    print("=" * 60)
    print("""
This example demonstrates the pattern for integrating ragatui with agentic workflows:

1. LangGraph Integration:
   - Decorate graph nodes with @tui_graph for state tracking
   - Use @gauge for agent metrics (confidence, token usage)
   - Use @execution_info for workflow metadata

2. PydanticAI Integration:
   - Decorate agent methods with monitoring decorators
   - Track structured outputs and validation states
   - Monitor agent reasoning chains

3. General Patterns:
   - Each agent step updates relevant metrics
   - TUI provides real-time visibility
   - LLM analysis can provide insights on agent performance
   - RAG can compare against historical agent runs

For production use, integrate with actual LangGraph/PydanticAI code
and enable LLM analysis for deeper insights.
    """)
