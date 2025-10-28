#!/usr/bin/env python3
"""Test subprocess call exactly like agent.py does it"""

import subprocess
import os
from dotenv import load_dotenv

load_dotenv('../.env')

CLAUDE_PATH = os.getenv('CLAUDE_CODE_PATH', 'claude')

# Simple test prompt
prompt = "/classify_issue test"
model = "sonnet"

cmd = [CLAUDE_PATH, "-p", prompt]
cmd.extend(["--model", model])
cmd.extend(["--output-format", "stream-json"])
cmd.append("--verbose")
cmd.append("--dangerously-skip-permissions")

# Project root is parent of adws
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("Command:", cmd)
print("Project root:", project_root)
print()

output_file = "test_subprocess_output.jsonl"

try:
    with open(output_file, "w", encoding="utf-8") as f:
        result = subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            cwd=project_root,
            timeout=60
        )

    print(f"Return code: {result.returncode}")
    print(f"Stderr: {result.stderr}")

    # Check output
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"\nOutput file size: {len(content)} bytes")
        print("First 500 chars:")
        print(content[:500])

except Exception as e:
    print(f"Error: {e}")
