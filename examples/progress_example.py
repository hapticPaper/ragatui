"""Example demonstrating nested progress tracking."""

import time
from ragatui import tui_app
from ragatui.utils.progress import progress


@tui_app(title="Nested Progress Example")
def main():
    """Demonstrate nested progress bars."""
    print("Starting multi-level processing...")
    
    # Outer loop
    for i in progress(range(3), desc="Phases", level=0):
        print(f"\nPhase {i + 1}")
        time.sleep(0.5)
        
        # Middle loop
        for j in progress(range(5), desc=f"  Phase {i+1} Batches", level=1):
            print(f"  Processing batch {j + 1}")
            time.sleep(0.3)
            
            # Inner loop
            for k in progress(range(10), desc=f"    Items", level=2):
                time.sleep(0.05)
    
    print("\nAll processing complete!")
    return {"status": "success"}


if __name__ == "__main__":
    main()
