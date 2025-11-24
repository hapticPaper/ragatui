"""Core decorators for ragatui."""

import argparse
import functools
import inspect
from typing import Any, Callable, Optional

from ragatui.core.app import run_tui
from ragatui.core.state import ExecutionState, WidgetConfig


def tui_app(
    title: str = "RagaTUI",
    auto_run: bool = True,
    **app_kwargs: Any
) -> Callable:
    """
    Main decorator to convert a Python function into a TUI application.

    This decorator wraps a function to run within the TUI interface,
    capturing output and enabling monitoring.

    Args:
        title: Title for the TUI application
        auto_run: Whether to automatically run the TUI when the function is called
        **app_kwargs: Additional arguments to pass to the TUI app

    Usage:
        @tui_app(title="My Application")
        def main():
            print("Hello from TUI!")
            # your code here
    """
    def decorator(func: Callable) -> Callable:
        state = ExecutionState()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Store function metadata
            state.set_metadata("function_name", func.__name__)
            state.set_metadata("start_time", None)

            # Create TUI streams for real-time output
            # This must happen BEFORE the TUI starts to ensure universal capture
            tui_stdout = TUIStream(state)
            tui_stderr = TUIStream(state, prefix="[ERROR] ")

            # Save and redirect streams BEFORE calling run_tui
            # This ensures stdout is captured from the very beginning
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = tui_stdout
            sys.stderr = tui_stderr

            try:
                # Create a wrapped version that executes the function
                def captured_func():
                    try:
                        result = func(*args, **kwargs)

                        # Flush any remaining output
                        tui_stdout.flush()
                        tui_stderr.flush()

                        return result
                    except Exception as e:
                        state.add_log(f"[EXCEPTION] {str(e)}")
                        raise

                if auto_run:
                    return run_tui(captured_func, title=title, **app_kwargs)
                else:
                    return captured_func()
            finally:
                # Always restore original streams
                sys.stdout = old_stdout
                sys.stderr = old_stderr

        return wrapper
    return decorator


def tui_args(parser: Optional[argparse.ArgumentParser] = None) -> Callable:
    """
    Decorator to integrate argparse with TUI.

    This decorator creates a TUI interface for setting command-line arguments
    before execution.

    Args:
        parser: An argparse.ArgumentParser instance

    Usage:
        parser = argparse.ArgumentParser()
        parser.add_argument('--name', default='World')

        @tui_args(parser)
        def main(args):
            print(f"Hello {args.name}")
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            state = ExecutionState()

            # TODO: Implement TUI-based argument configuration
            # For now, just parse sys.argv
            if parser:
                parsed_args = parser.parse_args()
                state.set_metadata("cli_args", vars(parsed_args))
                return func(parsed_args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper
    return decorator


def tui_graph(variable_name: str, title: Optional[str] = None) -> Callable:
    """
    Decorator to track and graph a variable over time.

    This decorator should be used on methods/functions that update a variable.
    The variable's history will be tracked and displayed as a graph.

    Args:
        variable_name: Name of the variable to track
        title: Optional title for the graph widget

    Usage:
        @tui_graph("loss")
        def update_loss(self, loss_value):
            self.loss = loss_value
    """
    def decorator(func: Callable) -> Callable:
        state = ExecutionState()

        # Register the widget
        widget_config = WidgetConfig(
            widget_type="graph",
            name=title or f"Graph: {variable_name}",
            variable_name=variable_name,
        )
        state.register_widget(widget_config)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # Try to extract the variable value
            # Check in the instance (self) if it's a method
            if args and hasattr(args[0], variable_name):
                value = getattr(args[0], variable_name)
                state.update_metric(variable_name, value)
            # Check in kwargs
            elif variable_name in kwargs:
                state.update_metric(variable_name, kwargs[variable_name])
            # Check in local variables if we can
            else:
                frame = inspect.currentframe()
                if frame and frame.f_back:
                    local_vars = frame.f_back.f_locals
                    if variable_name in local_vars:
                        state.update_metric(variable_name, local_vars[variable_name])

            return result

        return wrapper
    return decorator


def gauge(
    variable_name: str,
    min_value: float = 0,
    max_value: float = 100,
    title: Optional[str] = None
) -> Callable:
    """
    Decorator to display a gauge for a variable.

    Unlike tui_graph, this doesn't track history, just shows current value.

    Args:
        variable_name: Name of the variable to display
        min_value: Minimum value for the gauge
        max_value: Maximum value for the gauge
        title: Optional title for the gauge widget

    Usage:
        @gauge("progress", min_value=0, max_value=100)
        def update_progress(self, value):
            self.progress = value
    """
    def decorator(func: Callable) -> Callable:
        state = ExecutionState()

        # Register the widget
        widget_config = WidgetConfig(
            widget_type="gauge",
            name=title or f"Gauge: {variable_name}",
            variable_name=variable_name,
            metadata={"min_value": min_value, "max_value": max_value}
        )
        state.register_widget(widget_config)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # Extract and update the variable value
            if args and hasattr(args[0], variable_name):
                value = getattr(args[0], variable_name)
                state.update_metric(variable_name, value)
            elif variable_name in kwargs:
                state.update_metric(variable_name, kwargs[variable_name])

            return result

        return wrapper
    return decorator


def execution_info(**metadata: Any) -> Callable:
    """
    Decorator to add execution metadata.

    This decorator allows you to specify metadata about the execution
    that will be displayed in the TUI.

    Args:
        **metadata: Key-value pairs of metadata to display

    Usage:
        @execution_info(model="GPT-4", dataset="train.csv")
        def train_model():
            # training code
            pass
    """
    def decorator(func: Callable) -> Callable:
        state = ExecutionState()

        # Register the widget
        widget_config = WidgetConfig(
            widget_type="execution_info",
            name="Execution Info",
            metadata=metadata
        )
        state.register_widget(widget_config)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Set all metadata
            for key, value in metadata.items():
                state.set_metadata(key, value)

            return func(*args, **kwargs)

        return wrapper
    return decorator


def progress(description: str = "", total: Optional[int] = None, level: int = 0) -> Callable:
    """
    Decorator to track progress of loops.

    This decorator wraps tqdm-like functionality, properly handling
    nested progress bars.

    Args:
        description: Description of the progress
        total: Total iterations (if not using range/iterable)
        level: Nesting level for nested progress bars

    Usage:
        @progress(description="Training", total=100)
        def train():
            for i in range(100):
                # training code
                pass
    """
    def decorator(func: Callable) -> Callable:
        state = ExecutionState()

        # Register the widget
        widget_config = WidgetConfig(
            widget_type="progress",
            name=description or func.__name__,
            metadata={"total": total, "level": level}
        )
        state.register_widget(widget_config)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # This is a simplified version
            # In a full implementation, this would integrate with tqdm
            state.set_metadata(f"progress_{func.__name__}", "started")

            try:
                result = func(*args, **kwargs)
                state.set_metadata(f"progress_{func.__name__}", "completed")
                return result
            except Exception:
                state.set_metadata(f"progress_{func.__name__}", "failed")
                raise

        return wrapper
    return decorator
