"""Tests for ExecutionState."""

import pytest
from ragatui.core.state import ExecutionState, MetricData, WidgetConfig


def test_execution_state_singleton():
    """Test that ExecutionState is a singleton."""
    state1 = ExecutionState()
    state2 = ExecutionState()
    assert state1 is state2


def test_update_and_get_metric():
    """Test updating and retrieving metrics."""
    state = ExecutionState()
    state.reset()  # Clear any previous state
    
    state.update_metric("loss", 0.5)
    metric = state.get_metric("loss")
    
    assert metric is not None
    assert metric.name == "loss"
    assert metric.value == 0.5
    assert len(metric.history) == 0
    
    # Update again
    state.update_metric("loss", 0.3)
    metric = state.get_metric("loss")
    
    assert metric.value == 0.3
    assert len(metric.history) == 1
    assert metric.history[0][1] == 0.5


def test_register_widget():
    """Test widget registration."""
    state = ExecutionState()
    state.reset()
    
    config = WidgetConfig(
        widget_type="graph",
        name="Loss Graph",
        variable_name="loss"
    )
    
    state.register_widget(config)
    widgets = state.get_widgets()
    
    assert len(widgets) == 1
    assert widgets[0].name == "Loss Graph"
    assert widgets[0].widget_type == "graph"


def test_add_and_get_logs():
    """Test adding and retrieving logs."""
    state = ExecutionState()
    state.reset()
    
    state.add_log("First log")
    state.add_log("Second log")
    
    logs = state.get_logs()
    assert len(logs) == 2
    assert logs[0] == "First log"
    assert logs[1] == "Second log"
    
    # Test with limit
    recent_logs = state.get_logs(limit=1)
    assert len(recent_logs) == 1
    assert recent_logs[0] == "Second log"


def test_metadata():
    """Test metadata storage and retrieval."""
    state = ExecutionState()
    state.reset()
    
    state.set_metadata("function_name", "test_func")
    state.set_metadata("epoch", 5)
    
    assert state.get_metadata("function_name") == "test_func"
    assert state.get_metadata("epoch") == 5
    
    all_metadata = state.get_metadata()
    assert "function_name" in all_metadata
    assert "epoch" in all_metadata


def test_get_all_metrics():
    """Test getting all metrics."""
    state = ExecutionState()
    state.reset()
    
    state.update_metric("loss", 0.5)
    state.update_metric("accuracy", 0.95)
    
    metrics = state.get_all_metrics()
    assert len(metrics) == 2
    assert "loss" in metrics
    assert "accuracy" in metrics


def test_reset():
    """Test state reset."""
    state = ExecutionState()
    
    state.update_metric("loss", 0.5)
    state.add_log("Test log")
    state.set_metadata("key", "value")
    
    state.reset()
    
    assert len(state.get_all_metrics()) == 0
    assert len(state.get_logs()) == 0
    assert len(state.get_metadata()) == 0
