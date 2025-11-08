"""Widget registry for custom user widgets."""

import threading
from typing import Any, Callable, Optional

from textual.widget import Widget


class WidgetRegistry:
    """
    Registry for custom widgets.

    Allows users to register their own custom widgets that can be
    instantiated and used within the TUI.
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
        self._widgets: dict[str, type[Widget]] = {}
        self._factories: dict[str, Callable[..., Widget]] = {}

    def register_widget(
        self,
        name: str,
        widget_class: type[Widget],
        factory: Optional[Callable[..., Widget]] = None
    ) -> None:
        """
        Register a custom widget.

        Args:
            name: Unique name for the widget
            widget_class: The widget class to register
            factory: Optional factory function to create the widget
        """
        self._widgets[name] = widget_class
        if factory:
            self._factories[name] = factory

    def get_widget_class(self, name: str) -> Optional[type[Widget]]:
        """Get a registered widget class by name."""
        return self._widgets.get(name)

    def create_widget(self, name: str, **kwargs: Any) -> Optional[Widget]:
        """
        Create an instance of a registered widget.

        Args:
            name: Name of the registered widget
            **kwargs: Arguments to pass to the widget constructor or factory

        Returns:
            Widget instance or None if not found
        """
        if name in self._factories:
            return self._factories[name](**kwargs)

        widget_class = self._widgets.get(name)
        if widget_class:
            return widget_class(**kwargs)

        return None

    def list_widgets(self) -> list[str]:
        """List all registered widget names."""
        return list(self._widgets.keys())

    def unregister_widget(self, name: str) -> None:
        """Unregister a widget."""
        self._widgets.pop(name, None)
        self._factories.pop(name, None)
