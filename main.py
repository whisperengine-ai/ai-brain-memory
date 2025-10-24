#!/usr/bin/env python3
"""Main entry point for AI Brain chat interface."""

from ai_brain.cli import main
from ai_brain.device_utils import print_device_info

if __name__ == "__main__":
    # Show device information on startup
    print_device_info()
    print()
    
    # Run main CLI
    main()
