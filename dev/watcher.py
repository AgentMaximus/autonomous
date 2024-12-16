# watcher.py - Git changes watcher
import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class GitChangeHandler(FileSystemEventHandler):
    def __init__(self, server_process):
        self.server_process = server_process
        self.last_restart = time.time()
        self.cooldown = 2  # Minimum seconds between restarts

    def on_modified(self, event):
        if time.time() - self.last_restart < self.cooldown:
            return
        
        if not event.is_directory:
            try:
                # Check if file is tracked by git
                result = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", event.src_path],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:  # File is tracked by git
                    print(f"\nGit change detected in {event.src_path}")
                    self.restart_server()
                    self.last_restart = time.time()
                    
            except subprocess.CalledProcessError:
                pass

    def restart_server(self):
        print("Restarting FastAPI server...")
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        
        self.server_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def run_watcher():
    # Start the FastAPI server
    server_process = subprocess.Popen(
        [sys.executable, "../autonomous_clone/dev/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Setup the file watcher
    event_handler = GitChangeHandler(server_process)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        print("Watching for Git changes... Press Ctrl+C to exit")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if server_process:
            server_process.terminate()
    observer.join()

if __name__ == "__main__":
    run_watcher()