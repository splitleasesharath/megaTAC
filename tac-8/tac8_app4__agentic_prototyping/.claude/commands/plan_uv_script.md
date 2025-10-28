# Plan UV Script

Create a plan for building a net new UV single-file script MVP from scratch based on the prompt. This command designs and architects a complete Python script application using UV's inline dependency management, creating a comprehensive implementation roadmap.

## Variables
adw_id: $1
prompt: $2
app_name: <Create a concise app name based on the prompt>

## Instructions

- If the `adw_id` or `prompt` is not provided, stop and ask the user to provide them.
- IMPORTANT: Create a concise `app_name` based on the `prompt`. Use underscores not dashes or spaces when generating the name (e.g., `todo_tracker`, `api_client`). This will be used as the name of the directory the application will be created in.
- IMPORTANT: Create a plan to build a new UV single-file script application from scratch based on the `prompt`
- The plan should be appropriately detailed based on the task complexity
- Create the plan in the `specs/` directory with filename: `plan-{app_name}-uv-script.md`
- Research the codebase starting with `README.md`
- IMPORTANT: When you finish your plan, return only the path to the plan file created.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value
- Use your reasoning model: ULTRATHINK about the task requirements and appropriate level of planning needed
- Follow existing patterns and conventions in the codebase

## Workflow

1. **Initialize UV Script Structure**: Create `apps/{app_name}/` directory and run `uv init --script apps/{app_name}/{app_name}.py --python 3.10` to create the script template
2. **Research the Codebase**: Start with `README.md` to understand the project structure, existing patterns, and conventions. Expand from there based on the `prompt`
3. **Write Plan**: Create the plan document in `specs/` following the Plan Format template

## Codebase Structure

- `README.md` - Project overview and instructions (start here)
- `adws/` - AI Developer Workflow scripts and modules
- `apps/` - Application layer you'll be working in
- `apps/{app_name}/{app_name}.py` - Your UV script application that you'll focus on when implementing the plan
- `.claude/commands/` - Claude command templates
- `specs/` - Specification and plan documents
- `ai_docs/uv-scripts.md` - UV single-file script development reference documentation with inline dependencies

## Plan Format

```md
# Plan: <task name>

## Metadata
adw_id: `{adw_id}`
prompt: `{prompt}`
app_name: `{app_name}`
task_type: <prototype|utility|tool|automation>
complexity: <simple|medium|complex>

## Task Description
<describe the task in detail based on the prompt>

## Objective
<clearly state what will be accomplished when this plan is complete>

<if task_type is feature or complexity is medium/complex, include these sections:>
## Problem Statement
<clearly define the specific problem or opportunity this task addresses>

## Solution Approach
<describe the proposed solution approach and how it addresses the objective>
</if>

## Relevant Files
Use these files to complete the task:

<list files relevant to the task with bullet points explaining why. Include new files to be created under an h3 'New Files' section if needed>

<if complexity is medium/complex, include this section:>
## Implementation Phases
### Phase 1: Foundation
<describe any foundational work needed>

### Phase 2: Core Implementation
<describe the main implementation work>

### Phase 3: Integration & Polish
<describe integration, testing, and final touches>
</if>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers with bullet points. Start with foundational changes then move to specific changes. Last step should validate the work>

### 1. <First Task Name>
- <specific action>
- <specific action>

### 2. <Second Task Name>
- <specific action>
- <specific action>

<continue with additional tasks as needed>

<if task_type is feature or complexity is medium/complex, include this section:>
## Testing Strategy
<describe testing approach, including unit tests and edge cases as applicable>
</if>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the task to be considered complete>

## Validation Commands
Execute these commands to validate the task is complete:

<list specific commands to validate the work. Be precise about what to run>
- Example: `uv run apps/{app_name}/script.py --help` - Test script execution

## Notes
<optional additional context, considerations, or dependencies. Specify UV inline dependencies needed>
```

## Task
Use the task description from the `prompt` variable.

## Report

IMPORTANT: Exclusively return the path to the plan file created.