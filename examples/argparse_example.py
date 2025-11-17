"""Example demonstrating argparse integration with ragatui."""

import argparse
import time
from ragatui import tui_app, tui_args, execution_info


# Create argument parser
parser = argparse.ArgumentParser(description="Data processing script")
parser.add_argument("--input", type=str, default="data.csv", help="Input file")
parser.add_argument("--output", type=str, default="output.csv", help="Output file")
parser.add_argument("--iterations", type=int, default=10, help="Number of iterations")
parser.add_argument("--verbose", action="store_true", help="Verbose output")


@tui_app(title="Data Processor")
@tui_args(parser)
@execution_info(script="data_processor", version="1.0")
def process_data(args):
    """Process data with specified arguments."""
    print(f"Processing data from {args.input}")
    print(f"Output will be saved to {args.output}")
    print(f"Running {args.iterations} iterations")
    
    for i in range(args.iterations):
        if args.verbose:
            print(f"  Iteration {i + 1}/{args.iterations}: Processing...")
        time.sleep(0.3)
    
    print(f"\nProcessing complete! Results saved to {args.output}")
    return {"status": "success", "iterations": args.iterations}


if __name__ == "__main__":
    process_data()
