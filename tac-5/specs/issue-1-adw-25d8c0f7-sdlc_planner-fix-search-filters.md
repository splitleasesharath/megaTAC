# Bug: Search Page Filters Not Rendering

## Bug Description
The filters on the search page at https://app.split.lease/search are not displaying correctly. Instead of showing the expected filter controls (Borough dropdown, Week Pattern selector, Price Tier selector, Sort By options, Day Selector, and Neighborhood Search), the page displays a fallback message "Filters are loading..." indicating that the React SearchFilters component is failing to mount properly.

**Expected Behavior:** The search page should display interactive filter controls including:
- Borough dropdown (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
- Week Pattern dropdown (Every week, One-one, Two-two, One-three)
- Price Tier dropdown (Price ranges and "All Prices")
- Sort By dropdown (Recommended, Price, Most Viewed, Recently Added)
- Day Selector (Check-in and Check-out day selection)
- Neighborhood Search input

**Actual Behavior:** The page shows "Filters are loading..." message and the SearchFilters React component does not render.

## Problem Statement
The search page filters are not rendering because of a JavaScript namespace mismatch between the UMD bundle export name and the filters island mounting script. The filters-island.umd.js script attempts to access the SearchFilters component at `window.SLComponents.SearchFilters`, but the Vite build configuration exposes the component library as `window.SplitLeaseComponents`, causing the component lookup to fail and the fallback UI to display.

## Solution Statement
Fix the namespace mismatch by updating the filters-island.umd.js script to reference the correct UMD bundle namespace `window.SplitLeaseComponents.SearchFilters` instead of `window.SLComponents.SearchFilters`. This will allow the SearchFilters React component to mount properly and display all filter controls as intended.

## Steps to Reproduce
1. Navigate to the search page at `app/split-lease/pages/search/index.html` (or https://app.split.lease/search in production)
2. Observe the filters section in the topbar
3. Notice that instead of filter controls, only "Filters are loading..." text appears
4. Open browser DevTools console and check for JavaScript errors or warnings
5. Verify that `window.SplitLeaseComponents` exists but `window.SLComponents` does not

## Root Cause Analysis
The root cause is a naming mismatch in the JavaScript module namespace:

1. **UMD Bundle Configuration** (app/split-lease/components/vite.config.ts:10): The Vite build configuration exposes the component library as `SplitLeaseComponents`:
   ```typescript
   name: 'SplitLeaseComponents',
   ```
   This means all exported components are available at `window.SplitLeaseComponents.*`

2. **Island Mounting Script** (app/split-lease/pages/search/js/filters-island.umd.js:91): The filters island script incorrectly looks for the component at the wrong namespace:
   ```javascript
   var hasFilters = !!(window.SLComponents && window.SLComponents.SearchFilters);
   ```
   And later attempts to access it:
   ```javascript
   var SearchFilters = window.SLComponents.SearchFilters;
   ```

3. **Result**: The hasFilters check returns false, causing the script to skip the React component rendering and fall back to the vanilla rendering function (line 108) which only displays "Filters are loading..."

The SearchFilters component itself is correctly:
- Exported from app/split-lease/components/src/SearchFilters/index.ts
- Re-exported from app/split-lease/components/src/index.ts
- Built into the UMD bundle at app/split-lease/components/dist/split-lease-components.umd.cjs
- Loaded in the search page HTML (line 35)

The only issue is the namespace reference mismatch in the mounting script.

## Relevant Files
Use these files to fix the bug:

- **app/split-lease/pages/search/js/filters-island.umd.js** (lines 91-96) - Contains the incorrect namespace reference that needs to be fixed. This is the mounting script that attempts to render the SearchFilters component but looks for it at the wrong namespace.

- **app/split-lease/components/vite.config.ts** (line 10) - Defines the UMD bundle name as 'SplitLeaseComponents'. This configuration is correct and should not be changed. Referenced to confirm the correct namespace.

- **app/split-lease/components/src/SearchFilters/SearchFilters.tsx** - The main SearchFilters component that should be rendering. Referenced to understand the component structure and ensure it's properly exported.

- **app/split-lease/components/src/SearchFilters/types.ts** - Type definitions for filter state and options. Referenced to understand what filter controls should be present.

- **app/split-lease/pages/search/index.html** (lines 35-39) - The search page HTML that includes the UMD bundle and mounting script. Referenced to understand the loading order and island mounting.

- **.claude/commands/test_e2e.md** - E2E test framework documentation. Referenced to understand how to create E2E validation tests.

- **.claude/commands/e2e/test_basic_query.md** - Example E2E test. Referenced as a template for creating the search filters E2E test.

### New Files

- **.claude/commands/e2e/test_search_filters.md** - New E2E test file to validate that the search filters render correctly and all filter controls are functional.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Fix the Namespace Reference
- Update app/split-lease/pages/search/js/filters-island.umd.js line 91 to check for `window.SplitLeaseComponents` instead of `window.SLComponents`
- Update app/split-lease/pages/search/js/filters-island.umd.js line 96 to access `window.SplitLeaseComponents.SearchFilters` instead of `window.SLComponents.SearchFilters`

### Create E2E Test for Search Filters
- Read `.claude/commands/test_e2e.md` to understand the E2E test framework
- Read `.claude/commands/e2e/test_basic_query.md` as a template for test structure
- Create a new E2E test file at `.claude/commands/e2e/test_search_filters.md` that validates:
  - The search page loads successfully at the correct URL
  - The filters section is visible (not showing "Filters are loading...")
  - All six filter controls are present and rendered:
    1. Borough dropdown with all 5 borough options
    2. Week Pattern dropdown with all 4 pattern options
    3. Price Tier dropdown with all 5 price tier options
    4. Sort By dropdown with all 4 sort options
    5. Day Selector with check-in and check-out day selection
    6. Neighborhood Search input field
  - Filter controls are interactive (can be clicked/changed)
  - Changing filter values updates the URL query parameters
  - Take screenshots showing the filters rendered correctly

### Validate the Fix
- Run the `Validation Commands` to validate the bug is fixed with zero regressions
- Ensure all components build successfully
- Execute the new E2E test to verify filters render and function correctly

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd app/split-lease/components && npm run build` - Rebuild the component library UMD bundle (should complete without errors)
- `cd app/split-lease/components && npm run typecheck` - Verify TypeScript types are correct (should complete without errors)
- Read `.claude/commands/test_e2e.md`, then read and execute the new `.claude/commands/e2e/test_search_filters.md` test file to validate that all six filter controls render correctly and are functional

## Notes
- The SearchFilters component is already properly implemented with all required filter controls
- The component is correctly exported from the component library
- The UMD bundle is correctly configured and built
- The only issue is a simple namespace reference typo in the island mounting script
- This is a minimal fix requiring only 2 line changes in one file
- No new dependencies or libraries are needed
- After the fix, the filters should immediately render on page load showing all six filter controls
- The filter state will sync with URL query parameters as designed
- The fix preserves the Islands Architecture pattern - static HTML enhanced with React islands
