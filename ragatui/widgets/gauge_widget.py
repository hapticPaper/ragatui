"""Widget for displaying a gauge of a current value."""

from rich.panel import Panel
from rich.text import Text
from textual.widgets import Static

from ragatui.core.state import ExecutionState


class GaugeWidget(Static):
    """
    Widget to display a gauge for a current value.

    This widget shows the current value of a metric without history,
    optionally as a progress bar if min/max values are provided.
    """

    def __init__(
        self,
        metric_name: str,
        min_value: float = 0,
        max_value: float = 100,
        show_bar: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.metric_name = metric_name
        self.min_value = min_value
        self.max_value = max_value
        self.show_bar = show_bar
        self.state = ExecutionState()
        self.set_interval(0.5, self.refresh_gauge)

    def refresh_gauge(self) -> None:
        """Refresh the gauge display."""
        self.update(self._render_gauge())

    def _render_gauge(self) -> Panel:
        """Render the gauge as a Rich panel."""
        metric = self.state.get_metric(self.metric_name)

        if not metric:
            return Panel(
                f"[yellow]Waiting for metric: {self.metric_name}[/yellow]",
                title=f"[bold]{self.metric_name}[/bold]",
                border_style="yellow"
            )

        text = Text()

        # Display current value
        text.append(f"Current: {metric.value}\n", style="bold green")
        text.append(f"Updated: {metric.timestamp.strftime('%H:%M:%S')}\n", style="dim")

        # Try to show as a progress bar if numeric
        if self.show_bar:
            try:
                value = float(metric.value)
                percentage = ((value - self.min_value) / (self.max_value - self.min_value)) * 100
                percentage = max(0, min(100, percentage))

                # Create a simple text-based progress bar
                bar_width = 30
                filled = int((percentage / 100) * bar_width)
                bar = "█" * filled + "░" * (bar_width - filled)

                text.append(f"\n{bar} {percentage:.1f}%\n", style="cyan")
                text.append(f"Range: {self.min_value} - {self.max_value}", style="dim")
            except (ValueError, TypeError):
                text.append("\n[dim](non-numeric value)[/dim]")

        return Panel(
            text,
            title=f"[bold]Gauge: {self.metric_name}[/bold]",
            border_style="blue"
        )
