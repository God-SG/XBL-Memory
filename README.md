<div align="center">
  <img src="https://github.com/user-attachments/assets/cfed50ce-01b0-43e4-8602-41ffae3ce4a4" alt="" height="200">
</div>
<p align="center">
  <a href="https://www.python.org/downloads/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/Red-Discordbot">
  </a>
  <a href="https://github.com/God-SG/XBL-Memory/blob/main/XBL-Memory.py">
    <img src="https://img.shields.io/badge/python-red.svg" alt="xbox_api.py">
  </a>
  <a href="[https://github.com/God-SG/XBL-Memory/blob/main/XBL-Memory.py](https://www.xbox.com/en-US)">
    <img src="https://img.shields.io/badge/Xbox_Live_Authentication-107C10.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNzIuMzcgMzcyLjU3Ij48cGF0aCBmaWxsPSIjZmZmZmZmIiBkPSJNMTY3LjYyIDM3MS44MWMtMjguNjgtMi43NS01Ny43Mi0xMy4wNS04Mi42Ny0yOS4zMi0yMC45LTEzLjY0LTI1LjYzLTE5LjI1LTI1LjYzLTMwLjQ0IDAtMjIuNDcgMjQuNzEtNjEuODQgNjctMTA2LjcxIDI0LTI1LjQ5IDU3LjQ2LTU1LjM2IDYxLjA3LTU0LjU1IDcuMDMgMS41NyA2My4yNSA1Ni40MSA4NC4zIDgyLjIyIDMzLjI4IDQwLjgyIDQ4LjU4IDc0LjI1IDQwLjggODkuMTUtNS45IDExLjMzLTQyLjU3IDMzLjQ3LTY5LjUgNDEuOTctMjIuMiA3LjAxLTUxLjM2IDkuOTgtNzUuMzcgNy42OHpNMzEuMDkgMjg4LjY4Yy0xNy4zNy0yNi42NS0yNi4xNS01Mi44OS0zMC4zOC05MC44My0xLjQtMTIuNTMtLjktMTkuNyAzLjE4LTQ1LjQyQzguOTcgMjIwLjM4IDI3LjIyIDE4My4zIDQ5LjE1IDE2MC40OGM5LjM0LTkuNzIgMTAuMTgtOS45NiAyMS41Ni02LjEyIDEzLjgzIDQuNjYgMjguNiAxNC44NiA1MS41IDM1LjU3bDEzLjM2IDEyLjA4LTcuMyA4Ljk2Yy0zMy44NyA0MS42MS02OS42MyAxMDAuNi04My4xIDEzNy4wOS03LjMzIDE5Ljg0LTEwLjI4IDM5Ljc1LTcuMTMgNDguMDQgMi4xMyA1LjYuMTcgMy41MS02Ljk1LTcuNDJ6bTMwNC45MiA0LjUzYzEuNzEtOC4zOC0uNDYtMjMuNzYtNS41NC0zOS4yOC0xMS4wMi0zMy42LTQ3Ljg0LTk2LjEyLTgxLjY2LTEzOC42M2wtMTAuNjQtMTMuMzggMTEuNTItMTAuNTdjMTUuMDMtMTMuODEgMjUuNDctMjIuMDggMzYuNzQtMjkuMSA4Ljg5LTUuNTQgMjEuNTktMTAuNDQgMjcuMDUtMTAuNDQgMy4zNyAwIDE1LjIyIDEyLjMgMjQuNzggMjUuNzIgMTQuODIgMjAuNzkgMjUuNzIgNDUuOTkgMzEuMjQgNzIuMjIgMy41NyAxNi45NSAzLjg3IDUzLjIzLjU4IDcwLjE0LTIuNyAxMy44OC04LjQgMzEuODctMTMuOTcgNDQuMDgtNC4xNyA5LjE1LTE0LjUzIDI2LjkxLTE5LjA4IDMyLjY5LTIuMzMgMi45Ny0yLjMzIDIuOTctMS4wMi0zLjQ1ek0xNzAuNjkgNDUuNDZjLTE1LjYtNy45Mi0zOS42Ny0xNi40My01Mi45Ny0xOC43MS00LjY2LS44LTEyLjYxLTEuMjUtMTcuNjctMS0xMC45Ny41Ni0xMC40OC0uMDIgNy4xMi04LjMzIDE0LjYzLTYuOTEgMjYuODMtMTAuOTggNDMuNC0xNC40NkMxNjkuMjEtMS4wNSAyMDQuMjQtMS4xIDIyMi41OCAyLjc3YzE5LjggNC4xNyA0My4xMyAxMi44NSA1Ni4yOCAyMC45NGwzLjkgMi40LTguOTYtLjQ1Yy0xNy44MS0uOS00My43NiA2LjMtNzEuNjMgMTkuODYtOC40IDQuMS0xNS43MiA3LjM2LTE2LjI1IDcuMjYtLjUzLS4xLTcuMzgtMy40NC0xNS4yMy03LjQyeiIvPjwvc3ZnPg==" alt="Xbox Live Authentication Badge">
  </a>
</p>

# XBL-Memory

**XBL-Memory** is a Python-based tool designed to extract and validate Xbox Live tokens directly from the memory of the Xbox app on Windows systems. The tool leverages Windows API calls and memory scanning techniques to locate tokens with the signature pattern `XBL3.0 x=`, validate them via asynchronous HTTP requests, and automatically copy a valid token to the clipboard while saving it to a file.

---

## Overview

This utility is intended for ethical hacking and cybersecurity research. It works by:

- **Terminating existing Xbox processes:** Ensures that the environment is clean for token extraction.
- **Launching the Xbox app:** Automatically starts the app if it isn’t running.
- **Memory scanning:** Searches the process memory of the Xbox app for token patterns.
- **Token validation:** Uses asynchronous HTTP requests to validate the token.
- **Output handling:** Saves the valid token to a file (`xbl_token.txt`) and copies it to your clipboard.

---

## Features

- **Automated Process Management:** Terminates conflicting Xbox processes and starts a fresh instance of the Xbox app.
- **Memory Scanning:** Utilizes Windows API (`VirtualQueryEx`, `ReadProcessMemory`) to scan for memory regions containing the token pattern.
- **Token Extraction & Validation:** Extracts tokens and validates them by sending an HTTP request to Xbox Live profile settings.
- **User-Friendly Feedback:** Uses color-coded terminal messages and a splash of ASCII art for a playful touch.
- **Clipboard Integration:** Automatically copies the valid token to your clipboard for easy access.

---

## Requirements

- **Operating System:** Windows (the tool utilizes Windows-specific API calls)
- **Python:** Version 3.x
- **Dependencies:**
  - [psutil](https://pypi.org/project/psutil/)
  - [aiohttp](https://pypi.org/project/aiohttp/)
  - [pyperclip](https://pypi.org/project/pyperclip/)
  - Standard libraries: `ctypes`, `asyncio`, `subprocess`, etc.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/God-SG/XBL-Memory.git
   cd XBL-Memory
   ```
2. **Install Dependencies:**
   ```bash
   pip install psutil aiohttp pyperclip
   ```

---

## Usage

Run the script using Python:
```bash
python XBL-Memory.py
```

The tool will:
- Terminate any running Xbox processes.
- Launch a fresh instance of the Xbox app.
- Begin scanning for the Xbox Live token every 5 seconds for up to 90 seconds.
- Validate the token when found, copy it to the clipboard, and save it to `xbl_token.txt`.

Follow the on-screen prompts to complete the process.

---

## Disclaimer

**Important:** This tool is provided for educational and ethical cybersecurity research purposes only. Unauthorized access or misuse of systems is illegal. Use it responsibly and ensure you have the proper permissions before running this tool on any system.

---

## Contributing

Contributions, suggestions, and improvements are welcome! Please open an issue or submit a pull request if you have any enhancements or bug fixes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/God-SG/XBL-Memory/blob/main/LICENSE) file for details.
