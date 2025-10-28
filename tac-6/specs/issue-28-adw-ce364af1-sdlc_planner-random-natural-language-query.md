# Feature: Random Natural Language Query Generator

## Feature Description
This feature adds a "Generate Random Query" button to the Natural Language SQL Interface that automatically generates interesting natural language queries based on the existing database tables and their structures. The button will populate the query input field with AI-generated queries that users can execute manually, providing inspiration and demonstrating the application's capabilities.

## User Story
As a user
I want to generate random natural language queries based on my database tables
So that I can discover interesting insights from my data and see example queries that work with my specific schema

## Problem Statement
Users often don't know what questions to ask about their data or how to phrase natural language queries effectively. This creates a barrier to exploring and understanding their datasets, especially for new users who are unfamiliar with the application's capabilities.

## Solution Statement
Add a "Generate Random Query" button that uses the existing LLM processor to analyze the current database schema and generate contextually relevant, interesting natural language queries. The button will be positioned separate from the primary action buttons and will automatically populate the query input field, overwriting any existing content.

## Relevant Files
Use these files to implement the feature:

- `app/client/src/main.ts` - Main TypeScript file containing UI initialization and event handlers. Relevant for adding the new button functionality and integrating with the query input field.
- `app/client/src/style.css` - Styles for the application UI. Relevant for styling the new button to match the Upload Data button design.
- `app/client/index.html` - HTML template containing the application structure. Relevant for adding the new button to the query controls section.
- `app/server/core/llm_processor.py` - LLM processing module that handles OpenAI and Anthropic API calls. Relevant for generating random queries based on database schema.
- `app/server/core/sql_processor.py` - SQL processing module that handles database schema retrieval. Relevant for getting table structures to pass to the LLM.
- `app/server/server.py` - FastAPI server with API endpoints. Relevant for adding a new endpoint to handle random query generation requests.

### New Files
- `.claude/commands/e2e/test_random_query_generator.md` - E2E test file to validate the random query generator functionality works as expected

## Implementation Plan

### Phase 1: Foundation
Create the backend API endpoint that leverages the existing LLM processor to generate random queries based on the current database schema. This will use the same infrastructure as the existing query processing but with a different prompt focused on generating interesting questions rather than converting existing queries.

### Phase 2: Core Implementation
Implement the frontend button and integration with the new backend endpoint. The button will be styled to match the Upload Data button but positioned separately in the query controls section to maintain clear visual hierarchy.

### Phase 3: Integration
Connect the frontend and backend components, ensuring proper error handling and user feedback. The generated queries will be limited to two sentences maximum as specified in the requirements.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Backend API Development
- Add new `/api/generate-random-query` endpoint to `app/server/server.py` that returns a random natural language query based on current database schema
- Create helper function in `app/server/core/llm_processor.py` to generate random queries using existing LLM infrastructure with specialized prompt for query generation
- Update the LLM prompt to generate interesting, contextually relevant queries based on table structures, limiting output to two sentences maximum

### Frontend UI Implementation
- Add "Generate Random Query" button to `app/client/index.html` in the query controls section, positioned separately from Query and Upload Data buttons
- Style the new button in `app/client/src/style.css` to match the Upload Data button design but with distinct positioning using justify-apart layout
- Implement button click handler in `app/client/src/main.ts` that calls the new API endpoint and populates the query input field, overwriting existing content

### API Integration
- Add API client method in `app/client/src/api/client.ts` to call the new random query generation endpoint
- Implement proper error handling for API failures and display appropriate user feedback
- Ensure the generated query replaces any existing content in the query input field

### Testing and Validation
- Create E2E test file `.claude/commands/e2e/test_random_query_generator.md` that validates the button works correctly, generates queries, and populates the input field
- Test the feature with various database schemas to ensure query generation works appropriately
- Verify the button styling matches the Upload Data button and is properly positioned

### Final Integration Testing
- Run all validation commands to ensure no regressions were introduced
- Test the complete user flow from button click to query generation to query execution
- Verify the feature works with both OpenAI and Anthropic LLM providers

## Testing Strategy

### Unit Tests
- Test the new API endpoint returns valid natural language queries
- Test LLM processor generates appropriate queries for different schema types
- Test frontend button click handler properly calls API and updates input field
- Test error handling for API failures and malformed responses

### Edge Cases
- Empty database (no tables) - should return appropriate message
- Database with single table - should generate relevant queries
- Database with multiple related tables - should generate queries that demonstrate relationships
- LLM API failures - should display error message without breaking the application
- Network connectivity issues - should handle gracefully

## Acceptance Criteria
- New "Generate Random Query" button is visible and properly styled to match Upload Data button
- Button is positioned separately from primary action buttons using justify-apart layout
- Clicking the button generates a contextually relevant natural language query
- Generated query is limited to two sentences maximum
- Query automatically populates the input field, overwriting existing content
- Button works with both OpenAI and Anthropic LLM providers
- Error handling displays appropriate messages for API failures
- Feature works with various database schemas and table structures
- E2E test validates complete functionality

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_random_query_generator.md` test file to validate this functionality works

## Notes
- The feature leverages existing LLM infrastructure (llm_processor.py) to minimize new dependencies
- Generated queries should be contextually relevant to the actual data structure, not generic examples
- The button should be clearly distinguishable from primary action buttons while maintaining design consistency
- Consider adding a loading state for the button during API calls to improve user experience
- The feature should work regardless of which LLM provider is configured (OpenAI or Anthropic)