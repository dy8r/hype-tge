
# Hype-TGE: Hyperliquid Terms of Service Signing

This project automates the process of signing the terms of service (ToS) for **Hyperliquid** using private keys stored in `pks.txt`. It fetches points, checks account eligibility, and stores the results in a CSV file for further analysis. A proxy can be optionally configured in the `main.py`.

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Configuration](#configuration)  
4. [How to Run](#how-to-run)  
5. [Usage Workflow](#usage-workflow)  
6. [File Structure](#file-structure)

---

## Features

- **Automatic ToS Signing:** Uses private keys to sign terms of service for Hyperliquid.
- **Points Tracking:** Fetches user points and logs them in `results.csv`.
- **CSV-based Logging:** Records user data (address, points, genesis acceptance) in a CSV file.
- **Proxy Support:** Optional proxy configuration available in `main.py`.
- **Error Handling:** Skips already processed addresses and handles network errors with retries.

---

## Installation

1. **Install Python (if not installed):**
   - [Download Python](https://www.python.org/downloads/) and follow the installation instructions.
   
2. **Clone this repository:**
   ```bash
   git clone <your-repo-url>
   cd HYPE-TGE
   ```

3. **Install dependencies using `pip`:**
   ```bash
   pip3 install -r requirements.txt
   ```

---

## Configuration

### 1. **Private Keys File (`pks.txt`):**
   - Place the private keys, one per line, in the `pks.txt` file.

   **Example:**
   ```
   0xabc123...
   0xdef456...
   ```

### 2. **Optional Proxy Configuration:**
   - Set the proxy in `main.py` by uncommenting and providing the correct format.

   ```python
   # PROXY = "http://username:pass@ip:port"
   PROXY = "http://your-proxy-here"
   ```

---

## How to Run

1. **Initialize the CSV and Start the Script:**

   ```bash
   python3 main.py
   ```

2. **Expected Output:**
   - The script will:
     - Print total points fetched.
     - Process each private key.
     - Log account points and ToS acceptance status in `results.csv`.

---

## Usage Workflow

1. **Initial Setup:**
   - Ensure your private keys are in `pks.txt`.
   - Configure the optional proxy if needed.

2. **Script Execution:**
   - The script reads the private keys, checks if the address has been processed, fetches points, and tries to accept the ToS if applicable.

3. **Results in `results.csv`:**
   - The output CSV file contains the following fields:
     - **address**: Wallet address.
     - **points**: Points fetched for the account.
     - **accepted_genesis**: Whether the genesis has been accepted.

4. **Handling Errors:**
   - If an address is already processed, it will be skipped.
   - Errors will be printed to the console, and the script will retry after a random sleep interval.

---

## File Structure

```
HYPE-TGE/
│
├── hyperliquid_lib/         # Hyperliquid API library
├── .gitignore               # Files and directories to ignore in git
├── main.py                  # Main script to execute
├── pks.txt                  # Private keys (one per line)
├── requirements.txt         # Dependencies
├── results.csv              # Output CSV with fetched data
├── signing.py               # Helper functions for signing ToS
```

---

## Example CSV Output

```
address,points,accepted_genesis
0xabc123...,1000,True
0xdef456...,0,Not eligible
```

---

Feel free to reach out if you encounter any issues or need further assistance. Happy automating! 🎉
