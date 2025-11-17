"""Example demonstrating ragatui with Ollama (local LLM)."""

import time
import random
from ragatui import tui_app, tui_graph, gauge, configure_llm


# Configure Ollama before running the app
# This tells ragatui to use your local Ollama instance
configure_llm(
    provider="local",
    endpoint="http://localhost:11434",  # Default Ollama endpoint
    model="llama2"  # Or any other model you have installed
)


class ModelTraining:
    """Simulates model training with LLM monitoring."""

    def __init__(self):
        self.loss = 1.0
        self.accuracy = 0.0

    @tui_graph("loss")
    def update_loss(self, value):
        """Update training loss."""
        self.loss = value

    @gauge("accuracy", min_value=0, max_value=100)
    def update_accuracy(self, value):
        """Update accuracy."""
        self.accuracy = value


@tui_app(title="Training with Ollama")
def train_with_monitoring():
    """Train a model with ragatui monitoring."""
    print("Starting training with Ollama-powered monitoring...")
    print(f"LLM: Ollama (http://localhost:11434)")
    print()

    trainer = ModelTraining()

    for epoch in range(5):
        print(f"Epoch {epoch + 1}/5")

        for step in range(10):
            # Simulate training
            loss = 1.0 * (1 - (epoch * 10 + step) / 50) + random.uniform(0, 0.05)
            acc = 100 * ((epoch * 10 + step) / 50) + random.uniform(-2, 2)
            acc = max(0, min(100, acc))

            trainer.update_loss(loss)
            trainer.update_accuracy(acc)

            if step % 3 == 0:
                print(f"  Step {step + 1}: loss={loss:.4f}, acc={acc:.2f}%")

            time.sleep(0.2)

    print()
    print("Training complete!")
    print(f"Final accuracy: {trainer.accuracy:.2f}%")

    return {"final_loss": trainer.loss, "final_accuracy": trainer.accuracy}


if __name__ == "__main__":
    # Note: LLM analysis is currently a stub and will be implemented in future versions
    # For now, ragatui will still show your metrics and output in real-time!
    result = train_with_monitoring()
    print(f"\nResult: {result}")
