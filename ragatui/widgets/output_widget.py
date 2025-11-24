"""Widget for displaying captured output and logs."""

from textual.reactive import reactive
from textual.widgets import RichLog

from ragatui.core.state import ExecutionState


class OutputWidget(RichLog):
    """
    Widget to display captured output and logs.

    This widget continuously displays the output from the executing script,
    including stdout, stderr, and structured logs.
    """

    update_count: reactive[int] = reactive(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = ExecutionState()
        self.max_lines = 1000
        self._last_log_count = 0
        self._update_task = None

    def on_mount(self) -> None:
        """Start the update loop when widget is mounted."""
        # Start continuous updates using set_interval instead of @work
        self.set_interval(0.01, self.refresh_output)

    def refresh_output(self) -> None:
        """Refresh the output display with new logs."""
        logs = self.state.get_logs()

        # Only add new logs since last update
        if len(logs) > self._last_log_count:
            new_logs = logs[self._last_log_count:]
            for log in new_logs:
                # Write with scroll_end=True to ensure it scrolls and is visible
                self.write(log, scroll_end=True)
            self._last_log_count = len(logs)

        # Keep only the last max_lines
        line_count = len(self.lines) if self.lines else 0
        max_line_limit = self.max_lines or 1000
        if line_count > max_line_limit:
            self.clear()
            recent_logs = self.state.get_logs(limit=max_line_limit)
            for log in recent_logs:
                self.write(log, scroll_end=True)
            self._last_log_count = len(recent_logs)
