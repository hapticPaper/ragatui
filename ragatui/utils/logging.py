"""Logging utilities for ragatui."""

import io
from typing import Optional
from ragatui.core.state import ExecutionState

class TUIStream(io.StringIO):
    """
    Stream that redirects output to the TUI ExecutionState.
    
    This allows capturing stdout/stderr and displaying it in the TUI
    in real-time.
    """

    def __init__(self, state: ExecutionState, prefix: str = ""):
        super().__init__()
        self.state = state
        self.prefix = prefix
        self.buffer = ""

    def write(self, text: str) -> int:
        """Write text to the stream and update state."""
        # Add to local buffer
        self.buffer += text
        
        # Process complete lines
        if "\n" in self.buffer:
            lines = self.buffer.split("\n")
            # All lines except the last one are complete
            for line in lines[:-1]:
                if line:  # Skip empty lines if desired, or keep them
                    self.state.add_log(f"{self.prefix}{line}")
            
            # The last part is the new buffer
            self.buffer = lines[-1]
            
        return len(text)

    def flush(self) -> None:
        """Flush remaining buffer."""
        if self.buffer:
            self.state.add_log(f"{self.prefix}{self.buffer}")
            self.buffer = ""
        super().flush()
