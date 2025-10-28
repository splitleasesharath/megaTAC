# Bug: SQLite tests running against live database

## Bug Description
One of our SQLite tests is running against the 'live' database and saving data__ tables in the actual database file at `db/database.db`. The tests should be using an in-memory SQLite database instead to ensure test isolation and prevent pollution of the development database.

## Problem Statement
The `test_file_processor.py` test file attempts to mock the SQLite connection but the mocking is not working correctly, causing tests to write to the actual database at `db/database.db`. This creates unwanted tables with names like `data__` in the development database.

## Solution Statement
Refactor the file processor module to accept an optional database connection parameter, allowing tests to provide an in-memory database connection. This approach is more reliable than mocking and follows dependency injection principles.

## Steps to Reproduce
1. Run the tests: `cd app/server && uv run pytest tests/core/test_file_processor.py`
2. Check the database: `sqlite3 db/database.db ".tables"` 
3. Observe that test tables may be created in the live database

## Root Cause Analysis
The `file_processor.py` module hardcodes the database connection path to `"db/database.db"` in three functions:
- `convert_csv_to_sqlite` (line 58)
- `convert_json_to_sqlite` (line 130)  
- `convert_jsonl_to_sqlite` (line 290)

The test attempts to mock `sqlite3.connect` but the mock doesn't always work reliably, especially when the module is imported in different ways or when the mock scope doesn't cover all execution paths.

## Relevant Files
Use these files to fix the bug:

- `app/server/core/file_processor.py` - Contains the functions that hardcode the database path
- `app/server/tests/core/test_file_processor.py` - Contains the tests that need to use in-memory database
- `app/server/server.py` - Imports and uses the file processor functions, needs to be checked for compatibility

### New Files
None required

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Refactor file_processor.py to accept optional database path
- Read `app/server/core/file_processor.py`
- Modify the three conversion functions (`convert_csv_to_sqlite`, `convert_json_to_sqlite`, `convert_jsonl_to_sqlite`) to accept an optional `db_path` parameter with default value `"db/database.db"`
- Update each function to use the `db_path` parameter instead of the hardcoded path
- Ensure backward compatibility by keeping the default behavior

### 2. Update test_file_processor.py to use in-memory database
- Read `app/server/tests/core/test_file_processor.py` 
- Remove the mock patching approach from the `test_db` fixture
- Update the fixture to create an in-memory database directly
- Modify all test methods to pass the in-memory database path to the conversion functions
- Ensure all tests use the in-memory database consistently

### 3. Verify server.py compatibility
- Read `app/server/server.py` to check how it uses the file processor functions
- Verify that the default parameter ensures backward compatibility
- No changes should be needed if the default parameter is implemented correctly

### 4. Run tests to validate the fix
- Run the file processor tests to ensure they pass
- Verify no tables are created in the live database
- Run all server tests to ensure no regressions

### 5. Clean up any existing test tables in live database
- Connect to the live database and identify any test tables created by previous test runs
- Document the cleanup process in case users need to clean their databases

### 6. Execute Validation Commands
Run the validation commands to ensure the bug is fixed with zero regressions.

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd app/server && sqlite3 db/database.db ".tables" > before_tables.txt` - Capture current tables before running tests
- `cd app/server && uv run pytest tests/core/test_file_processor.py -v` - Run the file processor tests
- `cd app/server && sqlite3 db/database.db ".tables" > after_tables.txt` - Capture tables after running tests
- `cd app/server && diff before_tables.txt after_tables.txt` - Verify no new tables were created in live database
- `cd app/server && uv run pytest` - Run all server tests to validate no regressions
- `cd app/client && bun tsc --noEmit` - Run frontend type checks to validate no regressions
- `cd app/client && bun run build` - Run frontend build to validate no regressions

## Notes
- The `data__` prefix in table names comes from the flattening of nested JSON structures where `__` is used as a delimiter for nested fields
- Using dependency injection (passing the database path as a parameter) is more reliable than mocking for database connections
- In-memory SQLite databases use the special path `:memory:` which creates a temporary database that exists only for the duration of the connection