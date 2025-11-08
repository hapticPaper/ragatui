"""Widget for displaying time-series graphs of tracked variables."""

from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text

from ragatui.core.state import ExecutionState, MetricData


class GraphWidget(Static):
    """
    Widget to display a graph of a tracked variable over time.
    
    This widget tracks the history of a variable and displays it
    as an ASCII-based graph.
    """
    
    def __init__(self, metric_name: str, **kwargs):
        super().__init__(**kwargs)
        self.metric_name = metric_name
        self.state = ExecutionState()
        self.set_interval(1.0, self.refresh_graph)
    
    def refresh_graph(self) -> None:
        """Refresh the graph display."""
        self.update(self._render_graph())
    
    def _render_graph(self) -> Panel:
        """Render the graph as a Rich panel."""
        metric = self.state.get_metric(self.metric_name)
        
        if not metric:
            return Panel(
                f"[yellow]Waiting for metric: {self.metric_name}[/yellow]",
                title=f"[bold]{self.metric_name}[/bold]",
                border_style="yellow"
            )
        
        # Create a simple ASCII graph
        text = Text()
        text.append(f"Current value: {metric.value}\n", style="bold green")
        text.append(f"Last updated: {metric.timestamp.strftime('%H:%M:%S')}\n", style="dim")
        
        if metric.history:
            text.append(f"\nHistory ({len(metric.history)} points):\n", style="bold")
            
            # Get numeric values for graphing
            try:
                values = [float(metric.value)]
                for _, val in metric.history[-20:]:  # Last 20 points
                    try:
                        values.insert(0, float(val))
                    except (ValueError, TypeError):
                        pass
                
                if values and len(values) > 1:
                    min_val = min(values)
                    max_val = max(values)
                    
                    # Simple ASCII sparkline
                    if max_val > min_val:
                        height = 5
                        for val in values[-40:]:  # Show up to 40 points
                            normalized = (val - min_val) / (max_val - min_val)
                            bar_height = int(normalized * height)
                            text.append("▁▂▃▄▅▆▇█"[min(bar_height, 7)])
                        text.append(f"\n  Min: {min_val:.2f}  Max: {max_val:.2f}")
                    else:
                        text.append("  [dim](constant value)[/dim]")
            except (ValueError, TypeError):
                text.append("  [dim](non-numeric values)[/dim]")
        else:
            text.append("\n[dim]No history yet[/dim]")
        
        return Panel(
            text,
            title=f"[bold]Graph: {self.metric_name}[/bold]",
            border_style="green"
        )
