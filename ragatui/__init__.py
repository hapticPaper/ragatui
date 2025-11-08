"""
ragatui - A modular code execution TUI for Python with LLM-powered monitoring.

This package provides decorators and utilities to easily convert Python scripts
into interactive TUI applications with real-time monitoring and analysis.
"""

from ragatui.decorators import (
    tui_app,
    tui_args,
    tui_graph,
    gauge,
    execution_info,
    progress,
)
from ragatui.core.registry import WidgetRegistry
from ragatui.core.app import RagaTUIApp

__version__ = "0.1.0"

__all__ = [
    "tui_app",
    "tui_args",
    "tui_graph",
    "gauge",
    "execution_info",
    "progress",
    "WidgetRegistry",
    "RagaTUIApp",
]
