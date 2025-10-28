#!/usr/bin/env python3
"""Debug script to see exact command being executed"""

import os
from dotenv import load_dotenv

load_dotenv('../.env')

CLAUDE_PATH = os.getenv('CLAUDE_CODE_PATH', 'claude')

# Simulate what agent.py does
prompt = "/classify_issue test"
model = "sonnet"

cmd = [CLAUDE_PATH, "-p", prompt]
cmd.extend(["--model", model])
cmd.extend(["--output-format", "stream-json"])
cmd.append("--verbose")
cmd.append("--dangerously-skip-permissions")

print("Command as list:")
for i, part in enumerate(cmd):
    print(f"  [{i}]: {repr(part)}")

print("\nCommand as string (for reference):")
print(" ".join(cmd))

print("\nCLAUDE_PATH:", CLAUDE_PATH)
print("Prompt:", repr(prompt))
