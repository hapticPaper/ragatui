"""Tests for decorators."""

import pytest
from ragatui.decorators import tui_graph, gauge, execution_info
from ragatui.core.state import ExecutionState


class TestClass:
    """Test class for decorator testing."""
    
    def __init__(self):
        self.loss = 0.0
        self.accuracy = 0.0
    
    @tui_graph("loss")
    def update_loss(self, value):
        self.loss = value
    
    @gauge("accuracy", min_value=0, max_value=100)
    def update_accuracy(self, value):
        self.accuracy = value


def test_tui_graph_decorator():
    """Test tui_graph decorator."""
    state = ExecutionState()
    state.reset()
    
    obj = TestClass()
    obj.update_loss(0.5)
    
    # Check that metric was updated
    metric = state.get_metric("loss")
    assert metric is not None
    assert metric.value == 0.5
    
    # Update again
    obj.update_loss(0.3)
    metric = state.get_metric("loss")
    assert metric.value == 0.3
    assert len(metric.history) == 1


def test_gauge_decorator():
    """Test gauge decorator."""
    state = ExecutionState()
    state.reset()
    
    obj = TestClass()
    obj.update_accuracy(75.5)
    
    # Check that metric was updated
    metric = state.get_metric("accuracy")
    assert metric is not None
    assert metric.value == 75.5


def test_execution_info_decorator():
    """Test execution_info decorator."""
    state = ExecutionState()
    state.reset()
    
    @execution_info(model="GPT-4", dataset="test.csv")
    def test_func():
        return "done"
    
    result = test_func()
    
    assert result == "done"
    assert state.get_metadata("model") == "GPT-4"
    assert state.get_metadata("dataset") == "test.csv"


def test_widget_registration():
    """Test that decorators register widgets."""
    state = ExecutionState()
    
    # Get initial widget count
    initial_count = len(state.get_widgets())
    
    # Define a new class with decorators - this will register new widgets
    class NewTestClass:
        def __init__(self):
            self.test_metric = 0.0
        
        @tui_graph("test_metric_unique")
        def update_metric(self, value):
            self.test_metric = value
    
    # Check that a new widget was registered
    widgets = state.get_widgets()
    assert len(widgets) > initial_count
    
    # Check that our specific widget is there
    widget_names = [w.name for w in widgets]
    assert any("test_metric_unique" in name.lower() for name in widget_names)


def test_multiple_updates():
    """Test multiple metric updates maintain history."""
    state = ExecutionState()
    state.reset()
    
    obj = TestClass()
    
    values = [1.0, 0.8, 0.6, 0.4, 0.2]
    for val in values:
        obj.update_loss(val)
    
    metric = state.get_metric("loss")
    assert metric.value == 0.2
    assert len(metric.history) == len(values) - 1
