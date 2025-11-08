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
        self.set_interval(0.5, self.refresh_output)

    def refresh_output(self) -> None:
        """Refresh the output display with new logs."""
        logs = self.state.get_logs()

        # Only add new logs since last update
        if len(logs) > self._last_log_count:
            new_logs = logs[self._last_log_count:]
            for log in new_logs:
                self.write(log)
            self._last_log_count = len(logs)

        # Keep only the last max_lines
        if self.line_count > self.max_lines:
            self.clear()
            recent_logs = self.state.get_logs(limit=self.max_lines)
            for log in recent_logs:
                self.write(log)
            self._last_log_count = len(recent_logs)
