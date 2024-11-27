
DEVELOPMENT_TOOLS_DIR=~/development/github/development-tools

function periodic_git_commit() {
    echo "Periodically commit changes to git"
    echo "-------------------------------------------"
    echo "'.env' file contents:"
    cat $DEVELOPMENT_TOOLS_DIR/periodic-git-commit/.env
    echo ""
    echo "-------------------------------------------"
    echo "Starting..."
    echo ""
    source $DEVELOPMENT_TOOLS_DIR/periodic-git-commit/.venv/bin/activate
    python3 $DEVELOPMENT_TOOLS_DIR/periodic-git-commit/periodic_git_commit.py
    echo "Done."
}