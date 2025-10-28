#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Agent Test & Fix - Automated Testing and Error Resolution

This script provides an automated test-fix cycle for ADW scripts:
1. Runs a target script with subprocess
2. Detects errors in the output
3. Uses Claude Code /fix-adw to analyze and apply fixes
4. Repeats until script runs successfully or max cycles reached
5. Logs new fixes to ../fixes.md for future reference

Usage: uv run adw_agent_test_fix.py <script-path>

Example: uv run adw_agent_test_fix.py adws/adw_plan_build.py

Environment Requirements:
- CLAUDE_CODE_PATH: Path to Claude CLI (uses native authentication)
- GITHUB_PAT: (Optional) GitHub Personal Access Token - only if using a different account than 'gh auth login'
- All environment variables required by the target script
"""

import subprocess
import sys
import os
import re
from typing import Tuple, Optional
from dotenv import load_dotenv
from data_types import AgentTemplateRequest, AgentPromptResponse
from agent import execute_template
from utils import make_adw_id, setup_logger

# Load environment variables
load_dotenv()

# Constants
MAX_CYCLES = 18
TIMEOUT_SECONDS = 300  # 5 minutes
AGENT_NAME = "test_fix_agent"


def check_env_vars() -> None:
    """Check that all required environment variables are set."""
    required_vars = [
        "CLAUDE_CODE_PATH",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("Error: Missing required environment variables:", file=sys.stderr)
        for var in missing_vars:
            print(f"  - {var}", file=sys.stderr)
        sys.exit(1)


def parse_args() -> str:
    """Parse command line arguments. Returns script_path."""
    if len(sys.argv) < 2:
        usage_msg = [
            "Usage: uv run adw_agent_test_fix.py <script-path>",
            "",
            "Example: uv run adw_agent_test_fix.py adws/adw_plan_build.py",
            "Example: uv run adw_agent_test_fix.py ../adws/adw_plan_build.py",
            "",
            "This will:",
            "  1. Run the script with: uv run <script-path> 1",
            "  2. If errors occur, use /fix-adw to analyze and fix",
            "  3. Repeat up to 18 cycles until script runs successfully",
            "  4. Log new fixes to ../fixes.md",
        ]
        for msg in usage_msg:
            print(msg)
        sys.exit(1)

    script_path = sys.argv[1]

    # Clean up PowerShell invocation syntax if present
    # Remove leading "& '" and trailing "'" from PowerShell invocation
    if script_path.startswith("& '") and script_path.endswith("'"):
        script_path = script_path[3:-1]
    elif script_path.startswith('& "') and script_path.endswith('"'):
        script_path = script_path[3:-1]

    # Validate script path exists
    if not os.path.exists(script_path):
        print(f"Error: Script not found: {script_path}", file=sys.stderr)
        print(f"Note: Pass the script path without PowerShell invocation syntax", file=sys.stderr)
        print(f"Example: adws/adw_plan_build.py (not \"& 'path'\")", file=sys.stderr)
        sys.exit(1)

    return script_path


def run_script_test(script_path: str, adw_id: str, logger) -> Tuple[bool, str, str]:
    """
    Run the target script and capture output.

    Args:
        script_path: Path to the ADW script to test
        adw_id: ADW ID to pass to the script (for scripts that require it)
        logger: Logger instance

    Returns:
        Tuple of (success, stdout, stderr)
    """
    logger.info(f"Running test: uv run \"{script_path}\" 1 {adw_id}")

    try:
        # Run in PowerShell on Windows, regular shell on Unix
        if os.name == 'nt':  # Windows
            # Use PowerShell to run the command
            # Quote the script path to handle spaces in Windows paths
            # Pass both issue number (1) and adw_id for scripts that need it
            cmd = ['powershell', '-Command', f'uv run "{script_path}" 1 {adw_id}']
        else:
            cmd = ['uv', 'run', script_path, '1', adw_id]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=TIMEOUT_SECONDS,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Run from project root
        )

        success = result.returncode == 0
        stdout = result.stdout
        stderr = result.stderr

        if success:
            logger.info("✅ Script completed successfully")
        else:
            logger.error(f"❌ Script failed with exit code {result.returncode}")

        return success, stdout, stderr

    except subprocess.TimeoutExpired:
        logger.error(f"❌ Script timed out after {TIMEOUT_SECONDS} seconds")
        return False, "", f"TIMEOUT: Script exceeded {TIMEOUT_SECONDS} second limit"
    except Exception as e:
        logger.error(f"❌ Error running script: {e}")
        return False, "", str(e)


def extract_error_info(stdout: str, stderr: str) -> str:
    """Extract meaningful error information from output."""
    error_output = []

    if stderr:
        error_output.append("=== STDERR ===")
        error_output.append(stderr)

    if stdout:
        # Look for common error patterns in stdout
        error_patterns = [
            r'Error:.*',
            r'Traceback.*',
            r'.*Exception:.*',
            r'fatal:.*',
            r'UnicodeDecodeError.*',
            r'UnicodeEncodeError.*',
            r'.*ERROR.*',
        ]

        for pattern in error_patterns:
            matches = re.findall(pattern, stdout, re.MULTILINE | re.IGNORECASE)
            if matches:
                error_output.append("=== STDOUT ERRORS ===")
                error_output.extend(matches)
                break

        # If no specific errors found, include last 20 lines of stdout
        if not any('STDOUT' in line for line in error_output):
            lines = stdout.split('\n')
            if len(lines) > 20:
                error_output.append("=== LAST 20 LINES OF STDOUT ===")
                error_output.extend(lines[-20:])
            else:
                error_output.append("=== STDOUT ===")
                error_output.append(stdout)

    return '\n'.join(error_output)


def call_fix_agent(script_path: str, error_output: str, adw_id: str, cycle: int, logger) -> AgentPromptResponse:
    """
    Call the /fix-adw slash command to analyze and fix the error.

    Returns:
        AgentPromptResponse with fix results
    """
    logger.info(f"🔧 Cycle {cycle}: Calling /fix-adw to analyze and fix error")

    # Format arguments for fix-adw
    # The fix-adw expects: SCRIPT_PATH and ERROR_OUTPUT
    args_text = f"""SCRIPT_PATH: {script_path}

ERROR_OUTPUT:
{error_output}
"""

    # Create template request
    request = AgentTemplateRequest(
        agent_name=AGENT_NAME,
        slash_command="/fix-adw",
        args=[args_text],
        adw_id=adw_id,
        model="sonnet",  # Use faster model for fixing
    )

    # Execute the /fix-adw command
    response = execute_template(request)

    if response.success:
        logger.info("✅ Fix ADW completed analysis")
    else:
        logger.error("❌ Fix ADW encountered an error")

    return response


def main():
    """Main orchestration function."""
    # Check environment
    check_env_vars()

    # Parse arguments
    script_path = parse_args()

    # Generate unique ADW ID for this test session
    adw_id = make_adw_id()

    # Setup logger
    logger = setup_logger(adw_id)
    logger.info("="*60)
    logger.info("ADW Agent Test & Fix - Starting")
    logger.info(f"ADW ID: {adw_id}")
    logger.info(f"Target Script: {script_path}")
    logger.info(f"Max Cycles: {MAX_CYCLES}")
    logger.info("="*60)

    # Test-Fix Loop
    for cycle in range(1, MAX_CYCLES + 1):
        logger.info("")
        logger.info(f"{'='*60}")
        logger.info(f"CYCLE {cycle}/{MAX_CYCLES}")
        logger.info(f"{'='*60}")

        # Run the script test
        success, stdout, stderr = run_script_test(script_path, adw_id, logger)

        # Log test output for visibility
        if stdout:
            logger.info("")
            logger.info("Script STDOUT:")
            logger.info("-"*60)
            # Show first 1000 chars of stdout
            stdout_preview = stdout[:1000] + "..." if len(stdout) > 1000 else stdout
            logger.info(stdout_preview)
            logger.info("-"*60)

        if success:
            logger.info("")
            logger.info("="*60)
            logger.info("🎉 SUCCESS! Script completed without errors")
            logger.info(f"Total cycles: {cycle}")
            logger.info("="*60)
            sys.exit(0)

        # Extract error information
        error_output = extract_error_info(stdout, stderr)

        logger.info("")
        logger.info("Error detected:")
        logger.info("-"*60)
        logger.info(error_output[:500] + "..." if len(error_output) > 500 else error_output)
        logger.info("-"*60)

        # Call fix agent
        logger.info("")
        logger.info("Invoking /fix-adw command...")
        fix_response = call_fix_agent(script_path, error_output, adw_id, cycle, logger)

        if not fix_response.success:
            logger.error("")
            logger.error(f"⚠️  Fix ADW failed: {fix_response.output[:500]}")
            logger.info("Continuing to next cycle...")
        else:
            logger.info("")
            logger.info("Fix ADW output:")
            logger.info("-"*60)
            # Show full output for transparency
            logger.info(fix_response.output)
            logger.info("-"*60)

        # Continue to next cycle
        logger.info("")
        logger.info(f"Proceeding to cycle {cycle + 1} of {MAX_CYCLES}...")

    # Max cycles reached
    logger.info("")
    logger.info("="*60)
    logger.info(f"❌ FAILURE: Maximum cycles ({MAX_CYCLES}) reached")
    logger.info("The script still has errors after all fix attempts")
    logger.info("="*60)
    logger.info("")
    logger.info("Recommendations:")
    logger.info("  1. Review the /fix-adw output above")
    logger.info("  2. Check ../fixes.md for relevant fixes")
    logger.info("  3. Manually debug the remaining issues")
    logger.info("  4. Consider increasing MAX_CYCLES if fixes are being applied")

    sys.exit(1)


if __name__ == "__main__":
    main()
