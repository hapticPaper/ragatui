"""Logging utilities for ragatui."""

import sys
import logging
from typing import Optional, TextIO
from io import StringIO
import structlog

from ragatui.core.state import ExecutionState


class LogCapture:
    """
    Context manager to capture logs and add them to ExecutionState.
    
    This works with both standard logging and structlog.
    """
    
    def __init__(self, state: Optional[ExecutionState] = None):
        self.state = state or ExecutionState()
        self._old_stdout: Optional[TextIO] = None
        self._old_stderr: Optional[TextIO] = None
        self._stdout_capture = StringIO()
        self._stderr_capture = StringIO()
    
    def __enter__(self):
        """Start capturing logs."""
        # Redirect stdout and stderr
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        sys.stdout = self._stdout_capture
        sys.stderr = self._stderr_capture
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop capturing and process logs."""
        # Restore stdout and stderr
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr
        
        # Process captured stdout
        stdout_content = self._stdout_capture.getvalue()
        if stdout_content:
            for line in stdout_content.splitlines():
                if line.strip():
                    self.state.add_log(line)
        
        # Process captured stderr
        stderr_content = self._stderr_capture.getvalue()
        if stderr_content:
            for line in stderr_content.splitlines():
                if line.strip():
                    self.state.add_log(f"[ERROR] {line}")
        
        return False  # Don't suppress exceptions


class RagaTUIHandler(logging.Handler):
    """
    Custom logging handler that sends logs to ExecutionState.
    """
    
    def __init__(self, state: Optional[ExecutionState] = None):
        super().__init__()
        self.state = state or ExecutionState()
    
    def emit(self, record: logging.LogRecord):
        """Process a log record."""
        try:
            msg = self.format(record)
            level_prefix = f"[{record.levelname}]"
            self.state.add_log(f"{level_prefix} {msg}")
        except Exception:
            self.handleError(record)


def setup_logging(
    level: int = logging.INFO,
    use_structlog: bool = False,
    state: Optional[ExecutionState] = None
) -> None:
    """
    Setup logging for ragatui.
    
    This configures both standard logging and optionally structlog
    to send logs to the TUI.
    
    Args:
        level: Logging level
        use_structlog: Whether to configure structlog
        state: ExecutionState to send logs to
    """
    state = state or ExecutionState()
    
    # Setup standard logging
    handler = RagaTUIHandler(state)
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
    
    # Setup structlog if requested
    if use_structlog:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
