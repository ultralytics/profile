#!/usr/bin/env python3
"""Command-line interface for the profiler."""

import sys
from profile import profile_command


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: profile <command>")
        print("Examples:")
        print("  profile python script.py")
        print("  profile yolo predict model=yolo11n.pt source=image.jpg")
        print("  profile bash script.sh")
        sys.exit(1)
    
    command = " ".join(sys.argv[1:])
    profile_command(command)


if __name__ == "__main__":
    main()
