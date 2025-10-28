"""Git operations for ADW composable architecture.

Provides centralized git operations that build on top of github.py module.
"""

import subprocess
import json
import logging
import os
from typing import Optional, Tuple

# Import GitHub functions from existing module
from adw_modules.github import get_repo_url, extract_repo_path, make_issue_comment


def get_app_dir() -> str:
    """Get the app directory where the git repository is located."""
    # __file__ is in tac-5/adws/adw_modules/git_ops.py
    # We need to go up to tac-5/ level, then join with app/
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(script_dir, "app")


def get_current_branch() -> str:
    """Get current git branch name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True,
        cwd=get_app_dir()  # Run from app/ where .git exists
    )
    return result.stdout.strip()


def push_branch(branch_name: str) -> Tuple[bool, Optional[str]]:
    """Push current branch to remote. Returns (success, error_message)."""
    result = subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        capture_output=True, text=True,
        cwd=get_app_dir()  # Run from app/ where .git exists
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, None


def check_pr_exists(branch_name: str) -> Optional[str]:
    """Check if PR exists for branch. Returns PR URL if exists."""
    # Use github.py functions to get repo info
    try:
        repo_url = get_repo_url()
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return None
    
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", repo_path, "--head", branch_name, "--json", "url"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        prs = json.loads(result.stdout)
        if prs:
            return prs[0]["url"]
    return None


def create_branch(branch_name: str) -> Tuple[bool, Optional[str]]:
    """Create and checkout a new branch. Returns (success, error_message)."""
    app_dir = get_app_dir()

    # Create branch
    result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        capture_output=True, text=True,
        cwd=app_dir  # Run from app/ where .git exists
    )
    if result.returncode != 0:
        # Check if error is because branch already exists
        if "already exists" in result.stderr:
            # Try to checkout existing branch
            result = subprocess.run(
                ["git", "checkout", branch_name],
                capture_output=True, text=True,
                cwd=app_dir  # Run from app/ where .git exists
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, None
        return False, result.stderr
    return True, None


def commit_changes(message: str) -> Tuple[bool, Optional[str]]:
    """Stage all changes and commit. Returns (success, error_message)."""
    app_dir = get_app_dir()

    # Check if there are changes to commit
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True,
        cwd=app_dir  # Run from app/ where .git exists
    )
    if not result.stdout.strip():
        return True, None  # No changes to commit

    # Stage all changes
    result = subprocess.run(
        ["git", "add", "-A"],
        capture_output=True, text=True,
        cwd=app_dir  # Run from app/ where .git exists
    )
    if result.returncode != 0:
        return False, result.stderr

    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True, text=True,
        cwd=app_dir  # Run from app/ where .git exists
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, None


def finalize_git_operations(state: 'ADWState', logger: logging.Logger) -> None:
    """Standard git finalization: push branch and create/update PR."""
    branch_name = state.get("branch_name")
    if not branch_name:
        # Fallback: use current git branch if not main
        current_branch = get_current_branch()
        if current_branch and current_branch != "main":
            logger.warning(f"No branch name in state, using current branch: {current_branch}")
            branch_name = current_branch
        else:
            logger.error("No branch name in state and current branch is main, skipping git operations")
            return
    
    # Always push
    success, error = push_branch(branch_name)
    if not success:
        logger.error(f"Failed to push branch: {error}")
        return
    
    logger.info(f"Pushed branch: {branch_name}")
    
    # Handle PR
    pr_url = check_pr_exists(branch_name)
    issue_number = state.get("issue_number")
    adw_id = state.get("adw_id")
    
    if pr_url:
        logger.info(f"Found existing PR: {pr_url}")
        # Post PR link for easy reference
        if issue_number and adw_id:
            make_issue_comment(
                issue_number,
                f"{adw_id}_ops: ✅ Pull request: {pr_url}"
            )
    else:
        # Create new PR - fetch issue data first
        if issue_number:
            try:
                repo_url = get_repo_url()
                repo_path = extract_repo_path(repo_url)
                from adw_modules.github import fetch_issue
                issue = fetch_issue(issue_number, repo_path)
                
                from adw_modules.workflow_ops import create_pull_request
                pr_url, error = create_pull_request(branch_name, issue, state, logger)
            except Exception as e:
                logger.error(f"Failed to fetch issue for PR creation: {e}")
                pr_url, error = None, str(e)
        else:
            pr_url, error = None, "No issue number in state"
        
        if pr_url:
            logger.info(f"Created PR: {pr_url}")
            # Post new PR link
            if issue_number and adw_id:
                make_issue_comment(
                    issue_number,
                    f"{adw_id}_ops: ✅ Pull request created: {pr_url}"
                )
        else:
            logger.error(f"Failed to create PR: {error}")