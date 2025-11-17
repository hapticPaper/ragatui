"""Basic example demonstrating ragatui decorators."""

import time
import random
from ragatui import tui_app, tui_graph, gauge, execution_info


class TrainingSimulator:
    """Simulates a machine learning training process."""
    
    def __init__(self):
        self.loss = 1.0
        self.accuracy = 0.0
        self.epoch = 0
    
    @tui_graph("loss")
    def update_loss(self, value):
        """Update the loss metric."""
        self.loss = value
    
    @gauge("accuracy", min_value=0, max_value=100)
    def update_accuracy(self, value):
        """Update the accuracy metric."""
        self.accuracy = value
    
    @execution_info(model="ResNet50", dataset="ImageNet", batch_size=32)
    def train(self, epochs=10):
        """Simulate training for specified epochs."""
        print(f"Starting training for {epochs} epochs...")
        
        for epoch in range(epochs):
            self.epoch = epoch + 1
            print(f"\nEpoch {self.epoch}/{epochs}")
            
            # Simulate training steps
            for step in range(5):
                # Simulate decreasing loss
                loss = 1.0 * (1 - (epoch * 5 + step) / (epochs * 5)) + random.uniform(0, 0.1)
                self.update_loss(loss)
                
                # Simulate increasing accuracy
                acc = 100 * ((epoch * 5 + step) / (epochs * 5)) + random.uniform(-5, 5)
                acc = max(0, min(100, acc))
                self.update_accuracy(acc)
                
                print(f"  Step {step + 1}: loss={loss:.4f}, accuracy={acc:.2f}%")
                time.sleep(0.5)
        
        print(f"\nTraining complete! Final accuracy: {self.accuracy:.2f}%")
        return {"final_loss": self.loss, "final_accuracy": self.accuracy}


@tui_app(title="ML Training Monitor")
def main():
    """Main function to run the training simulation."""
    simulator = TrainingSimulator()
    results = simulator.train(epochs=5)
    return results


if __name__ == "__main__":
    main()
