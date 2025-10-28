# Feature: JSONL Support

## Feature Description
Add support for uploading JSONL (JSON Lines) files to the Natural Language SQL Interface application. This feature will allow users to upload JSONL files containing newline-delimited JSON objects, which will be processed and converted to SQLite tables similar to existing CSV and JSON functionality. The system will automatically flatten nested objects and arrays using a configurable delimiter system, making complex JSON data queryable through natural language.

## User Story
As a data analyst
I want to upload JSONL files containing nested JSON objects
So that I can query complex, hierarchical data using natural language without manually flattening the structure

## Problem Statement
The current application only supports CSV and JSON array uploads. Many data sources, especially from APIs and streaming systems, provide data in JSONL format with nested structures. Users currently cannot easily import and query this type of data without manual preprocessing.

## Solution Statement
Implement JSONL file processing that:
1. Parses JSONL files line by line to handle large datasets efficiently
2. Automatically discovers all possible fields by scanning the entire file
3. Flattens nested objects and arrays using a configurable delimiter system (`__` for nested fields, `_0` for list items)
4. Creates SQLite tables with proper column naming and data types
5. Updates the UI to indicate JSONL support and provides test files for validation

## Relevant Files
Use these files to implement the feature:

- `app/server/core/file_processor.py` - Contains CSV and JSON processing logic that needs to be extended with JSONL support
- `app/server/server.py` - Main FastAPI server with upload endpoint that needs to handle `.jsonl` files
- `app/client/src/main.ts` - Frontend logic for file upload handling and UI updates
- `app/client/index.html` - UI elements that need to be updated to show JSONL support
- `app/server/core/data_models.py` - Data models for API responses that may need updates
- `app/server/tests/test_file_processor.py` - Test file that needs JSONL test cases

### New Files
- `app/server/core/constants.py` - Store configurable delimiter constants
- `app/server/tests/assets/sample_data.jsonl` - Test JSONL file with nested structures
- `app/server/tests/assets/complex_data.jsonl` - Test JSONL file with arrays and deep nesting
- `app/client/public/sample-data/events.jsonl` - Sample JSONL file for frontend testing

## Implementation Plan
### Phase 1: Foundation
Set up the delimiter constants and core JSONL processing utilities. This includes creating the constants file and implementing the field discovery and flattening logic that will be used by the main processing function.

### Phase 2: Core Implementation
Implement the main JSONL processing function in the file processor, add it to the server endpoint, and create comprehensive tests to ensure the functionality works correctly with various JSONL structures.

### Phase 3: Integration
Update the frontend to support JSONL uploads, create sample test files, and ensure the entire feature works end-to-end with proper error handling and user feedback.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Constants File
- Create `app/server/core/constants.py` with delimiter constants
- Define `NESTED_DELIMITER = "__"` for nested fields
- Define `LIST_INDEX_DELIMITER = "_"` for list items
- Add documentation explaining the delimiter system

### Step 2: Implement JSONL Field Discovery
- Add `discover_jsonl_fields()` function to scan entire JSONL file
- Implement logic to collect all possible field names from all records
- Handle nested objects and arrays recursively
- Create field mapping for flattened column names

### Step 3: Implement Field Flattening Logic
- Add `flatten_json_object()` function to flatten nested structures
- Use delimiter constants for consistent naming
- Handle arrays with index-based naming (e.g., `items_0`, `items_1`)
- Handle deeply nested objects (e.g., `user__profile__name`)

### Step 4: Add JSONL Processing Function
- Create `convert_jsonl_to_sqlite()` function in `file_processor.py`
- Parse JSONL files line by line for memory efficiency
- Apply field discovery and flattening to each record
- Create pandas DataFrame with consistent column structure
- Follow existing patterns from CSV/JSON processors

### Step 5: Update Server Endpoint
- Modify upload endpoint in `server.py` to accept `.jsonl` files
- Add JSONL file type validation
- Route JSONL files to the new processing function
- Ensure proper error handling and logging

### Step 6: Create Test Files
- Create `app/server/tests/assets/sample_data.jsonl` with basic nested structures
- Create `app/server/tests/assets/complex_data.jsonl` with arrays and deep nesting
- Include various data types (strings, numbers, booleans, null values)
- Document expected flattened column names

### Step 7: Implement Unit Tests
- Add comprehensive tests to `test_file_processor.py`
- Test field discovery with various JSONL structures
- Test flattening logic with nested objects and arrays
- Test error handling for malformed JSONL files
- Test integration with SQLite table creation

### Step 8: Update Frontend UI
- Modify file upload text in `index.html` to mention JSONL support
- Update file validation in `main.ts` to accept `.jsonl` files
- Add appropriate error messages for JSONL-specific issues
- Ensure drag-and-drop works with JSONL files

### Step 9: Create Sample Frontend Data
- Create `app/client/public/sample-data/events.jsonl` for testing
- Include realistic sample data with nested structures
- Add sample button in upload modal for JSONL testing
- Update modal JavaScript to handle JSONL sample data

### Step 10: Integration Testing
- Test complete upload flow with various JSONL files
- Verify table creation and data integrity
- Test natural language querying on flattened data
- Ensure no regressions in existing CSV/JSON functionality

### Step 11: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Test with sample JSONL files to verify functionality
- Validate that all existing tests still pass

## Testing Strategy
### Unit Tests
- Test JSONL field discovery with various nesting levels
- Test flattening algorithm with different data structures
- Test error handling for malformed JSONL files
- Test delimiter configuration and column naming
- Test memory efficiency with large JSONL files

### Integration Tests
- Test complete upload flow from frontend to database
- Test natural language querying on flattened JSONL data
- Test file validation and error handling
- Test sample data loading functionality

### Edge Cases
- Empty JSONL files
- JSONL files with inconsistent schemas across lines
- Very deeply nested objects (5+ levels)
- Arrays with mixed data types
- Large files with thousands of records
- Files with special characters in field names
- Null values and missing fields

## Acceptance Criteria
- Users can upload JSONL files through the web interface
- JSONL files are automatically processed and converted to SQLite tables
- Nested objects are flattened using the `__` delimiter
- Array elements are flattened using index-based naming (e.g., `_0`, `_1`)
- The system scans the entire JSONL file to discover all possible fields
- The UI clearly indicates JSONL support alongside CSV and JSON
- All existing functionality (CSV, JSON uploads) continues to work without regression
- Sample JSONL files are provided for testing
- Natural language queries work correctly on flattened JSONL data
- Error handling provides clear messages for malformed JSONL files

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/test_file_processor.py -v` - Run file processor tests including new JSONL tests
- `cd app/server && uv run pytest tests/ -v` - Run all server tests to ensure no regressions
- `cd app/server && uv run python -c "import core.file_processor; print('Import successful')"` - Verify module imports work
- `cd app/client && npm run build` - Ensure frontend builds without errors
- `cd app/server && uv run python server.py &` - Start server in background
- `cd app/client && npm run dev &` - Start frontend in background
- `curl -X POST -F "file=@tests/assets/sample_data.jsonl" http://localhost:8000/api/upload` - Test JSONL upload endpoint
- `curl http://localhost:8000/api/schema` - Verify schema endpoint works with JSONL tables

## Notes
- Use standard library `json` module for JSONL parsing - no additional dependencies required
- Implement line-by-line processing to handle large JSONL files efficiently
- Store delimiter constants in a dedicated constants file for easy configuration
- Follow existing security patterns from CSV/JSON processors
- Consider memory usage when processing large JSONL files
- Ensure proper error handling for malformed JSON lines
- The flattening algorithm should be deterministic and consistent across uploads
- Document the delimiter system clearly for users who need to understand the flattened column names