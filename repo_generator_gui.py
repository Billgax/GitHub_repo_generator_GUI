import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime, timedelta
import os
import random
import subprocess
import sys


class RepositoryGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Repository Generator")
        self.root.geometry("600x500")
        self.create_widgets()

    def create_widgets(self):
        # Input Fields
        ttk.Label(self.root, text="Repository URL (optional):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.repo_url = ttk.Entry(self.root, width=50)
        self.repo_url.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="User Name (optional):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.user_name = ttk.Entry(self.root, width=50)
        self.user_name.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="User Email (optional):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.user_email = ttk.Entry(self.root, width=50)
        self.user_email.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Days Before:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.days_before = ttk.Entry(self.root, width=10)
        self.days_before.insert(0, "365")
        self.days_before.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.root, text="Days After:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.days_after = ttk.Entry(self.root, width=10)
        self.days_after.insert(0, "0")
        self.days_after.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.root, text="Max Commits Per Day:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.max_commits = ttk.Entry(self.root, width=10)
        self.max_commits.insert(0, "10")
        self.max_commits.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.root, text="Frequency (%):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.frequency = ttk.Entry(self.root, width=10)
        self.frequency.insert(0, "80")
        self.frequency.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.no_weekends = tk.BooleanVar()
        ttk.Checkbutton(self.root, text="No Weekends", variable=self.no_weekends).grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Buttons
        ttk.Button(self.root, text="Generate Repository", command=self.generate_repository).grid(row=8, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="Clear Logs", command=self.clear_logs).grid(row=8, column=1, padx=10, pady=10)

        # Logs
        self.log_area = scrolledtext.ScrolledText(self.root, width=70, height=20, state="disabled")
        self.log_area.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def generate_repository(self):
        """Generate the repository based on user inputs."""
        try:
            config = {
                "repository": self.repo_url.get(),
                "user_name": self.user_name.get(),
                "user_email": self.user_email.get(),
                "days_before": int(self.days_before.get()),
                "days_after": int(self.days_after.get()),
                "max_commits": int(self.max_commits.get()),
                "frequency": int(self.frequency.get()),
                "no_weekends": self.no_weekends.get(),
            }

            self.log("Starting repository generation...")
            self.log(f"Configuration: {config}")

            # Call the repository generation logic
            generate_repository(config, self.log)

            self.log("Repository generation completed successfully!")
        except Exception as e:
            self.log(f"Error: {e}")

    def log(self, message: str):
        """Log messages to the log area."""
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.config(state="disabled")
        self.log_area.yview(tk.END)

    def clear_logs(self):
        """Clear the log area."""
        self.log_area.config(state="normal")
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state="disabled")


def generate_repository(config: dict, log_func):
    """Generate the Git repository with contributions."""
    curr_date = datetime.now()
    directory = (
        f"repository-{curr_date.strftime('%Y-%m-%d-%H-%M-%S')}"
        if not config["repository"]
        else config["repository"].split("/")[-1].replace(".git", "")
    )

    os.makedirs(directory, exist_ok=True)
    os.chdir(directory)
    run_command(["git", "init", "-b", "main"], log_func)

    if config["user_name"]:
        run_command(["git", "config", "user.name", config["user_name"]], log_func)
    if config["user_email"]:
        run_command(["git", "config", "user.email", config["user_email"]], log_func)

    start_date = curr_date.replace(hour=20, minute=0) - timedelta(days=config["days_before"])
    for day in (start_date + timedelta(days=n) for n in range(config["days_before"] + config["days_after"])):
        if (not config["no_weekends"] or day.weekday() < 5) and random.randint(0, 100) < config["frequency"]:
            for commit_time in (
                day + timedelta(minutes=m)
                for m in range(random.randint(1, config["max_commits"]))
            ):
                make_contribution(commit_time, log_func)

    if config["repository"]:
        run_command(["git", "remote", "add", "origin", config["repository"]], log_func)
        run_command(["git", "branch", "-M", "main"], log_func)
        run_command(["git", "push", "-u", "origin", "main"], log_func)


def make_contribution(date: datetime, log_func):
    """Make a Git contribution for the given date."""
    with open("README.md", "a") as file:
        file.write(f"{generate_commit_message(date)}\n\n")
    run_command(["git", "add", "."], log_func)
    run_command(
        [
            "git",
            "commit",
            "-m",
            f'"{generate_commit_message(date)}"',
            "--date",
            date.strftime('"%Y-%m-%d %H:%M:%S"'),
        ],
        log_func,
    )


def generate_commit_message(date: datetime) -> str:
    """Generate a commit message based on the date."""
    return date.strftime("Contribution: %Y-%m-%d %H:%M")


def run_command(commands: list, log_func):
    """Run a shell command and log the output."""
    try:
        log_func(f"Running command: {' '.join(commands)}")
        subprocess.run(commands, check=True)
    except subprocess.CalledProcessError as e:
        log_func(f"Command failed: {e}")
        raise


if __name__ == "__main__":
    root = tk.Tk()
    app = RepositoryGeneratorApp(root)
    root.mainloop()