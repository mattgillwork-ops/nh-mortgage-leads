import subprocess
import os
import logging
import shutil

class GitManager:
    """
    Anti-Gravity Git Integration Tool
    Provides a high-level API for git operations used by the DevOps agent.
    """
    def __init__(self, repo_path=None):
        if repo_path is None:
            # Default to the workspace root
            self.repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.repo_path = os.path.abspath(repo_path)
            
        self.logger = logging.getLogger("GitManager")

    def _run_git(self, cmd_args):
        """Internal helper to run git commands via subprocess."""
        # Try default 'git' first, then common Windows path
        git_executable = "git"
        if os.name == "nt":
            # Check if 'git' is in PATH
            if not shutil.which("git"):
                common_path = r"C:\Program Files\Git\bin\git.exe"
                if os.path.exists(common_path):
                    git_executable = common_path

        try:
            result = subprocess.run(
                [git_executable] + cmd_args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',
                errors='replace'
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            stderr_text = e.stderr.strip() if e.stderr else "No stderr output"
            error_msg = f"Git Error ({' '.join(cmd_args)}): {stderr_text}"
            self.logger.error(error_msg)
            return f"[ERROR] {error_msg}"
        except Exception as e:
            return f"[ERROR] Unexpected failure: {str(e)}"

    def init_repo(self):
        """Initialize a git repository if it doesn't already exist."""
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            return self._run_git(['init'])
        return "Repository already initialized."

    def add_files(self, files=None):
        """Add files to the staging area. Defaults to all (.)."""
        if files is None:
            return self._run_git(['add', '.'])
        if isinstance(files, list):
            return self._run_git(['add'] + files)
        return self._run_git(['add', files])

    def commit(self, message):
        """Commit staged changes."""
        if not message:
            return "[ERROR] Commit message cannot be empty."
        return self._run_git(['commit', '-m', message])

    def create_branch(self, branch_name):
        """Create and switch to a new branch."""
        return self._run_git(['checkout', '-b', branch_name])

    def switch_branch(self, branch_name):
        """Switch to an existing branch."""
        return self._run_git(['checkout', branch_name])

    def show_status(self):
        """Return the current git status."""
        return self._run_git(['status'])

    def show_log(self, n=5):
        """Return the last n commit logs."""
        return self._run_git(['log', '-n', str(n), '--oneline'])

    def set_remote(self, url, name="origin"):
        """Add or update a remote origin."""
        # Try to add first
        res = self._run_git(['remote', 'add', name, url])
        if "[ERROR]" in res and "already exists" in res:
            # If exists, set-url instead
            return self._run_git(['remote', 'set-url', name, url])
        return res

    def list_remotes(self):
        """List all configured remotes."""
        return self._run_git(['remote', '-v'])

    def push(self, branch="main", remote="origin"):
        """Push changes to the remote repository."""
        return self._run_git(['push', remote, branch])

# Example Usage
if __name__ == "__main__":
    gm = GitManager()
    print("Status:", gm.show_status())
