# Fix ADW Script Error

Analyze an error from an ADW script, determine if it's fixable, and apply the appropriate fix if possible.

## Instructions

You will receive two pieces of information in `$ARGUMENTS` (separated by a delimiter):
1. The script path that encountered the error
2. The error message/output

Your task is to:
1. **Classify the error type** (CRITICAL FIRST STEP)
2. **Exit immediately if it's a usage/parameter error**
3. **Read fixes documentation** and search for patterns (only if fixable)
4. **Apply the appropriate fix** if one is found
5. **Log new fixes** to fixes.md if this is a novel error that you successfully resolve

## Arguments Format

```
SCRIPT_PATH: <path to the script>
ERROR_OUTPUT: <the error message and stack trace>
```

$ARGUMENTS

## Step 1: Error Classification (CRITICAL)

**BEFORE doing anything else**, classify the error into one of these categories:

### Category A: USAGE ERRORS (Exit Immediately - DO NOT FIX)
These are user errors that cannot be fixed by modifying code:

**Pattern Recognition:**
- `Usage:` or `usage:` in error message
- `Error: Missing required` or `required argument`
- `Error: adw-id is required`
- `Error: <argument> is required`
- `GraphQL: Could not resolve to an issue` (non-existent issue number)
- `No such file or directory` (for input files/issues)
- `Invalid issue number`
- `Permission denied` (authentication/access issues)

**Response for Category A:**
```
USAGE ERROR DETECTED - CANNOT FIX AUTOMATICALLY

Error Type: Missing/Invalid Parameter
Description: [Brief description]
User Action Required: [What the user needs to do]

RECOMMENDATION: Exit the test-fix cycle immediately. This is not a code bug.
```

**IMPORTANT**: After detecting a usage error, **STOP PROCESSING** and return the above message. Do NOT proceed to Step 2.

### Category B: CODE BUGS (Proceed to Fix)
These are actual bugs in the code that can be fixed:

**Pattern Recognition:**
- `UnicodeDecodeError`, `UnicodeEncodeError` (encoding issues)
- `fatal: not a git repository` (directory issues)
- `error connecting to api.github.com` (environment issues)
- `ModuleNotFoundError`, `ImportError` (dependency issues)
- `AttributeError`, `TypeError`, `KeyError` (code logic errors)
- `--- Logging error ---` (logger configuration issues)
- Empty Claude Code output (CLI integration issues)

**Response for Category B:**
Proceed to Step 2 (Fix Analysis and Application)

---

## Step 2: Analyze the Error (Only for Category B)

**Read fixes documentation:**
- Read the complete `../fixes.md` file
- Understand the fix patterns already documented

**Identify error patterns:**
- Error type (encoding, environment, path, etc.)
- Affected files and line numbers
- Root cause category

**Search for similar fixes:**
Look for patterns in fixes.md:
- Similar error messages
- Same file mentioned in the error
- Same error type
- Similar subprocess or file operation issues

---

## Step 3: Apply Fix (Only for Category B)

**If a matching fix is found:**
- Apply the fix using the Edit tool
- Verify the fix was applied correctly
- Report: "FIX APPLIED: [description of what was fixed]"

**If no matching fix is found but you can deduce a solution:**
- Analyze the error using your knowledge
- Apply an appropriate fix
- Proceed to Step 4 to log it

**If you cannot fix the error:**
- Report: "FIX NOT FOUND: Unable to determine appropriate fix for this error"
- Provide diagnostic information to help manual debugging

---

## Step 4: Log New Fixes (Only for New Patterns)

If you applied a NEW fix (not already in fixes.md):
- Add a comprehensive entry to `../fixes.md` following the existing format:
  - Fix number (next in sequence)
  - Problem description with error message
  - Root cause analysis
  - Solution pattern with before/after code
  - Files modified with line numbers
  - How to apply to other projects
- Use the existing fixes as templates for formatting

---

## Fix Categories to Look For (Category B Only)

Based on the fixes.md file, common fixable categories include:
1. **Git Directory Issues**: `fatal: not a git repository`
2. **Environment Variables**: `error connecting to api.github.com`
3. **Unicode Encoding**: `UnicodeDecodeError`, `UnicodeEncodeError`
4. **Python Bytecode Cache**: Stale .pyc files
5. **Empty Output**: Claude Code producing no JSONL
6. **Windows .cmd Wrapper**: Argument mangling with long prompts
7. **Working Directory**: Scripts running from wrong location
8. **Subprocess Encoding**: Missing `encoding='utf-8'`

---

## Output Format

### For Usage Errors (Category A):
```
USAGE ERROR DETECTED - CANNOT FIX AUTOMATICALLY

Error Type: [Missing Required Argument / Invalid Issue Number / etc.]
Description: [What the actual problem is]
User Action Required: [Specific steps the user must take]

RECOMMENDATION: Exit the test-fix cycle immediately. This is not a code bug.
```

### For Code Bugs (Category B):
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

---

## Important Notes

- **ALWAYS classify first** - Don't skip error classification
- **Exit immediately for usage errors** - Don't waste cycles trying to fix user mistakes
- **Only make necessary fixes** - Don't refactor or improve code unnecessarily
- **Preserve file structure** - Maintain existing formatting and style
- **Log comprehensively** - Future runs depend on accurate fix documentation
- **Be specific** - Include exact line numbers and file paths in logs
- **Verify encoding fixes** - Always add `encoding='utf-8'` for text operations
- **Check for stale cache** - Suggest deleting `__pycache__` if fix doesn't apply

---

## Examples

### Example 1: Usage Error (Category A)
```
Input: Error: adw-id is required to locate the plan file

Output:
USAGE ERROR DETECTED - CANNOT FIX AUTOMATICALLY

Error Type: Missing Required Argument (adw-id)
Description: The script requires an ADW ID parameter but it was not provided
User Action Required: Run the script with: uv run adw_build.py <issue-number> <adw-id>

RECOMMENDATION: Exit the test-fix cycle immediately. This is not a code bug.
```

### Example 2: Code Bug (Category B)
```
Input: UnicodeEncodeError: 'charmap' codec can't encode character

Output:
ERROR ANALYSIS:
- Error Type: Unicode Encoding
- Affected File: utils.py:41
- Root Cause: Logger using Windows cp1252 encoding instead of UTF-8

FIX SEARCH RESULT:
- Match Found: Yes
- Fix Reference: Fix #3 from fixes.md

ACTION TAKEN:
- Added encoding='utf-8' to FileHandler in utils.py:41
- Added sys.stdout.reconfigure(encoding='utf-8') at start of setup_logger()
- Deleted __pycache__ to clear stale bytecode

RECOMMENDATION:
- Test completed successfully after applying UTF-8 encoding pattern
```
