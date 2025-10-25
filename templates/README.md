# Prompt Templates

This directory contains editable prompt templates for the AI Brain system.

## Available Templates

### `system_prompt.txt`
The main system prompt that defines the AI assistant's personality, capabilities, and behavior guidelines.

**How to customize:**
1. Edit `system_prompt.txt` with your preferred system prompt
2. Set the environment variable: `SYSTEM_PROMPT_FILE=templates/system_prompt.txt`
3. Restart the AI Brain application

**Tips:**
- Keep the prompt clear and focused
- Include specific behavioral guidelines
- Test different prompts to see what works best for your use case

### Creating Custom Templates

You can create multiple template variations:
- `system_prompt_professional.txt` - For professional/business contexts
- `system_prompt_creative.txt` - For creative writing assistance
- `system_prompt_technical.txt` - For technical support
- `system_prompt_tutor.txt` - For educational/tutoring mode

Then switch between them by changing the `SYSTEM_PROMPT_FILE` environment variable.
