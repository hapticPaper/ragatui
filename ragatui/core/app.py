"""Main TUI application for ragatui."""

from typing import Optional, Callable, Any
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Static, Label
from textual.reactive import reactive

from ragatui.core.state import ExecutionState
from ragatui.core.registry import WidgetRegistry
from ragatui.widgets.output_widget import OutputWidget
from ragatui.widgets.metrics_widget import MetricsWidget


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
        # Start the target function if provided
        if self.target_func:
            self.run_worker(self._execute_target)
    
    async def _execute_target(self) -> None:
        """Execute the target function."""
        if self.target_func:
            try:
                # Execute the wrapped function
                if callable(self.target_func):
                    result = self.target_func()
                    self.state.set_metadata("execution_result", result)
                    self.state.set_metadata("execution_status", "completed")
            except Exception as e:
                self.state.set_metadata("execution_error", str(e))
                self.state.set_metadata("execution_status", "failed")
                self.state.add_log(f"Error: {str(e)}")


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
