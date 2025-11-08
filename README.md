# ragatui

A modular code execution TUI (Text User Interface) for Python with LLM-powered monitoring.

## Overview

**ragatui** makes it incredibly easy to turn your normal Python code with logging into a beautiful TUI application. Simply add decorators to your existing code, and ragatui will:

- 🎨 Create an interactive TUI to visualize your script's execution
- 📊 Capture and display output in organized widgets
- 🔍 Use LLMs to analyze logs in near real-time and extract key metrics
- 📈 Track variables over time with automatic graphing
- 🎯 Monitor progress with nested progress bars
- 🔧 Provide a modular system for custom widgets and extensions

Perfect for ML training scripts, data processing pipelines, and any long-running Python process where you want better visibility!

## Features

### Core Decorators

- **`@tui_app`** - Convert any function into a TUI application
- **`@tui_args`** - Integrate argparse with TUI-based configuration
- **`@tui_graph`** - Track and graph variables over time
- **`@gauge`** - Display current values as gauges
- **`@execution_info`** - Display execution metadata
- **`@progress`** - Wrap tqdm with proper nesting support

### Architecture

- **Two-pane layout**: Output/logs on the left, key metrics on the right
- **LLM-powered analysis**: Optional integration with OpenAI, Anthropic, or local LLMs
- **RAG integration**: Store execution history and compare runs
- **Modular widgets**: Easy to add custom widgets
- **Agentic development support**: Designed for LangGraph, PydanticAI, and complex pipelines

## Installation

```bash
pip install ragatui
```

For LLM features:
```bash
pip install ragatui[llm]
```

For RAG features:
```bash
pip install ragatui[rag]
```

For agentic development support:
```bash
pip install ragatui[agentic]
```

## Setup

### Basic Usage (No LLM Required)

ragatui works out of the box without any LLM configuration! Simply use the decorators and you'll get:
- Real-time output capture in the TUI
- Automatic metric tracking
- Progress monitoring
- Execution metadata display

### Configuring Local LLM (Ollama)

If you have Ollama running locally, configure ragatui to use it:

```python
from ragatui import configure_llm, tui_app

# Configure Ollama before your app
configure_llm(
    provider="local",
    endpoint="http://localhost:11434",  # Default Ollama endpoint
    model="llama2"  # Or any model you have installed
)

@tui_app(title="My App")
def main():
    print("Running with Ollama monitoring!")
    # Your code here
```

### Configuring Cloud LLMs

For OpenAI:
```python
from ragatui import configure_llm

configure_llm(
    provider="openai",
    model="gpt-4",
    api_key="sk-..."  # Your OpenAI API key
)
```

### Environment Variables

You can also configure via environment variables:

```bash
# .env file
RAGATUI_LLM_PROVIDER=local
RAGATUI_LLM_ENDPOINT=http://localhost:11434
RAGATUI_LLM_MODEL=llama2
```

Then just run your script - ragatui will pick up the configuration automatically!

## Quick Start

### Basic Example

```python
from ragatui import tui_app

@tui_app(title="My Script")
def main():
    print("Hello from ragatui!")
    # Your code here
    return "Done"

if __name__ == "__main__":
    main()
```

### Tracking Metrics

```python
from ragatui import tui_app, tui_graph, gauge

class Trainer:
    def __init__(self):
        self.loss = 1.0
        self.accuracy = 0.0
    
    @tui_graph("loss")
    def update_loss(self, value):
        self.loss = value
    
    @gauge("accuracy", min_value=0, max_value=100)
    def update_accuracy(self, value):
        self.accuracy = value

@tui_app(title="Training Monitor")
def train():
    trainer = Trainer()
    for epoch in range(10):
        # Training logic
        trainer.update_loss(loss_value)
        trainer.update_accuracy(acc_value)
```

### With Argparse

```python
import argparse
from ragatui import tui_app, tui_args

parser = argparse.ArgumentParser()
parser.add_argument('--epochs', type=int, default=10)

@tui_app(title="Training")
@tui_args(parser)
def train(args):
    print(f"Training for {args.epochs} epochs")
    # Your training code
```

## Advanced Usage

### Custom Widgets

```python
from ragatui.core.registry import WidgetRegistry
from textual.widget import Widget

class MyCustomWidget(Widget):
    # Your widget implementation
    pass

# Register your widget
registry = WidgetRegistry()
registry.register_widget("my_widget", MyCustomWidget)
```

### LLM Integration

```python
from ragatui.llm import get_llm_provider, LLMProviderType

# Use OpenAI
provider = get_llm_provider(
    LLMProviderType.OPENAI,
    config={"api_key": "your-key", "model": "gpt-4"}
)

# Or use a local LLM
provider = get_llm_provider(
    LLMProviderType.LOCAL,
    config={"endpoint": "http://localhost:11434"}
)
```

### RAG Setup

```python
from ragatui.rag import setup_rag_environment, generate_docker_compose

# Setup with ChromaDB
env_vars = setup_rag_environment(provider="chromadb", docker=True)

# Generate docker-compose.yml
generate_docker_compose(provider="chromadb")

# Then run: docker-compose up -d
```

## Use Cases

### Machine Learning Training

Monitor your ML training runs with automatic metric extraction, loss curves, and accuracy tracking:

```python
from ragatui import tui_app, tui_graph, execution_info

@tui_app(title="Model Training")
@execution_info(model="ResNet50", dataset="ImageNet")
def train_model():
    # Your training loop with automatic monitoring
    pass
```

### Data Processing Pipelines

Track progress through complex data processing with nested progress bars:

```python
from ragatui import tui_app
from ragatui.utils.progress import progress

@tui_app(title="Data Pipeline")
def process_data():
    for file in progress(files, desc="Files"):
        for batch in progress(batches, desc="Batches", level=1):
            # Process batch
            pass
```

### Agentic Workflows

Monitor LangGraph or PydanticAI executions with structured logging:

```python
from ragatui import tui_app
from langgraph import Graph

@tui_app(title="Agent Workflow")
def run_agent():
    graph = Graph()
    # Your agent workflow with automatic TUI
    result = graph.run()
    return result
```

## Architecture & Design

### State Management

ragatui uses a singleton `ExecutionState` to manage:
- Tracked metrics and their history
- Widget configurations
- Log messages
- Execution metadata

### Widget System

All widgets inherit from Textual's `Widget` class and can be:
- Registered in the `WidgetRegistry`
- Created with factory functions
- Customized and extended

### LLM Analysis

The `LogAnalyzer` runs in the background, periodically:
1. Collecting recent logs
2. Analyzing them with your chosen LLM
3. Extracting key metrics and insights
4. Updating the TUI with findings

### RAG Integration

The optional RAG database:
- Stores execution history
- Enables comparison across runs
- Provides context for LLM analysis
- Supports vector similarity search

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
black ragatui/
ruff check ragatui/
```

### Type Checking

```bash
mypy ragatui/
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Roadmap

- [ ] Full LLM integration with streaming analysis
- [ ] Complete RAG database implementation
- [ ] TUI-based configuration interface
- [ ] LangGraph/PydanticAI visualization components
- [ ] Real-time collaboration features
- [ ] Plugin system for extensions
- [ ] Cloud deployment support

## Support

- 📖 [Documentation](https://github.com/hapticPaper/ragatui/wiki)
- 🐛 [Issue Tracker](https://github.com/hapticPaper/ragatui/issues)
- 💬 [Discussions](https://github.com/hapticPaper/ragatui/discussions)

## Acknowledgments

Built with:
- [Textual](https://github.com/Textualize/textual) - TUI framework
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [structlog](https://github.com/hynek/structlog) - Structured logging
- [tqdm](https://github.com/tqdm/tqdm) - Progress bars 
