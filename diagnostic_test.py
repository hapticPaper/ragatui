#!/usr/bin/env python3
"""
Diagnostic test for ragatui real-time streaming.

This script helps diagnose why output might not appear in real-time.
Run this and report what you see.
"""

import time
from ragatui import tui_app


@tui_app(title="DIAGNOSTIC: Real-Time Streaming Test")
def diagnostic_test():
    """
    This test prints messages with clear timestamps and delays.
    
    EXPECTED BEHAVIOR:
    - You should see "Starting..." immediately when the TUI loads
    - Each numbered line should appear approximately 1 second apart
    - The screen should NOT be blank - you should see output streaming
    
    ACTUAL BEHAVIOR:
    - Report what you actually see and when
    """
    print("=" * 70)
    print("DIAGNOSTIC TEST FOR REAL-TIME OUTPUT STREAMING")
    print("=" * 70)
    print()
    print("Starting diagnostic test...")
    print(f"Current time: {time.strftime('%H:%M:%S')}")
    print()
    print("If you can see this immediately, real-time output is working!")
    print("If you only see this after all lines appear, there's an issue.")
    print()
    
    for i in range(1, 6):
        print(f"--- Waiting 1 second before line {i} ---")
        time.sleep(1.0)
        print(f">>> LINE {i} appeared at {time.strftime('%H:%M:%S')}")
        print()
    
    print("=" * 70)
    print("DIAGNOSTIC TEST COMPLETE")
    print("=" * 70)
    print()
    print("QUESTIONS TO ANSWER:")
    print("1. Did you see 'Starting diagnostic test...' immediately?")
    print("2. Did lines 1-5 appear one at a time, or all at once at the end?")
    print("3. Was the screen blank during the 5-second execution?")
    print("4. What terminal/emulator are you using?")
    print("5. Are you running locally or over SSH?")
    
    return "diagnostic_complete"


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RAGATUI DIAGNOSTIC TEST")
    print("=" * 70)
    print()
    print("This test will:")
    print("  1. Open a TUI window")
    print("  2. Print messages with 1-second delays between them")
    print("  3. Test if output streams in real-time")
    print()
    print("Watch carefully:")
    print("  - Do you see output appearing line-by-line during execution?")
    print("  - Or does everything appear at once after 5+ seconds?")
    print()
    print("Starting in 3 seconds...")
    print()
    time.sleep(3)
    
    diagnostic_test()
