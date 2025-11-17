"""Tests for WidgetRegistry."""

import pytest
from textual.widget import Widget
from ragatui.core.registry import WidgetRegistry


class TestWidget(Widget):
    """Test widget class."""
    pass


class AnotherWidget(Widget):
    """Another test widget class."""
    def __init__(self, title: str = "Test", **kwargs):
        super().__init__(**kwargs)
        self.title = title


def test_widget_registry_singleton():
    """Test that WidgetRegistry is a singleton."""
    registry1 = WidgetRegistry()
    registry2 = WidgetRegistry()
    assert registry1 is registry2


def test_register_widget():
    """Test widget registration."""
    registry = WidgetRegistry()
    
    # Clear any existing widgets
    for name in registry.list_widgets():
        registry.unregister_widget(name)
    
    registry.register_widget("test_widget", TestWidget)
    
    assert "test_widget" in registry.list_widgets()
    assert registry.get_widget_class("test_widget") == TestWidget


def test_create_widget():
    """Test widget creation."""
    registry = WidgetRegistry()
    registry.register_widget("test_widget", TestWidget)
    
    widget = registry.create_widget("test_widget")
    assert widget is not None
    assert isinstance(widget, TestWidget)


def test_create_widget_with_args():
    """Test widget creation with arguments."""
    registry = WidgetRegistry()
    registry.register_widget("another_widget", AnotherWidget)
    
    widget = registry.create_widget("another_widget", title="Custom Title")
    assert widget is not None
    assert isinstance(widget, AnotherWidget)
    assert widget.title == "Custom Title"


def test_create_widget_with_factory():
    """Test widget creation with factory function."""
    registry = WidgetRegistry()
    
    def widget_factory(custom_param: str = "default"):
        widget = AnotherWidget(title=custom_param)
        return widget
    
    registry.register_widget("factory_widget", AnotherWidget, factory=widget_factory)
    
    widget = registry.create_widget("factory_widget", custom_param="Factory Title")
    assert widget is not None
    assert widget.title == "Factory Title"


def test_get_nonexistent_widget():
    """Test getting a widget that doesn't exist."""
    registry = WidgetRegistry()
    
    widget_class = registry.get_widget_class("nonexistent")
    assert widget_class is None
    
    widget = registry.create_widget("nonexistent")
    assert widget is None


def test_unregister_widget():
    """Test unregistering a widget."""
    registry = WidgetRegistry()
    registry.register_widget("temp_widget", TestWidget)
    
    assert "temp_widget" in registry.list_widgets()
    
    registry.unregister_widget("temp_widget")
    
    assert "temp_widget" not in registry.list_widgets()


def test_list_widgets():
    """Test listing all registered widgets."""
    registry = WidgetRegistry()
    
    # Clear existing
    for name in registry.list_widgets():
        registry.unregister_widget(name)
    
    registry.register_widget("widget1", TestWidget)
    registry.register_widget("widget2", AnotherWidget)
    
    widgets = registry.list_widgets()
    assert len(widgets) == 2
    assert "widget1" in widgets
    assert "widget2" in widgets
