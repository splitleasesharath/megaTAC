# Bug: Search Page Filters Are Inaccurate

## Bug Description
The filters displayed on the search page (`app/split-lease/pages/search/index.html`) do not match the actual Split Lease search page at https://app.split.lease/search. The current implementation shows an incomplete and inaccurate set of filters compared to the original website design.

**Symptoms:**
- Current implementation displays only 4 basic filters: Weekly Schedule, Price (dropdown), Room Type (checkboxes), and Sort
- The actual website shows a horizontal topbar layout with different filters: Borough, Week Pattern, Price Tier, Sort By, plus a calendar day selector and neighborhood search
- The filter layout is incorrect (vanilla sidebar vs. horizontal topbar)
- Filter options don't match the original (e.g., price dropdown vs. price tier selection)
- Missing critical filters: calendar day selector, neighborhood search/refinement, borough dropdown
- Missing week pattern filter

**Expected Behavior:**
Filters should match the original Split Lease search page with proper horizontal topbar layout and all required filter types

**Actual Behavior:**
Displays a basic vertical sidebar layout with only 4 simplified filters that don't match the original design

## Problem Statement
The `app/split-lease/pages/search/js/filters-island.umd.js` file implements an incomplete and inaccurate filter system that does not reflect the actual Split Lease search page design. This creates a mismatch between what users expect (based on the original site) and what is actually rendered, leading to poor user experience and missing critical search functionality.

## Solution Statement
Replace the current basic filter implementation with a proper horizontal topbar layout that matches the original Split Lease search page. Implement the 4 core dropdown filters (Borough, Week Pattern, Price Tier, Sort By), add the calendar day selector (S M T W T F S format), and include the neighborhood search/refine input. Update the filter state management and URL synchronization to handle the new filter structure.

## Steps to Reproduce
1. Navigate to `app/split-lease/pages/search/index.html` in a browser
2. Observe the filter section in the sidebar
3. Compare with the screenshot from context: `C:\Users\Split Lease\splitleaseteam\!Agent Context and Tools\SL1\Practice TAC\z_Test Tac 2\Search TAC 2\.playwright-mcp\split-lease-search-filters.png`
4. Note the differences:
   - Layout: sidebar vs. horizontal topbar
   - Filter types: 4 basic filters vs. proper filter set
   - Filter UI: vanilla HTML vs. proper styled components
   - Missing filters: calendar day selector, neighborhood search, borough dropdown, week pattern

## Root Cause Analysis

### Primary Cause
The `filters-island.umd.js` file was built with a simplified, minimal filter implementation that does not align with the actual Split Lease search page requirements. It appears to be a prototype or placeholder implementation rather than the production-ready filter system.

### Contributing Factors

1. **Incomplete Filter Set**: Only implements 4 filters (Weekly Schedule, Price, Room Type, Sort) when 7+ filter types are required according to specifications in `apps/search_filters/README.md`

2. **Wrong Layout Pattern**: Uses a sidebar layout when the original design uses a horizontal topbar layout (as documented in `chore-ab8feeed-rebuild-filters-match-original.md`)

3. **Vanilla Fallback Implementation**: The code primarily uses vanilla JavaScript with basic HTML rendering (`renderVanilla` function) instead of proper React components from the UMD bundle

4. **Mismatched Filter Options**:
   - Price filter uses simple buckets instead of proper price tier selection
   - Room types are checkboxes instead of proper filtering
   - Missing week pattern filter entirely
   - No calendar day selector for check-in/check-out

5. **Missing Core Features**:
   - No borough dropdown
   - No neighborhood search/refine input
   - No calendar day selector (S M T W T F S)
   - No week pattern dropdown

### Code Location
- **File**: `app/split-lease/pages/search/js/filters-island.umd.js:82-162`
- **Function**: `renderVanilla()` - implements the basic filter rendering
- **Issue**: This function renders only 4 basic filters in vanilla HTML instead of using proper React components

## Relevant Files
Use these files to fix the bug:

- `app/split-lease/pages/search/js/filters-island.umd.js` - Main filter implementation file that needs complete restructuring. Currently implements only 4 basic filters with vanilla JS fallback (lines 82-162). Needs to be replaced with proper horizontal topbar layout matching the original design.

- `app/split-lease/pages/search/index.html` - Search page HTML that mounts the filters island. Contains the `#sl-filters-root` mount point (line 21) and references to the filters island script (line 37).

- `app/split-lease/pages/search/css/styles.css` - Current filter styles for sidebar layout (lines 35-78). Needs complete overhaul to support horizontal topbar layout.

- `app/split-lease/pages/search/css/responsive.css` - Responsive styles that need updating for new filter layout.

- `app/split-lease/components/src/index.ts` - Component exports that may need new filter components exported for the UMD bundle.

### New Files

- `app/split-lease/components/src/SearchFilters/SearchFilters.tsx` - New React component implementing the horizontal topbar filter layout with all required filters

- `app/split-lease/components/src/SearchFilters/SearchFilters.styles.ts` - Styled components for the new filter layout

- `app/split-lease/components/src/SearchFilters/types.ts` - Type definitions for filter state and options

- `app/split-lease/components/src/SearchFilters/index.ts` - Export file for SearchFilters component

- `app/split-lease/components/src/SearchFilters/components/BoroughDropdown.tsx` - Borough filter dropdown component

- `app/split-lease/components/src/SearchFilters/components/WeekPatternDropdown.tsx` - Week pattern filter dropdown component

- `app/split-lease/components/src/SearchFilters/components/PriceTierDropdown.tsx` - Price tier filter dropdown component

- `app/split-lease/components/src/SearchFilters/components/SortByDropdown.tsx` - Sort by filter dropdown component

- `app/split-lease/components/src/SearchFilters/components/DaySelector.tsx` - Calendar day selector component (S M T W T F S)

- `app/split-lease/components/src/SearchFilters/components/NeighborhoodSearch.tsx` - Neighborhood search/refine input component

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Capture Original Filter Layout
- Use Playwright MCP to navigate to https://app.split.lease/search
- Take detailed screenshots of the filter bar
- Document exact filter options from each dropdown (Borough, Week Pattern, Price Tier, Sort By)
- Document calendar selector layout and behavior
- Document neighborhood search input appearance and position
- Save screenshot analysis to document exact requirements

### 2. Create SearchFilters React Component Structure
- Create directory structure: `app/split-lease/components/src/SearchFilters/`
- Create `types.ts` with interfaces for:
  - `FilterState` (borough, week_pattern, price_tier, sort_by, check_in_day, check_out_day, neighborhood)
  - `FilterOptions` for each dropdown
  - `BoroughOption`, `WeekPatternOption`, `PriceTierOption`, `SortOption`
- Create `SearchFilters.styles.ts` with styled components for horizontal topbar layout
- Create component subdirectory: `app/split-lease/components/src/SearchFilters/components/`

### 3. Implement Borough Dropdown Component
- Create `components/BoroughDropdown.tsx`
- Implement dropdown with options: Manhattan, Brooklyn, Queens, Bronx, Staten Island
- Add onChange handler that updates filter state
- Style to match original website dropdown appearance
- Default to Manhattan
- Export from component index

### 4. Implement Week Pattern Dropdown Component
- Create `components/WeekPatternDropdown.tsx`
- Implement dropdown with options:
  - "Every week"
  - "One week on, one week off"
  - "Two weeks on, two weeks off"
  - "One week on, three weeks off"
- Add onChange handler
- Style to match original website
- Export from component index

### 5. Implement Price Tier Dropdown Component
- Create `components/PriceTierDropdown.tsx`
- Implement dropdown with options:
  - "< $200/night"
  - "$200-$350/night"
  - "$350-$500/night"
  - "$500+/night"
  - "All Prices"
- Map price tiers to actual min/max values
- Add onChange handler
- Style to match original website
- Export from component index

### 6. Implement Sort By Dropdown Component
- Create `components/SortByDropdown.tsx`
- Implement dropdown with options:
  - "Our Recommendations" (default)
  - "Price-Lowest to Highest"
  - "Most Viewed"
  - "Recently Added"
- Add onChange handler
- Style to match original website
- Export from component index

### 7. Implement Calendar Day Selector Component
- Create `components/DaySelector.tsx`
- Render 7 day buttons: S M T W T F S (Sunday through Saturday)
- Implement toggle functionality for check-in and check-out day selection
- Add visual states: default, selected check-in, selected check-out, hover
- Include logic for valid day ranges
- Style with proper spacing and colors matching original
- Export from component index

### 8. Implement Neighborhood Search Component
- Create `components/NeighborhoodSearch.tsx`
- Implement text input with search/filter functionality
- Add autocomplete dropdown showing filtered neighborhoods
- Filter neighborhoods based on selected borough
- Add onChange handler for search text
- Add onSelect handler for neighborhood selection
- Style to match original website search input
- Export from component index

### 9. Build Main SearchFilters Component
- Create `SearchFilters.tsx` as main container component
- Implement horizontal topbar layout using flexbox
- Arrange components in order: Borough → Week Pattern → Price Tier → Sort By
- Add DaySelector below or integrated with main filter bar
- Add NeighborhoodSearch input
- Implement state management using React hooks (useState)
- Add props: `onFilterChange`, `initialFilters`
- Implement filter change debouncing (500ms) for performance
- Add TypeScript prop types
- Export from index.ts

### 10. Update Styled Components
- In `SearchFilters.styles.ts`, create styled components:
  - `FilterBar` - horizontal flex container for topbar layout
  - `FilterGroup` - wrapper for each filter with proper spacing
  - `FilterLabel` - label styling for each filter
  - `DropdownWrapper` - consistent dropdown container styling
  - `DaySelectorWrapper` - container for calendar day selector
  - `SearchInputWrapper` - container for neighborhood search
- Match colors, fonts, spacing from original website
- Ensure responsive behavior for mobile screens
- Add hover and focus states

### 11. Export SearchFilters from Components Bundle
- Update `app/split-lease/components/src/index.ts`
- Add export: `export { SearchFilters } from './SearchFilters';`
- Add export: `export type { FilterState, FilterOptions } from './SearchFilters/types';`
- Ensure proper TypeScript types are exported

### 12. Build Components UMD Bundle
- Run `cd app/split-lease/components && npm run build`
- Verify `dist/split-lease-components.umd.cjs` is generated
- Verify `dist/style.css` includes new filter styles
- Check bundle size is reasonable

### 13. Update filters-island.umd.js
- Replace the `renderVanilla` function implementation (lines 82-162)
- Update `init` function to mount SearchFilters React component instead of vanilla HTML
- Update state management to handle new filter structure:
  - Replace `schedule_days` with `check_in_day`, `check_out_day`
  - Replace `price_min`, `price_max` with `price_tier`
  - Add `borough`, `week_pattern` fields
- Update URL parameter parsing to handle new filter fields
- Update `stringifyQuery` to serialize new filter structure
- Remove old price buckets, room types logic
- Ensure proper integration with `window.SLComponents.SearchFilters`

### 14. Update Search Page HTML
- In `app/split-lease/pages/search/index.html`
- Update `#sl-filters-root` container to support topbar layout
- Remove or update the `.sl-search-sidebar` wrapper if needed
- Ensure proper mount point for horizontal filters

### 15. Update CSS for Horizontal Layout
- In `app/split-lease/pages/search/css/styles.css`
- Replace sidebar styles (lines 35-78) with topbar styles
- Add horizontal flex layout for `.sl-search-layout`
- Update `.sl-search-sidebar` to be a topbar container
- Remove fixed width, add full-width horizontal styling
- Update responsive breakpoints for mobile

### 16. Update Responsive CSS
- In `app/split-lease/pages/search/css/responsive.css`
- Add mobile breakpoints for filter topbar
- Implement filter drawer/modal for mobile screens
- Ensure dropdowns work properly on mobile
- Test calendar day selector on touch devices

### 17. Test Filter Functionality
- Open `app/split-lease/pages/search/index.html` in browser
- Verify all 4 dropdowns render and function correctly
- Test borough selection updates neighborhoods
- Test week pattern selection
- Test price tier selection
- Test sort by selection
- Test calendar day selector (check-in/check-out)
- Test neighborhood search input and autocomplete
- Verify filter state updates properly

### 18. Test URL Synchronization
- Change each filter and verify URL updates with correct parameters
- Refresh page and verify filters restore from URL
- Test URL with all filters set
- Test URL with no filters (defaults)
- Verify URL parameters are properly encoded

### 19. Validate Against Original Website
- Compare side-by-side with https://app.split.lease/search
- Verify layout matches (horizontal topbar)
- Verify filter options match exactly
- Verify styling matches (colors, fonts, spacing)
- Verify interaction behaviors match
- Take screenshot for documentation

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd app/split-lease/components && npm run typecheck` - Verify TypeScript types are correct with no errors
- `cd app/split-lease/components && npm run build` - Build the UMD bundle and verify it succeeds without errors
- Open `app/split-lease/pages/search/index.html` in browser and verify filters render correctly
- Test each filter dropdown: Borough, Week Pattern, Price Tier, Sort By - verify all options work
- Test calendar day selector: click days S-S and verify check-in/check-out selection works
- Test neighborhood search: type text and verify filtering/autocomplete works
- Test URL sync: change filters, verify URL updates, refresh page, verify filters restore
- Visual comparison: Compare `app/split-lease/pages/search/index.html` with `https://app.split.lease/search` screenshot
- Test mobile responsive: resize browser to mobile width and verify filter drawer/modal works
- `cd app/split-lease/components && npm run typecheck` - Final type check to ensure no regressions

## Notes

**Context Files Referenced:**
- `C:\Users\Split Lease\splitleaseteam\!Agent Context and Tools\SL1\Practice TAC\z_Test Tac 2\Search TAC 2\apps\search_filters\README.md` - Contains full specification for proper filter implementation with 7 filter types
- `C:\Users\Split Lease\splitleaseteam\!Agent Context and Tools\SL1\Practice TAC\z_Test Tac 2\Search TAC 2\specs\chore-ab8feeed-rebuild-filters-match-original.md` - Documents the exact requirements for matching original website filters

**Key Differences to Address:**
1. **Layout**: Sidebar → Horizontal topbar
2. **Filter Count**: 4 basic → 7 proper filters
3. **Filter Types**: Generic → Specific (Borough, Week Pattern, Price Tier, Sort By, Day Selector, Neighborhood Search)
4. **Implementation**: Vanilla JS fallback → React components from UMD bundle
5. **Styling**: Basic CSS → Styled components matching original design

**Design Decisions:**
- Use React components built in the `components/` directory and exported via UMD bundle
- Maintain Islands Architecture pattern (static HTML + React islands)
- Keep existing URL synchronization infrastructure
- Use 500ms debouncing for filter changes
- Ensure backward compatibility with existing search functionality

**Performance Considerations:**
- Debounce filter changes to avoid excessive re-renders
- Lazy load neighborhood options based on borough selection
- Minimize bundle size by code splitting filter components if needed
- Use React.memo for dropdown components to prevent unnecessary re-renders

**Accessibility:**
- Ensure all dropdowns have proper ARIA labels
- Make calendar day selector keyboard accessible
- Add proper focus management for filter interactions
- Ensure screen reader compatibility

**Browser Compatibility:**
- Test in Chrome, Firefox, Safari, Edge
- Ensure ES2020 compatibility as documented in README
- Test mobile browsers (iOS Safari, Chrome Mobile)
