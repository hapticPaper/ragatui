"""Widget for displaying progress bars with tqdm integration."""

from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime

from ragatui.core.state import ExecutionState


@dataclass
class ProgressInfo:
    """Information about a progress bar."""
    name: str
    current: int
    total: int
    description: str = ""
    start_time: datetime = None
    level: int = 0  # For nested progress bars
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()


class ProgressWidget(Static):
    """
    Widget to display progress bars.
    
    This widget manages multiple progress bars, supporting nested
    progress tracking for complex operations.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state = ExecutionState()
        self.progress_bars: Dict[str, ProgressInfo] = {}
        self.set_interval(0.2, self.refresh_progress)
    
    def add_progress(
        self, 
        name: str, 
        total: int, 
        description: str = "",
        level: int = 0
    ) -> None:
        """Add a new progress bar."""
        self.progress_bars[name] = ProgressInfo(
            name=name,
            current=0,
            total=total,
            description=description,
            level=level
        )
    
    def update_progress(self, name: str, current: int) -> None:
        """Update progress for a specific bar."""
        if name in self.progress_bars:
            self.progress_bars[name].current = current
    
    def remove_progress(self, name: str) -> None:
        """Remove a completed progress bar."""
        self.progress_bars.pop(name, None)
    
    def refresh_progress(self) -> None:
        """Refresh the progress display."""
        self.update(self._render_progress())
    
    def _render_progress(self) -> Panel:
        """Render all progress bars."""
        if not self.progress_bars:
            return Panel(
                "[dim]No active progress tracking[/dim]",
                title="[bold]Progress[/bold]",
                border_style="cyan"
            )
        
        text = Text()
        
        # Sort by level for proper nesting display
        sorted_bars = sorted(
            self.progress_bars.values(),
            key=lambda x: (x.level, x.name)
        )
        
        for progress in sorted_bars:
            # Indent based on nesting level
            indent = "  " * progress.level
            
            # Calculate percentage
            percentage = (progress.current / progress.total * 100) if progress.total > 0 else 0
            
            # Create progress bar
            bar_width = 25
            filled = int((percentage / 100) * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)
            
            # Calculate elapsed time and ETA
            elapsed = (datetime.now() - progress.start_time).total_seconds()
            if progress.current > 0 and percentage < 100:
                eta = (elapsed / progress.current) * (progress.total - progress.current)
                eta_str = f"ETA: {eta:.1f}s"
            else:
                eta_str = "Done" if percentage >= 100 else "Starting..."
            
            # Build the line
            desc = f" - {progress.description}" if progress.description else ""
            text.append(f"{indent}{progress.name}{desc}\n", style="bold")
            text.append(
                f"{indent}{bar} {percentage:.1f}% ({progress.current}/{progress.total}) {eta_str}\n\n",
                style="cyan"
            )
        
        return Panel(
            text,
            title="[bold]Progress Tracking[/bold]",
            border_style="cyan"
        )
