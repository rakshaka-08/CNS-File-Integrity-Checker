# CNS - File Integrity Checker

## Project Description

The File Integrity Checker is a Cyber and Network Security mini-project developed using Python and Streamlit. It uses the SHA-256 cryptographic hashing algorithm to check whether files have been modified.

## Features

- Generate SHA-256 hashes for uploaded files.
- Verify file integrity by comparing original and current hashes.
- Detect unchanged and modified files.
- Save verification history using CSV storage.
- Manage and save original hash references.
- Use saved hash references during file verification.
- Download verification history as a CSV file.

## Technologies Used

- Python
- Streamlit
- SHA-256
- hashlib
- Pandas
- CSV file storage

## Project Structure

```text
CNS-File-Integrity-Checker/
├── app.py
├── hashing.py
├── verification.py
├── history.csv
├── references.csv
├── test_hashing.py
├── test_verification.py
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rakshaka-08/CNS-File-Integrity-Checker/issues
```

2. Open the project folder:

```bash
cd CNS-File-Integrity-Checker
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
streamlit run app.py
```

## How to Use

1. Open the dashboard in your browser.
2. Select Generate SHA-256 Hash to upload a file and generate its hash.
3. Select Manage Hash References to save an original hash.
4. Select Verify File Integrity to compare the current file with its original hash.
5. Open History to view previous hashing and verification activities.

## Testing

The project includes tests for SHA-256 hash generation and file integrity verification.

Run the tests using:

```bash
python test_hashing.py
python test_verification.py
```

## Team Contributions

- Diya Patil
- Raksha K A
- Sanvi M
- Sahana E


## Conclusion

This project demonstrates how cryptographic hashing can be used to identify changes in files and help maintain file integrity.