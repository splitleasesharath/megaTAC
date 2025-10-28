#!/usr/bin/env python3
"""Test script to debug environment issues"""

import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv('../.env')

CLAUDE_PATH = os.getenv('CLAUDE_CODE_PATH', 'claude')

# Test 1: Run with full environment (env=None)
print("=" * 80)
print("TEST 1: Running with full environment (env=None)")
print("=" * 80)
cmd = [CLAUDE_PATH, '-p', 'What is 2+2?', '--model', 'sonnet', '--output-format', 'stream-json', '--verbose', '--dangerously-skip-permissions']

try:
    with open('test_output_full_env.jsonl', 'w', encoding='utf-8') as f:
        result = subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            timeout=30
        )

    print(f"Return code: {result.returncode}")
    print(f"Stderr: {result.stderr}")

    # Check if file has content
    with open('test_output_full_env.jsonl', 'r') as f:
        content = f.read()
        print(f"Output file size: {len(content)} bytes")
        if content:
            print("SUCCESS - Got output with full environment")
        else:
            print("FAIL - No output with full environment")
except Exception as e:
    print(f"Error: {e}")

print()

# Test 2: Run with restricted environment (like get_claude_env)
print("=" * 80)
print("TEST 2: Running with restricted environment (like get_claude_env)")
print("=" * 80)

required_env_vars = {
    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
    'CLAUDE_CODE_PATH': os.getenv('CLAUDE_CODE_PATH', 'claude'),
    'HOME': os.getenv('HOME'),
    'USER': os.getenv('USER'),
    'PATH': os.getenv('PATH'),
}
env = {k: v for k, v in required_env_vars.items() if v is not None}

print(f"Environment variables being passed: {list(env.keys())}")

try:
    with open('test_output_restricted_env.jsonl', 'w', encoding='utf-8') as f:
        result = subprocess.run(
            cmd,
            stdout=f,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            env=env,
            timeout=30
        )

    print(f"Return code: {result.returncode}")
    print(f"Stderr: {result.stderr}")

    # Check if file has content
    with open('test_output_restricted_env.jsonl', 'r') as f:
        content = f.read()
        print(f"Output file size: {len(content)} bytes")
        if content:
            print("SUCCESS - Got output with restricted environment")
        else:
            print("FAIL - No output with restricted environment")
except Exception as e:
    print(f"Error: {e}")

print()
print("=" * 80)
print("Check the output files: test_output_full_env.jsonl and test_output_restricted_env.jsonl")
