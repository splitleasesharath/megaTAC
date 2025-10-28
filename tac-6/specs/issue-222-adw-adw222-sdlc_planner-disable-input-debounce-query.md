# Bug: Disable Input Area During Query Execution and Add Request Debouncing

## Bug Description
The query input area (textarea) remains enabled while a query is being processed, allowing users to continue typing and potentially confusing the user experience. Additionally, there is no debouncing mechanism to prevent rapid consecutive API requests when users quickly click the query button multiple times before the first request completes. This can lead to unnecessary server load and potential race conditions.

## Problem Statement
Users can interact with the query input field while a query is running, and rapid consecutive requests can be made without debouncing, leading to:
1. Confusing user experience (typing while query is processing)
2. Potential for multiple simultaneous API requests
3. Unnecessary server load from rapid button clicking
4. Race conditions in query result display

## Solution Statement
Implement input disabling during query execution and add debouncing to prevent rapid consecutive requests. The input textarea should be disabled when a query starts and re-enabled when the query completes (success or error). Additionally, implement a debounce mechanism to prevent multiple rapid API calls within a short time window.

## Steps to Reproduce
1. Navigate to the application at http://localhost:5173
2. Enter a query in the input textarea
3. Click the Query button
4. Observe that:
   - The textarea remains enabled and users can continue typing during processing
   - Rapidly clicking the Query button can trigger multiple simultaneous requests

## Root Cause Analysis
The current implementation in `app/client/src/main.ts` only disables the query button during execution but does not:
1. Disable the query input textarea (line 16 in index.html, handled in initializeQueryInput function lines 15-50)
2. Implement any debouncing mechanism to prevent rapid consecutive requests
3. Provide visual feedback that the input area is locked during processing

## Relevant Files
Use these files to fix the bug:

- `app/client/src/main.ts` - Contains the query input initialization and button click handler that needs modification to disable the textarea and add debouncing
- `app/client/index.html` - Contains the query input textarea element that needs to be disabled during query execution
- `app/client/src/style.css` - May need styling updates to show disabled state visually
- `app/client/src/api/client.ts` - Contains the API client that makes the actual requests, may need modification for debouncing

### New Files
- `.claude/commands/e2e/test_disable_input_debounce.md` - E2E test to validate the input disabling and debouncing functionality

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Implement Input Disabling and Debouncing Logic
- Modify the `initializeQueryInput()` function in `app/client/src/main.ts` to:
  - Disable the query textarea when query starts
  - Re-enable the query textarea when query completes
  - Add debouncing mechanism to prevent rapid consecutive requests
  - Add visual feedback for disabled state

### Update Styling for Disabled State
- Add CSS styles in `app/client/src/style.css` to provide clear visual feedback when the input area is disabled during query processing

### Create E2E Test
- Read `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/test_e2e.md` and create a new E2E test file in `.claude/commands/e2e/test_disable_input_debounce.md` that validates:
  - Input textarea becomes disabled when query is executed
  - Input textarea is re-enabled when query completes
  - Debouncing prevents multiple rapid API requests
  - Visual feedback is provided to users

### Run Validation Commands
- Execute all validation commands to ensure the bug is fixed with zero regressions

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- Manual test: Start the application and verify input disabling and debouncing work correctly
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_disable_input_debounce.md` test file to validate this functionality works
- `cd app/server && uv run pytest` - Run server tests to validate the bug is fixed with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the bug is fixed with zero regressions  
- `cd app/client && bun run build` - Run frontend build to validate the bug is fixed with zero regressions

## Notes
- The debouncing should have a reasonable delay (e.g., 300-500ms) to prevent accidental rapid requests while still feeling responsive
- The disabled input should have clear visual feedback (e.g., grayed out, different cursor)
- Ensure that keyboard shortcuts (Cmd+Enter/Ctrl+Enter) respect the same disabling behavior
- The fix should maintain all existing functionality while adding the new protective measures