"""Global state management for ragatui execution."""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import threading


@dataclass
class MetricData:
    """Data structure for tracked metrics."""
    name: str
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    history: List[tuple[datetime, Any]] = field(default_factory=list)


@dataclass
class WidgetConfig:
    """Configuration for a widget."""
    widget_type: str
    name: str
    variable_name: Optional[str] = None
    callback: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExecutionState:
    """
    Singleton to manage global execution state across decorators.
    
    This class maintains the state of all tracked variables, widgets,
    and execution metadata.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._metrics: Dict[str, MetricData] = {}
        self._widgets: List[WidgetConfig] = []
        self._logs: List[str] = []
        self._execution_metadata: Dict[str, Any] = {}
        self._lock = threading.RLock()
        
    def register_widget(self, config: WidgetConfig) -> None:
        """Register a new widget configuration."""
        with self._lock:
            self._widgets.append(config)
    
    def update_metric(self, name: str, value: Any) -> None:
        """Update a metric value and maintain its history."""
        with self._lock:
            timestamp = datetime.now()
            if name not in self._metrics:
                self._metrics[name] = MetricData(name=name, value=value, timestamp=timestamp)
            else:
                metric = self._metrics[name]
                metric.history.append((metric.timestamp, metric.value))
                metric.value = value
                metric.timestamp = timestamp
    
    def get_metric(self, name: str) -> Optional[MetricData]:
        """Get current metric data."""
        with self._lock:
            return self._metrics.get(name)
    
    def get_all_metrics(self) -> Dict[str, MetricData]:
        """Get all metrics."""
        with self._lock:
            return self._metrics.copy()
    
    def get_widgets(self) -> List[WidgetConfig]:
        """Get all registered widgets."""
        with self._lock:
            return self._widgets.copy()
    
    def add_log(self, message: str) -> None:
        """Add a log message."""
        with self._lock:
            self._logs.append(message)
    
    def get_logs(self, limit: Optional[int] = None) -> List[str]:
        """Get log messages."""
        with self._lock:
            if limit:
                return self._logs[-limit:]
            return self._logs.copy()
    
    def set_metadata(self, key: str, value: Any) -> None:
        """Set execution metadata."""
        with self._lock:
            self._execution_metadata[key] = value
    
    def get_metadata(self, key: Optional[str] = None) -> Any:
        """Get execution metadata."""
        with self._lock:
            if key:
                return self._execution_metadata.get(key)
            return self._execution_metadata.copy()
    
    def reset(self) -> None:
        """Reset all state (useful for testing)."""
        with self._lock:
            self._metrics.clear()
            self._widgets.clear()
            self._logs.clear()
            self._execution_metadata.clear()
