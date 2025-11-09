"""Main TUI application for ragatui."""

from typing import Any, Callable, Optional

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Label

from ragatui.core.registry import WidgetRegistry
from ragatui.core.state import ExecutionState
from ragatui.widgets.metrics_widget import MetricsWidget
from ragatui.widgets.output_widget import OutputWidget


class RagaTUIApp(App):
    """
    Main TUI application for ragatui.

    This app provides a two-pane layout:
    - Left pane: Output/logs from the executed script
    - Right pane: Key metrics and analysis

    Users can extend this with custom widgets.
    """

    CSS = """
    Screen {
        layout: horizontal;
    }

    #left-pane {
        width: 60%;
        border: solid $primary;
    }

    #right-pane {
        width: 40%;
        border: solid $secondary;
    }

    .pane-title {
        background: $boost;
        color: $text;
        text-align: center;
        padding: 1;
    }

    #output-container {
        height: 100%;
    }

    #metrics-container {
        height: 100%;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("r", "refresh_all", "Refresh"),
    ]

    def __init__(
        self,
        target_func: Optional[Callable] = None,
        title: str = "RagaTUI",
        **kwargs: Any
    ):
        """
        Initialize the RagaTUI app.

        Args:
            target_func: The function to execute and monitor
            title: Application title
        """
        super().__init__(**kwargs)
        self.title = title
        self.target_func = target_func
        self.state = ExecutionState()
        self.registry = WidgetRegistry()

        # Enable automatic refresh for smooth real-time updates
        # This ensures the screen updates frequently even during heavy processing
        self.auto_refresh = 0.05  # Refresh screen every 50ms

    def compose(self) -> ComposeResult:
        """Create the layout."""
        yield Header()

        with Horizontal():
            # Left pane: Output
            with VerticalScroll(id="left-pane"):
                yield Label("Output & Logs", classes="pane-title")
                yield OutputWidget(id="output-container")

            # Right pane: Metrics
            with VerticalScroll(id="right-pane"):
                yield Label("Key Metrics", classes="pane-title")
                yield MetricsWidget(id="metrics-container")

        yield Footer()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def action_refresh_all(self) -> None:
        """Refresh all widgets."""
        output_widget = self.query_one("#output-container", OutputWidget)
        output_widget.refresh_output()

        metrics_widget = self.query_one("#metrics-container", MetricsWidget)
        metrics_widget.refresh_metrics()

    async def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Add initial log message
        self.state.add_log(f"[TUI] Starting {self.title}...")
        self.state.set_metadata("status", "starting")

        # Give the UI a moment to fully render before starting execution
        # This ensures widgets are visible when output starts appearing
        import asyncio
        await asyncio.sleep(0.1)

        # Start the target function if provided
        if self.target_func:
            self.run_worker(self._execute_target)
        else:
            self.state.add_log("[TUI] No target function provided")

    async def _execute_target(self) -> None:
        """Execute the target function in a thread to allow real-time updates."""
        if self.target_func:
            self.state.add_log("[TUI] Executing function...")
            self.state.set_metadata("status", "running")

            # Run the function in a thread pool to avoid blocking the TUI
            # This allows the TUI to update in real-time as output is generated
            import asyncio
            loop = asyncio.get_event_loop()

            try:
                # Execute in thread pool so TUI can update during execution
                result = await loop.run_in_executor(None, self.target_func)
                self.state.set_metadata("execution_result", result)
                self.state.set_metadata("execution_status", "completed")
                self.state.set_metadata("status", "completed")
                self.state.add_log("[TUI] Execution completed successfully")
            except Exception as e:
                self.state.set_metadata("execution_error", str(e))
                self.state.set_metadata("execution_status", "failed")
                self.state.set_metadata("status", "failed")
                self.state.add_log(f"[TUI] Error: {str(e)}")


def run_tui(
    func: Callable,
    title: str = "RagaTUI",
    **app_kwargs: Any
) -> Any:
    """
    Run a function within the TUI.

    Args:
        func: The function to execute and monitor
        title: Application title
        **app_kwargs: Additional arguments for the App

    Returns:
        The result of the function execution
    """
    app = RagaTUIApp(target_func=func, title=title, **app_kwargs)
    app.run()

    # Return the execution result
    state = ExecutionState()
    return state.get_metadata("execution_result")
