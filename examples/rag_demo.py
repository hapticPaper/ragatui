"""Example demonstrating RAG functionality."""

import time
import random
from ragatui import tui_app, tui_graph, gauge, execution_info

class TrainingSimulator:
    def __init__(self):
        self.loss = 1.0
        self.accuracy = 0.0
    
    @tui_graph("loss")
    def update_loss(self, value):
        self.loss = value
    
    @gauge("accuracy", min_value=0, max_value=100)
    def update_accuracy(self, value):
        self.accuracy = value
    
    @execution_info(model="RAG-Demo-Model", dataset="Synthetic")
    def train(self, epochs=3):
        print(f"Starting training for {epochs} epochs...")
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            
            # Simulate training steps
            for step in range(3):
                loss = 1.0 * (1 - (epoch * 3 + step) / (epochs * 3)) + random.uniform(0, 0.1)
                self.update_loss(loss)
                
                acc = 100 * ((epoch * 3 + step) / (epochs * 3)) + random.uniform(-5, 5)
                acc = max(0, min(100, acc))
                self.update_accuracy(acc)
                
                print(f"  Step {step + 1}: loss={loss:.4f}, accuracy={acc:.2f}%")
                time.sleep(0.5)
        
        print(f"\nTraining complete! Final accuracy: {self.accuracy:.2f}%")
        return {"final_loss": self.loss, "final_accuracy": self.accuracy}

@tui_app(title="RAG Demo")
def main():
    simulator = TrainingSimulator()
    results = simulator.train(epochs=3)
    return results

if __name__ == "__main__":
    main()
