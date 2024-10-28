

function periodic_git_commit() {
    echo "Periodically commit changes to git"
    echo "'.env' file contents:"
    cat ./periodic-git-commit/.env
    echo "Starting..."
    ./periodic-git-commit/periodic_git_commit.py
    echo "Done."
}