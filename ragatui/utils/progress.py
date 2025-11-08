"""Progress tracking utilities with tqdm integration."""

from typing import Optional, Iterator, Any
from tqdm import tqdm as tqdm_original

from ragatui.core.state import ExecutionState


class ProgressTracker:
    """
    Progress tracker that integrates with both tqdm and ragatui TUI.
    
    This class wraps tqdm to provide progress tracking that works
    both in CLI and TUI modes.
    """
    
    def __init__(
        self,
        iterable: Optional[Any] = None,
        total: Optional[int] = None,
        desc: Optional[str] = None,
        level: int = 0,
        state: Optional[ExecutionState] = None
    ):
        """
        Initialize progress tracker.
        
        Args:
            iterable: Iterable to track progress on
            total: Total number of iterations
            desc: Description of the progress
            level: Nesting level
            state: ExecutionState instance
        """
        self.iterable = iterable
        self.total = total
        self.desc = desc or "Progress"
        self.level = level
        self.state = state or ExecutionState()
        self.current = 0
        self._tqdm = None
    
    def __enter__(self):
        """Start progress tracking."""
        # Create tqdm instance for CLI output
        self._tqdm = tqdm_original(
            iterable=self.iterable,
            total=self.total,
            desc=self.desc,
            leave=True
        )
        
        # Register with state
        self.state.set_metadata(f"progress_{self.desc}_total", self.total or 0)
        self.state.set_metadata(f"progress_{self.desc}_current", 0)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Complete progress tracking."""
        if self._tqdm:
            self._tqdm.close()
        
        # Mark as complete
        self.state.set_metadata(f"progress_{self.desc}_complete", True)
        return False
    
    def __iter__(self) -> Iterator:
        """Iterate with progress tracking."""
        if self._tqdm:
            for item in self._tqdm:
                self.current += 1
                self.state.set_metadata(f"progress_{self.desc}_current", self.current)
                yield item
        elif self.iterable:
            for item in self.iterable:
                self.current += 1
                self.state.set_metadata(f"progress_{self.desc}_current", self.current)
                yield item
    
    def update(self, n: int = 1) -> None:
        """
        Update progress by n steps.
        
        Args:
            n: Number of steps to increment
        """
        self.current += n
        if self._tqdm:
            self._tqdm.update(n)
        self.state.set_metadata(f"progress_{self.desc}_current", self.current)
    
    def set_description(self, desc: str) -> None:
        """
        Update the description.
        
        Args:
            desc: New description
        """
        self.desc = desc
        if self._tqdm:
            self._tqdm.set_description(desc)


def progress(
    iterable: Optional[Any] = None,
    total: Optional[int] = None,
    desc: Optional[str] = None,
    level: int = 0
) -> ProgressTracker:
    """
    Create a progress tracker.
    
    This is a convenience function similar to tqdm.
    
    Args:
        iterable: Iterable to track
        total: Total iterations
        desc: Description
        level: Nesting level
        
    Returns:
        ProgressTracker instance
    
    Usage:
        for i in progress(range(100), desc="Training"):
            # do work
            pass
    """
    return ProgressTracker(
        iterable=iterable,
        total=total,
        desc=desc,
        level=level
    )
