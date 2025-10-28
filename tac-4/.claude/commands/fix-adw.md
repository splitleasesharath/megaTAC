# Fix ADW Script Error

Analyze an error from an ADW script, find relevant fixes in the fixes documentation, and apply the appropriate fix.

## Instructions

You will receive two pieces of information in `$ARGUMENTS` (separated by a delimiter):
1. The script path that encountered the error
2. The error message/output

Your task is to:
1. **Read the fixes documentation** at `../fixes.md`
2. **Analyze the error** to identify the root cause
3. **Search for similar patterns** in the fixes.md file
4. **Apply the appropriate fix** if one is found
5. **Log new fixes** to fixes.md if this is a novel error that you successfully resolve

## Arguments Format

```
SCRIPT_PATH: <path to the script>
ERROR_OUTPUT: <the error message and stack trace>
```

$ARGUMENTS

## Analysis Steps

### Step 1: Read Fixes Documentation
- Read the complete `../fixes.md` file
- Understand the fix patterns already documented

### Step 2: Analyze the Error
- Identify the error type (UnicodeError, subprocess error, import error, etc.)
- Extract key error patterns (file names, line numbers, error messages)
- Determine the root cause category

### Step 3: Search for Similar Fixes
Look for similar patterns in fixes.md:
- Similar error messages
- Same file mentioned in the error
- Same error type (encoding, environment, path, etc.)
- Similar subprocess or file operation issues

### Step 4: Apply Fix
If a matching fix is found:
- Apply the fix using the Edit tool
- Verify the fix was applied correctly
- Report: "FIX APPLIED: [description of what was fixed]"

If no matching fix is found but you can deduce a solution:
- Analyze the error using your knowledge
- Apply an appropriate fix
- Proceed to Step 5 to log it

If you cannot fix the error:
- Report: "FIX NOT FOUND: Unable to determine appropriate fix for this error"
- Provide diagnostic information to help manual debugging

### Step 5: Log New Fixes
If you applied a NEW fix (not already in fixes.md):
- Add a comprehensive entry to `../fixes.md` following the existing format:
  - Fix number (next in sequence)
  - Problem description with error message
  - Root cause analysis
  - Solution pattern with before/after code
  - Files modified with line numbers
  - How to apply to other projects
- Use the existing fixes as templates for formatting

## Fix Categories to Look For

Based on the fixes.md file, common categories include:
1. **Git Directory Issues**: `fatal: not a git repository`
2. **Environment Variables**: `error connecting to api.github.com`
3. **Unicode Encoding**: `UnicodeDecodeError`, `UnicodeEncodeError`
4. **Python Bytecode Cache**: Stale .pyc files
5. **Empty Output**: Claude Code producing no JSONL
6. **Windows .cmd Wrapper**: Argument mangling with long prompts
7. **Working Directory**: Scripts running from wrong location
8. **Subprocess Encoding**: Missing `encoding='utf-8'`

## Output Format

Provide a clear report:
```
ERROR ANALYSIS:
- Error Type: [type]
- Affected File: [file:line]
- Root Cause: [description]

FIX SEARCH RESULT:
- Match Found: [Yes/No]
- Fix Reference: [Fix #N from fixes.md]

ACTION TAKEN:
- [Description of fix applied]
- [Files modified]
- [New entry added to fixes.md: Yes/No]

RECOMMENDATION:
- [Next steps or additional context]
```

## Important Notes

- **Only make necessary fixes** - don't refactor or improve code unnecessarily
- **Preserve file structure** - maintain existing formatting and style
- **Log comprehensively** - future runs depend on accurate fix documentation
- **Be specific** - include exact line numbers and file paths in logs
- **Verify encoding fixes** - always add `encoding='utf-8'` for text operations
- **Check for stale cache** - suggest deleting `__pycache__` if fix doesn't apply
