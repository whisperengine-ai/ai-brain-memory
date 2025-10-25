# System Prompt Templates Guide

This guide explains how to customize the AI Brain's personality and behavior using system prompt templates.

## Quick Start

### 1. Choose a Template

The project includes several pre-configured templates in the `templates/` directory:

- **`system_prompt.txt`** - Default balanced assistant (recommended for general use)
- **`system_prompt_professional.txt`** - Business/professional tone
- **`system_prompt_creative.txt`** - Creative writing and brainstorming
- **`system_prompt_technical.txt`** - Technical support and coding assistance

### 2. Configure in .env

Edit your `.env` file and add:

```bash
SYSTEM_PROMPT_FILE=templates/system_prompt.txt
```

Or choose a different template:

```bash
SYSTEM_PROMPT_FILE=templates/system_prompt_professional.txt
```

### 3. Restart the AI

```bash
python main.py
# or
python main_enhanced.py
```

You'll see a confirmation message:
```
✓ Loaded system prompt from: templates/system_prompt.txt
```

## How It Works

The system loads prompts in this priority order:

1. **File Template** (if `SYSTEM_PROMPT_FILE` is set)
2. **Environment Variable** (if `SYSTEM_PROMPT` is set)
3. **Default** (hardcoded in `config.py`)

## Customization Options

### Option 1: Edit Existing Templates (Easiest)

Simply edit the `.txt` files in the `templates/` directory:

```bash
# Mac/Linux
nano templates/system_prompt.txt

# Windows
notepad templates/system_prompt.txt
```

Changes take effect on next restart!

### Option 2: Create a New Template

1. Create a new file in `templates/`:
   ```bash
   touch templates/system_prompt_my_custom.txt
   ```

2. Add your custom prompt:
   ```
   You are a specialized AI assistant for [your use case].
   
   CAPABILITIES:
   - [List your specific capabilities]
   
   GUIDELINES:
   - [Your specific instructions]
   ```

3. Configure in `.env`:
   ```bash
   SYSTEM_PROMPT_FILE=templates/system_prompt_my_custom.txt
   ```

### Option 3: Set as Environment Variable

For quick testing or temporary changes:

```bash
export SYSTEM_PROMPT="You are a helpful AI assistant that..."
python main.py
```

Or add to `.env`:
```bash
SYSTEM_PROMPT="Your full prompt here..."
```

## Template Examples

### Professional Template
Best for: Business communications, formal interactions, productivity

Key features:
- Formal, business-appropriate tone
- Focus on clarity and actionability
- Professional communication style

### Creative Template
Best for: Creative writing, brainstorming, artistic projects

Key features:
- Enthusiastic and encouraging tone
- Exploratory and open-ended
- Celebrates creativity and experimentation

### Technical Template
Best for: Programming, system administration, technical support

Key features:
- Precise technical language
- Code examples when relevant
- Best practices and patterns
- Clear explanations

## Writing Effective Prompts

### Best Practices

1. **Be Specific**: Clearly define the AI's role and capabilities
2. **Set Boundaries**: Explain what the AI should and shouldn't do
3. **Provide Context**: Mention the memory and emotional intelligence features
4. **Use Structure**: Break into sections (CAPABILITIES, GUIDELINES, etc.)
5. **Test Iterations**: Try different prompts and see what works best

### Template Structure

```
[Role Definition]
You are a [type] AI assistant with [specific capabilities].

[Core Capabilities]
- Capability 1
- Capability 2
- Capability 3

[Behavioral Guidelines]
- Guideline 1
- Guideline 2
- Guideline 3

[Special Instructions]
- Any specific handling rules
- Edge case behaviors
- Tone/style preferences
```

### Example: Custom Study Assistant

```
You are an AI study assistant with persistent memory. You help users learn
and retain information through spaced repetition and contextual recall.

CORE CAPABILITIES:
- Memory of past study sessions and topics covered
- Understanding of user's learning style and pace
- Ability to quiz on previously learned material
- Tracking progress across study sessions

STUDY GUIDELINES:
- Break complex topics into digestible chunks
- Reference past lessons to reinforce learning
- Ask recall questions to test retention
- Adapt difficulty based on user's responses
- Celebrate learning milestones and progress
- Suggest review of older topics periodically

IMPORTANT:
- Always ask if the user understands before moving forward
- Provide examples and analogies when explaining concepts
- Connect new topics to previously learned material
- Be patient and encouraging with mistakes
```

## Advanced Features

### Multiple Prompt Profiles

Create different prompts for different tasks:

```bash
# Work mode
SYSTEM_PROMPT_FILE=templates/system_prompt_professional.txt
python main_enhanced.py

# Creative mode
SYSTEM_PROMPT_FILE=templates/system_prompt_creative.txt
python main_enhanced.py
```

### Dynamic Prompt Switching

You can switch prompts without restarting by changing the environment variable:

```bash
# In one terminal session
export SYSTEM_PROMPT_FILE=templates/system_prompt_professional.txt
python main.py

# In another session (different personality)
export SYSTEM_PROMPT_FILE=templates/system_prompt_creative.txt
python main.py
```

### Prompt Versioning

Keep versions of your prompts:

```bash
templates/
  system_prompt_v1.txt
  system_prompt_v2.txt
  system_prompt_v2_experimental.txt
```

Then test which version works best!

## Testing Your Prompt

After creating or editing a prompt:

1. **Restart the AI**:
   ```bash
   python main.py
   ```

2. **Verify it loaded**:
   Look for: `✓ Loaded system prompt from: templates/your_prompt.txt`

3. **Test the behavior**:
   - Try different types of questions
   - Check if tone matches your expectations
   - Verify it uses memory appropriately
   - Test edge cases

4. **Iterate**:
   - Edit the prompt based on results
   - Restart and test again
   - Compare with other templates

## Troubleshooting

### Prompt not loading

**Issue**: Changes to template file not taking effect

**Solution**: Make sure you restarted the AI after editing the file

### Wrong prompt loading

**Issue**: Getting default prompt instead of custom one

**Solution**: 
- Check `.env` has correct `SYSTEM_PROMPT_FILE` path
- Verify file exists: `ls -la templates/`
- Check for typos in filename

### Syntax errors

**Issue**: AI behavior is strange or inconsistent

**Solution**:
- Check for formatting issues in your prompt
- Ensure proper line breaks and structure
- Test with the default prompt first

### File not found

**Issue**: `⚠️ Warning: SYSTEM_PROMPT_FILE not found`

**Solution**:
- Use relative path from project root: `templates/filename.txt`
- Or absolute path: `/full/path/to/templates/filename.txt`
- Verify file exists: `cat templates/filename.txt`

## Tips & Tricks

1. **Start with a Template**: Modify existing templates rather than starting from scratch
2. **Keep It Concise**: Shorter prompts often work better than lengthy ones
3. **Test Incrementally**: Make small changes and test each one
4. **Version Control**: Keep track of what works with git commits
5. **Compare Behaviors**: Run the same conversation with different prompts
6. **Use Comments**: Add notes in your template files (they're just text)

## Contributing Your Templates

If you create an effective custom template, consider:
- Adding it to the `templates/` directory
- Documenting its use case
- Sharing via pull request

## See Also

- `templates/README.md` - Template directory documentation
- `ai_brain/config.py` - Source code for prompt loading
- `tests/test_prompt_templates.py` - Test suite for prompts
- Main README.md - General project documentation
