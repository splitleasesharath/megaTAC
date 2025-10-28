# Test ADW Script

Run an ADW script with proper error handling and timeout.

## Instructions

- You are testing an ADW (AI Developer Workflow) script to verify it runs without errors
- The script path and ADW ID will be provided in `$ARGUMENTS` (format: `<script_path> <adw_id>`)
- Run the script using `uv run` with the following specifications:
  - Command: `uv run <script_path> 1 <adw_id>`
  - Working directory: `app/` (if it exists, otherwise current directory)
  - Timeout: 300 seconds (5 minutes)
  - Shell: PowerShell on Windows
  - Capture both stdout and stderr

## Arguments

$ARGUMENTS

**Format**: First argument is the script path, second argument is the ADW ID

## Execution Steps

1. **Parse arguments**:
   - Extract script path (first argument)
   - Extract ADW ID (second argument)
   - Validate the script path exists

2. **Run the script**:
   - Use the Bash tool to execute: `uv run <script_path> 1 <adw_id>`
   - Issue number is always "1" (for testing)
   - Pass the ADW ID as the second script argument
   - Set timeout to 300000ms (5 minutes)
   - Capture all output

3. **Report Results**:
   - If successful (exit code 0): Report "SUCCESS: Script completed without errors"
   - If error occurred: Report "ERROR:" followed by the error message and stderr output
   - If timeout: Report "TIMEOUT: Script exceeded 5 minute limit"
   - Include the exit code in your report

## Important Notes

- Do NOT attempt to fix errors - just report them
- Preserve the complete error output for analysis
- If the script requires environment variables, ensure they are available
- The ADW ID is passed to support scripts like `adw_build.py` that require it
- Scripts like `adw_plan.py` accept the ADW ID as optional and will use it if provided
