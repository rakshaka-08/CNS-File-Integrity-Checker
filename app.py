
import streamlit as st
import hashlib
import os
from hashing import calculate_sha256
from verification import verify_file

# Page configuration
st.set_page_config(
    page_title="File Integrity Checker",
    page_icon="🔐",
    layout="centered"
)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Main heading
st.title("🔐 File Integrity Checker")
st.write("A simple tool to generate SHA-256 hashes and verify file integrity.")

st.divider()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose an option",
    ["Home", "Generate SHA-256 Hash", "Verify File Integrity", "History", "About"]
)

# Home page
if page == "Home":
    st.header("Welcome")
    st.write(
        "This application helps you check whether a file has been changed "
        "by using the SHA-256 hashing algorithm."
    )

    st.subheader("Available Features")
    st.write("- Generate SHA-256 hash of a file")
    st.write("- Verify whether a file has been modified")
    st.write("- View previous verification activities")

# Generate hash page
elif page == "Generate SHA-256 Hash":
    st.header("Generate SHA-256 Hash")

    uploaded_file = st.file_uploader(
        "Upload a file",
        key="hash_upload"
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        st.success("Hash generated successfully!")
        st.write("**File name:**", uploaded_file.name)
        st.code(file_hash, language="text")

        if st.button("Save to History"):
            st.session_state.history.append({
                "file": uploaded_file.name,
                "hash": file_hash,
                "status": "Hash Generated"
            })
            st.success("Hash saved to history.")

# Verify file page
elif page == "Verify File Integrity":
    st.header("Verify File Integrity")

    uploaded_file = st.file_uploader(
        "Upload the file you want to verify",
        key="verify_upload"
    )

    original_hash = st.text_input(
        "Enter the original SHA-256 hash"
    )

    if st.button("Verify File"):
        if uploaded_file is None:
            st.warning("Please upload a file.")

        elif not original_hash.strip():
            st.warning("Please enter the original SHA-256 hash.")

        elif len(original_hash.strip()) != 64 or any(
            char not in "0123456789abcdefABCDEF"
            for char in original_hash.strip()
        ):
            st.error("Please enter a valid 64-character SHA-256 hash.")

        else:
            current_hash = hashlib.sha256(
                uploaded_file.getvalue()
            ).hexdigest()

            if current_hash == original_hash.strip().lower():
                st.success("File is unchanged. Integrity verified.")
                status = "Unchanged"
            else:
                st.error("File has been modified!")
                status = "Modified"

            st.write("**File name:**", uploaded_file.name)
            st.write("**Current SHA-256 hash:**")
            st.code(current_hash, language="text")

            st.session_state.history.append({
                "file": uploaded_file.name,
                "hash": current_hash,
                "status": status
            })

# History page
elif page == "History":
    st.header("Verification History")

    if st.session_state.history:
        for index, record in enumerate(
            reversed(st.session_state.history), start=1
        ):
            st.subheader(f"Record {index}")
            st.write("**File:**", record["file"])
            st.write("**SHA-256:**")
            st.code(record["hash"], language="text")
            st.write("**Status:**", record["status"])
            st.divider()
    else:
        st.info("No history available yet.")

# About page
elif page == "About":
    st.header("About This Project")
    st.write(
        "The File Integrity Checker is a Cyber and Network Security "
        "mini-project that uses the SHA-256 cryptographic hash algorithm "
        "to identify changes in files."
    )

    st.subheader("Technology Used")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- SHA-256")
    st.write("- hashlib library")

    st.write("**Project:** CNS - File Integrity Checker")
