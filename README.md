# Autonomous Project

## Overview
The `autonomous` project provides an automated solution for real-time server management using FastAPI and a git changes watcher. This document outlines setup, usage, and deployment instructions.

---

## Deployment

### Prerequisites
- Python 3.8+
- Git installed on your machine.

---

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AgentMaximus/autonomous.git
   ```
2. **Navigate to the Project Directory**
   ```bash
   cd autonomous/dev
   ```
3. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Server

1. **Start the FastAPI Server**
   - Ensure you are in the `dev` directory where `main.py` is located.
   ```bash
   uvicorn main:app --reload
   ```
   - Access the server at `http://localhost:8000`

2. **Run the Watcher for Git Changes**
   - This will automatically refresh the server on changes.
   ```bash
   python watcher.py
   ```

---

## Important Notes
- The server automatically reloads when changes in Git-tracked files are detected.
- Ensure all necessary environment variables are configured.

---

## Usage
- FastAPI provides an interactive API documentation at `/docs`.

---

## License
- Licensed under the MIT License.

---

## Contributing
- Fork this repository and propose your changes via pull request.

---

This document was last updated on Dec 16, 2024.