#!/usr/bin/env python3
"""
Example script demonstrating system prompt template usage.

This shows how to programmatically load and switch between different
system prompts for different use cases.
"""

import os
from pathlib import Path
from ai_brain.config import Config

def demonstrate_prompt_loading():
    """Demonstrate different ways to load system prompts."""
    
    print("=" * 70)
    print("System Prompt Template Loading Demo")
    print("=" * 70)
    print()
    
    # Save original state
    original_prompt_file = os.environ.get('SYSTEM_PROMPT_FILE')
    original_prompt = os.environ.get('SYSTEM_PROMPT')
    
    try:
        # Demo 1: Default prompt
        print("1. Loading DEFAULT prompt (no configuration)")
        print("-" * 70)
        if 'SYSTEM_PROMPT_FILE' in os.environ:
            del os.environ['SYSTEM_PROMPT_FILE']
        if 'SYSTEM_PROMPT' in os.environ:
            del os.environ['SYSTEM_PROMPT']
        
        Config.SYSTEM_PROMPT = None
        Config.validate()
        
        print(f"Prompt loaded: {Config.SYSTEM_PROMPT[:100]}...")
        print(f"Length: {len(Config.SYSTEM_PROMPT)} characters")
        print()
        
        # Demo 2: Professional template
        print("2. Loading PROFESSIONAL template from file")
        print("-" * 70)
        os.environ['SYSTEM_PROMPT_FILE'] = 'templates/system_prompt_professional.txt'
        
        Config.SYSTEM_PROMPT = None
        Config.validate()
        
        print(f"Prompt loaded: {Config.SYSTEM_PROMPT[:100]}...")
        print(f"Length: {len(Config.SYSTEM_PROMPT)} characters")
        print()
        
        # Demo 3: Creative template
        print("3. Loading CREATIVE template from file")
        print("-" * 70)
        os.environ['SYSTEM_PROMPT_FILE'] = 'templates/system_prompt_creative.txt'
        
        Config.SYSTEM_PROMPT = None
        Config.validate()
        
        print(f"Prompt loaded: {Config.SYSTEM_PROMPT[:100]}...")
        print(f"Length: {len(Config.SYSTEM_PROMPT)} characters")
        print()
        
        # Demo 4: Technical template
        print("4. Loading TECHNICAL template from file")
        print("-" * 70)
        os.environ['SYSTEM_PROMPT_FILE'] = 'templates/system_prompt_technical.txt'
        
        Config.SYSTEM_PROMPT = None
        Config.validate()
        
        print(f"Prompt loaded: {Config.SYSTEM_PROMPT[:100]}...")
        print(f"Length: {len(Config.SYSTEM_PROMPT)} characters")
        print()
        
        # Demo 5: Environment variable
        print("5. Loading prompt from ENVIRONMENT VARIABLE")
        print("-" * 70)
        del os.environ['SYSTEM_PROMPT_FILE']
        os.environ['SYSTEM_PROMPT'] = "You are a concise AI that gives brief answers."
        
        Config.SYSTEM_PROMPT = None
        Config.validate()
        
        print(f"Prompt loaded: {Config.SYSTEM_PROMPT}")
        print(f"Length: {len(Config.SYSTEM_PROMPT)} characters")
        print()
        
    finally:
        # Restore original state
        if original_prompt_file:
            os.environ['SYSTEM_PROMPT_FILE'] = original_prompt_file
        elif 'SYSTEM_PROMPT_FILE' in os.environ:
            del os.environ['SYSTEM_PROMPT_FILE']
        
        if original_prompt:
            os.environ['SYSTEM_PROMPT'] = original_prompt
        elif 'SYSTEM_PROMPT' in os.environ:
            del os.environ['SYSTEM_PROMPT']
        
        # Reset to original
        Config.SYSTEM_PROMPT = None
        Config.validate()
    
    print("=" * 70)
    print("Demo complete!")
    print()
    print("To use templates in your own code:")
    print()
    print("  # Set environment variable before importing")
    print("  os.environ['SYSTEM_PROMPT_FILE'] = 'templates/your_template.txt'")
    print("  from ai_brain.config import Config")
    print("  Config.validate()")
    print()
    print("Or in .env file:")
    print("  SYSTEM_PROMPT_FILE=templates/system_prompt_professional.txt")
    print("=" * 70)


def list_available_templates():
    """List all available prompt templates."""
    templates_dir = Path(__file__).parent.parent / "templates"
    
    if not templates_dir.exists():
        print("Templates directory not found!")
        return
    
    print("\n📁 Available Prompt Templates:")
    print("-" * 70)
    
    templates = sorted(templates_dir.glob("system_prompt*.txt"))
    
    for template in templates:
        size = template.stat().st_size
        name = template.name
        
        # Read first line as description
        try:
            with open(template, 'r') as f:
                first_line = f.readline().strip()
            
            print(f"  • {name}")
            print(f"    Size: {size} bytes")
            print(f"    Preview: {first_line[:60]}...")
            print()
        except Exception as e:
            print(f"  • {name} (could not read: {e})")
            print()


if __name__ == '__main__':
    list_available_templates()
    print()
    demonstrate_prompt_loading()
