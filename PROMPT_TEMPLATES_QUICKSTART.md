# 🎨 Prompt Templates Quick Reference

## 📋 Quick Start (30 seconds)

```bash
# 1. Edit .env file
nano .env

# 2. Add this line
SYSTEM_PROMPT_FILE=templates/system_prompt_professional.txt

# 3. Run the AI
python main.py

# 4. Verify it loaded
# You'll see: ✓ Loaded system prompt from: templates/system_prompt_professional.txt
```

---

## 🎯 Available Templates

| Template | Use Case | Tone |
|----------|----------|------|
| `system_prompt.txt` | General use | Balanced, friendly |
| `system_prompt_professional.txt` | Business, work | Formal, professional |
| `system_prompt_creative.txt` | Writing, brainstorming | Enthusiastic, exploratory |
| `system_prompt_technical.txt` | Coding, tech support | Precise, technical |

---

## ⚙️ Configuration Methods

### Method 1: File (Recommended)
```bash
# In .env
SYSTEM_PROMPT_FILE=templates/system_prompt.txt
```

### Method 2: Environment Variable
```bash
# In .env
SYSTEM_PROMPT="Your custom prompt text here..."
```

### Method 3: Edit Code
```python
# In ai_brain/config.py
DEFAULT_SYSTEM_PROMPT = "Your prompt..."
```

**Priority:** File → Env Variable → Default

---

## 🔧 Common Tasks

### Switch Templates
```bash
# Edit .env
SYSTEM_PROMPT_FILE=templates/system_prompt_creative.txt

# Restart
python main.py
```

### Create Custom Template
```bash
# 1. Create file
touch templates/my_custom.txt

# 2. Edit it
nano templates/my_custom.txt

# 3. Use it
echo "SYSTEM_PROMPT_FILE=templates/my_custom.txt" >> .env
```

### Test Different Templates
```bash
# Terminal 1
export SYSTEM_PROMPT_FILE=templates/system_prompt_professional.txt
python main.py

# Terminal 2
export SYSTEM_PROMPT_FILE=templates/system_prompt_creative.txt
python main.py
```

---

## ✅ Verify Setup

```bash
# Run demo
python scripts/demo_prompts.py

# Run tests
python tests/test_prompt_templates.py

# Check available templates
ls -la templates/
```

---

## 📚 Full Documentation

- **Complete Guide:** `docs/PROMPT_TEMPLATES.md`
- **Implementation:** `docs/PROMPT_TEMPLATES_IMPLEMENTATION.md`
- **Templates Info:** `templates/README.md`

---

## 💡 Tips

1. **Start with existing** - Modify templates rather than creating from scratch
2. **Keep it short** - Shorter prompts often work better
3. **Test changes** - Restart after editing
4. **Version control** - Commit good templates
5. **Share templates** - Create team-specific versions

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Changes not taking effect | Restart the AI (python main.py) |
| File not found error | Check path: `ls templates/` |
| Still using default | Check `.env` has correct `SYSTEM_PROMPT_FILE` |
| Can't edit file | Use: `nano templates/filename.txt` |

---

## 🎨 Example Custom Prompt

```
You are a patient tutor helping students learn programming.

TEACHING STYLE:
- Break concepts into simple steps
- Use analogies and examples
- Encourage questions
- Celebrate progress

MEMORY FEATURES:
- Remember what topics we've covered
- Track student's learning progress
- Reference past lessons
- Build on previous knowledge

Remember: Be encouraging and patient!
```

Save as `templates/system_prompt_tutor.txt` and use it:
```bash
SYSTEM_PROMPT_FILE=templates/system_prompt_tutor.txt
```

---

**Need more help?** See `docs/PROMPT_TEMPLATES.md` for the complete guide!
