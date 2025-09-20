#!/bin/bash

# Sync script for keeping local and remote repositories in sync
# Best practices for Git workflow

set -e

echo "🔄 Repository Sync Utility"
echo "========================="

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ Not in a Git repository"
        exit 1
    fi
}

# Function to check for uncommitted changes
check_uncommitted_changes() {
    if ! git diff-index --quiet HEAD --; then
        echo "⚠️ You have uncommitted changes:"
        git status --porcelain
        echo ""
        read -p "Do you want to commit these changes? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            read -p "Enter commit message: " commit_msg
            git commit -m "$commit_msg"
        else
            echo "❌ Please commit or stash your changes before syncing"
            exit 1
        fi
    fi
}

# Function to sync with remote
sync_with_remote() {
    current_branch=$(git branch --show-current)
    echo "📋 Current branch: $current_branch"
    
    echo "📥 Fetching latest changes..."
    git fetch origin
    
    echo "🔄 Pulling latest changes..."
    git pull origin $current_branch
    
    echo "📤 Pushing local changes..."
    git push origin $current_branch
    
    echo "✅ Sync complete!"
}

# Function to show repository status
show_status() {
    echo "📊 Repository Status:"
    echo "==================="
    echo "Branch: $(git branch --show-current)"
    echo "Last commit: $(git log -1 --pretty=format:'%h - %s (%cr) <%an>')"
    echo ""
    echo "Status:"
    git status --short
    echo ""
    echo "Remote status:"
    git remote -v
}

# Main script
main() {
    check_git_repo
    
    case "${1:-status}" in
        "status")
            show_status
            ;;
        "sync")
            check_uncommitted_changes
            sync_with_remote
            ;;
        "quick-commit")
            if [ -z "$2" ]; then
                echo "❌ Please provide a commit message"
                echo "Usage: $0 quick-commit 'Your commit message'"
                exit 1
            fi
            git add .
            git commit -m "$2"
            git push origin $(git branch --show-current)
            echo "✅ Quick commit and push complete!"
            ;;
        *)
            echo "Usage: $0 [status|sync|quick-commit 'message']"
            echo ""
            echo "Commands:"
            echo "  status        - Show repository status"
            echo "  sync          - Sync with remote repository"
            echo "  quick-commit  - Add, commit, and push changes"
            ;;
    esac
}

main "$@"