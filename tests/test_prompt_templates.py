"""Test system prompt template loading."""

import os
import tempfile
from pathlib import Path
from ai_brain.config import Config


def test_default_prompt():
    """Test that default prompt loads when no env vars are set."""
    # Clear any existing env vars
    if 'SYSTEM_PROMPT' in os.environ:
        del os.environ['SYSTEM_PROMPT']
    if 'SYSTEM_PROMPT_FILE' in os.environ:
        del os.environ['SYSTEM_PROMPT_FILE']
    
    # Reset Config.SYSTEM_PROMPT
    Config.SYSTEM_PROMPT = None
    Config.validate()
    
    assert Config.SYSTEM_PROMPT is not None
    assert "persistent memory" in Config.SYSTEM_PROMPT.lower()
    print("✓ Default prompt loaded successfully")


def test_env_variable_prompt():
    """Test loading prompt from SYSTEM_PROMPT env variable."""
    custom_prompt = "This is a custom test prompt from environment variable."
    os.environ['SYSTEM_PROMPT'] = custom_prompt
    
    # Reset and reload
    Config.SYSTEM_PROMPT = None
    Config.validate()
    
    assert Config.SYSTEM_PROMPT == custom_prompt
    print("✓ Environment variable prompt loaded successfully")
    
    # Cleanup
    del os.environ['SYSTEM_PROMPT']


def test_file_prompt():
    """Test loading prompt from file."""
    # Create a temporary prompt file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        test_prompt = "This is a test prompt loaded from a file."
        f.write(test_prompt)
        temp_file = f.name
    
    try:
        os.environ['SYSTEM_PROMPT_FILE'] = temp_file
        
        # Reset and reload
        Config.SYSTEM_PROMPT = None
        Config.validate()
        
        assert Config.SYSTEM_PROMPT == test_prompt
        print("✓ File-based prompt loaded successfully")
    finally:
        # Cleanup
        os.unlink(temp_file)
        del os.environ['SYSTEM_PROMPT_FILE']


def test_template_files_exist():
    """Test that template files exist and are readable."""
    templates_dir = Path(__file__).parent.parent / "templates"
    
    expected_templates = [
        "system_prompt.txt",
        "system_prompt_professional.txt",
        "system_prompt_creative.txt",
        "system_prompt_technical.txt"
    ]
    
    for template in expected_templates:
        template_path = templates_dir / template
        assert template_path.exists(), f"Template not found: {template}"
        
        # Verify it's readable and not empty
        content = template_path.read_text()
        assert len(content) > 0, f"Template is empty: {template}"
        print(f"✓ Template exists and is readable: {template}")


def test_relative_path_resolution():
    """Test that relative paths are resolved correctly."""
    os.environ['SYSTEM_PROMPT_FILE'] = 'templates/system_prompt.txt'
    
    try:
        # Reset and reload
        Config.SYSTEM_PROMPT = None
        Config.validate()
        
        assert Config.SYSTEM_PROMPT is not None
        assert len(Config.SYSTEM_PROMPT) > 0
        print("✓ Relative path resolved successfully")
    finally:
        # Cleanup
        del os.environ['SYSTEM_PROMPT_FILE']


if __name__ == '__main__':
    print("\n=== Testing System Prompt Template Loading ===\n")
    
    test_default_prompt()
    test_env_variable_prompt()
    test_file_prompt()
    test_template_files_exist()
    test_relative_path_resolution()
    
    print("\n✅ All prompt template tests passed!\n")
