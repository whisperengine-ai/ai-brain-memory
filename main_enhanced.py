#!/usr/bin/env python3
"""Main entry point for AI Brain - Enhanced with LangChain and LlamaIndex."""

import sys

def main():
    """Main entry point with mode selection."""
    # Check for mode flags
    if "--enhanced" in sys.argv or "--langchain" in sys.argv or "--lc" in sys.argv:
        print("🚀 Starting Enhanced Mode (LangChain + LlamaIndex)")
        from ai_brain.enhanced_cli import main as enhanced_main
        enhanced_main()
    else:
        print("🚀 Starting Basic Mode")
        print("💡 Tip: Use --enhanced for LangChain and LlamaIndex features")
        from ai_brain.cli import main as basic_main
        basic_main()


if __name__ == "__main__":
    main()
