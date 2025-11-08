"""Advanced example demonstrating comprehensive monitoring with ragatui."""

import time
import random
from ragatui import tui_app, tui_graph, gauge, execution_info
from ragatui.utils.logging import setup_logging
from ragatui.core.state import ExecutionState


class AdvancedMLPipeline:
    """Simulates a complex ML pipeline with multiple stages."""

    def __init__(self):
        self.epoch = 0
        self.train_loss = 1.0
        self.val_loss = 1.0
        self.train_accuracy = 0.0
        self.val_accuracy = 0.0
        self.learning_rate = 0.001
        self.samples_processed = 0

        # Setup logging integration
        setup_logging()

    @tui_graph("train_loss")
    def update_train_loss(self, value):
        """Update training loss."""
        self.train_loss = value

    @tui_graph("val_loss")
    def update_val_loss(self, value):
        """Update validation loss."""
        self.val_loss = value

    @gauge("train_accuracy", min_value=0, max_value=100)
    def update_train_accuracy(self, value):
        """Update training accuracy."""
        self.train_accuracy = value

    @gauge("val_accuracy", min_value=0, max_value=100)
    def update_val_accuracy(self, value):
        """Update validation accuracy."""
        self.val_accuracy = value

    @gauge("learning_rate", min_value=0, max_value=0.01, title="Learning Rate")
    def update_learning_rate(self, value):
        """Update learning rate."""
        self.learning_rate = value

    def data_preprocessing(self):
        """Simulate data preprocessing stage."""
        print("=" * 50)
        print("Stage 1: Data Preprocessing")
        print("=" * 50)

        steps = ["Loading dataset", "Normalizing features", "Train/test split", "Creating batches"]

        for step in steps:
            print(f"  {step}...")
            time.sleep(0.5)

        print("  ✓ Preprocessing complete!\n")

    def model_training(self, epochs=5):
        """Simulate model training with monitoring."""
        print("=" * 50)
        print("Stage 2: Model Training")
        print("=" * 50)

        for epoch in range(epochs):
            self.epoch = epoch + 1
            print(f"\nEpoch {self.epoch}/{epochs}")
            print("-" * 30)

            # Training phase
            for batch in range(10):
                # Simulate decreasing loss
                train_loss = 1.0 * (1 - (epoch * 10 + batch) / (epochs * 10))
                train_loss += random.uniform(0, 0.1)
                self.update_train_loss(train_loss)

                # Simulate increasing accuracy
                train_acc = 100 * ((epoch * 10 + batch) / (epochs * 10))
                train_acc += random.uniform(-5, 5)
                train_acc = max(0, min(100, train_acc))
                self.update_train_accuracy(train_acc)

                self.samples_processed += 32  # Batch size

                if batch % 3 == 0:
                    print(
                        f"  Batch {batch + 1}/10: loss={train_loss:.4f}, "
                        f"acc={train_acc:.2f}%"
                    )

                time.sleep(0.2)

            # Validation phase
            val_loss = train_loss + random.uniform(-0.05, 0.1)
            val_acc = train_acc + random.uniform(-3, 3)
            val_acc = max(0, min(100, val_acc))

            self.update_val_loss(val_loss)
            self.update_val_accuracy(val_acc)

            # Update learning rate (decay)
            lr = 0.001 * (0.9**epoch)
            self.update_learning_rate(lr)

            print(
                f"  Validation: loss={val_loss:.4f}, acc={val_acc:.2f}%, "
                f"lr={lr:.6f}"
            )

        print("\n  ✓ Training complete!\n")

    def model_evaluation(self):
        """Simulate model evaluation."""
        print("=" * 50)
        print("Stage 3: Model Evaluation")
        print("=" * 50)

        metrics = [
            ("Precision", random.uniform(0.85, 0.95)),
            ("Recall", random.uniform(0.80, 0.90)),
            ("F1 Score", random.uniform(0.82, 0.92)),
            ("AUC-ROC", random.uniform(0.88, 0.98)),
        ]

        for metric_name, value in metrics:
            print(f"  {metric_name}: {value:.4f}")
            time.sleep(0.3)

        print("\n  ✓ Evaluation complete!\n")

        return metrics


@tui_app(title="Advanced ML Pipeline Monitor")
@execution_info(
    model="ResNet50",
    dataset="CIFAR-10",
    optimizer="Adam",
    batch_size=32,
    framework="PyTorch",
)
def run_pipeline():
    """Run the complete ML pipeline."""
    print("Starting Advanced ML Pipeline")
    print("=" * 50)
    print()

    # Create pipeline
    pipeline = AdvancedMLPipeline()

    # Store pipeline info
    state = ExecutionState()
    state.set_metadata("pipeline_version", "2.0")
    state.set_metadata("gpu_enabled", True)

    # Run pipeline stages
    try:
        pipeline.data_preprocessing()
        pipeline.model_training(epochs=5)
        results = pipeline.model_evaluation()

        # Final summary
        print("=" * 50)
        print("Pipeline Complete!")
        print("=" * 50)
        print(f"Total samples processed: {pipeline.samples_processed}")
        print(f"Final validation accuracy: {pipeline.val_accuracy:.2f}%")
        print(f"Final validation loss: {pipeline.val_loss:.4f}")
        print()

        return {
            "status": "success",
            "samples_processed": pipeline.samples_processed,
            "final_accuracy": pipeline.val_accuracy,
            "final_loss": pipeline.val_loss,
            "evaluation_metrics": results,
        }

    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {str(e)}")
        return {"status": "failed", "error": str(e)}


if __name__ == "__main__":
    result = run_pipeline()
    print(f"\nFinal result: {result}")
