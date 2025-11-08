"""
ragatui - A modular code execution TUI for Python with LLM-powered monitoring.

This package provides decorators and utilities to easily convert Python scripts
into interactive TUI applications with real-time monitoring and analysis.
"""

from ragatui.config import configure_llm, configure_rag, get_config
from ragatui.core.app import RagaTUIApp
from ragatui.core.registry import WidgetRegistry
from ragatui.decorators import (
    execution_info,
    gauge,
    progress,
    tui_app,
    tui_args,
    tui_graph,
)

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
    "configure_llm",
    "configure_rag",
    "get_config",
]
