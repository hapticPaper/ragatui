from ragatui import tui_app, tui_graph, gauge, execution_info
import time

class Trainer:
    @tui_graph("loss")              # Tracks history, renders sparkline
    def update_loss(self, val):
        self.loss = val

    @gauge("accuracy", 0, 100)      # Current value with progress bar
    def update_acc(self, val):
        self.accuracy = val


@tui_app(title="Training")
@execution_info(model="ResNet50", dataset="CIFAR-10")
def train():
    trainer = Trainer()
    for epoch in range(10):
        trainer.update_loss(1.0 / (epoch + 1))
        trainer.update_acc(90 + epoch)
        print(f"Epoch {epoch + 1}/10 completed.")
        time.sleep(1)
    return "training_complete"


if __name__ == "__main__":
    train()