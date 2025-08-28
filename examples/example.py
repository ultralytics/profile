#!/usr/bin/env python3
"""Example script to demonstrate profiling."""

import time
import random


def slow_function():
    """A deliberately slow function."""
    time.sleep(0.1)
    return sum(random.random() for _ in range(1000))


def fast_function():
    """A fast function called many times."""
    return random.random() * 2


def main():
    """Main function."""
    print("Starting example script...")
    
    # Call slow function once
    result1 = slow_function()
    print(f"Slow function result: {result1:.4f}")
    
    # Call fast function many times
    results = []
    for i in range(1000):
        results.append(fast_function())
    
    print(f"Fast function called {len(results)} times")
    print(f"Average result: {sum(results) / len(results):.4f}")
    print("Script completed!")


if __name__ == "__main__":
    main()
