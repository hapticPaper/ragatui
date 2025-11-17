"""Widget for displaying key metrics."""

from rich.panel import Panel
from rich.table import Table
from textual.widgets import Static

from ragatui.core.state import ExecutionState


class MetricsWidget(Static):
    """
    Widget to display key metrics and execution information.

    This widget shows:
    - Execution metadata
    - Tracked variables and their current values
    - Summary statistics
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = ExecutionState()
        # Refresh more frequently for real-time updates (every 200ms)
        self.set_interval(0.2, self.refresh_metrics)

    def refresh_metrics(self) -> None:
        """Refresh the metrics display."""
        self.update(self._render_metrics())

    def _render_metrics(self) -> Panel:
        """Render metrics as a Rich panel."""
        table = Table(title="Execution Metrics", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Add execution metadata
        metadata = self.state.get_metadata()
        for key, value in metadata.items():
            table.add_row(key, str(value))

        # Add tracked metrics
        metrics = self.state.get_all_metrics()
        if metrics:
            table.add_section()
            for name, metric_data in metrics.items():
                value_str = str(metric_data.value)
                if len(metric_data.history) > 0:
                    value_str += f" (updated {len(metric_data.history) + 1} times)"
                table.add_row(name, value_str)

        # Add widget information
        widgets = self.state.get_widgets()
        if widgets:
            table.add_section()
            table.add_row("Active Widgets", str(len(widgets)))

        return Panel(table, title="[bold]Key Metrics[/bold]", border_style="blue")
