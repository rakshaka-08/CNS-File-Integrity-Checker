import streamlit as st
import hashlib
import os
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="File Integrity Checker",
    page_icon="🔐",
    layout="centered"
)

# CSV file used to store history
HISTORY_FILE = "history.csv"

# Function to calculate SHA-256 hash
def calculate_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()


# Function to save activity in CSV
def save_history(file_name, file_hash, status):
    record = {
        "File Name": file_name,
        "SHA-256 Hash": file_hash,
        "Date and Time": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "Status": status
    }

    df = pd.DataFrame([record])

    if os.path.exists(HISTORY_FILE):
        df.to_csv(
            HISTORY_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        df.to_csv(HISTORY_FILE, index=False)


# Function to load saved history
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            return pd.read_csv(HISTORY_FILE)
        except pd.errors.EmptyDataError:
            pass

    return pd.DataFrame(
        columns=[
            "File Name",
            "SHA-256 Hash",
            "Date and Time",
            "Status"
        ]
    )


# Main heading
st.title("🔐 File Integrity Checker")

st.write(
    "A simple application to generate SHA-256 hashes "
    "and verify the integrity of files."
)

st.divider()

# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose an option",
    [
        "Home",
        "Generate SHA-256 Hash",
        "Verify File Integrity",
        "History",
        "About"
    ]
)


# HOME PAGE
if page == "Home":

    st.header("Welcome!")

    st.write(
        "This application helps users check whether a file "
        "has been modified using the SHA-256 hashing algorithm."
    )

    st.subheader("Available Features")

    st.write("1. Generate SHA-256 hash of a file")
    st.write("2. Verify file integrity")
    st.write("3. View previous activities")
    st.write("4. Save history permanently using CSV storage")


# GENERATE HASH PAGE
elif page == "Generate SHA-256 Hash":

    st.header("Generate SHA-256 Hash")

    uploaded_file = st.file_uploader(
        "Upload a file",
        key="hash_upload"
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        file_hash = calculate_file_hash(file_bytes)

        st.success("SHA-256 hash generated successfully!")

        st.write("**File Name:**", uploaded_file.name)

        st.write("**SHA-256 Hash:**")

        st.code(file_hash)

        if st.button("Save Hash to History"):

            save_history(
                uploaded_file.name,
                file_hash,
                "Hash Generated"
            )

            st.success("Hash saved to history successfully!")


# VERIFY FILE INTEGRITY PAGE
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

        elif (
            len(original_hash.strip()) != 64
            or any(
                char not in "0123456789abcdefABCDEF"
                for char in original_hash.strip()
            )
        ):

            st.error("Please enter a valid SHA-256 hash.")

        else:

            file_bytes = uploaded_file.getvalue()

            current_hash = calculate_file_hash(file_bytes)

            st.write("**File Name:**", uploaded_file.name)

            st.write("**Current SHA-256 Hash:**")

            st.code(current_hash)

            if current_hash == original_hash.strip().lower():

                st.success(
                    "File is unchanged. Integrity verified!"
                )

                status = "Unchanged"

            else:

                st.error(
                    "File has been modified! Integrity check failed."
                )

                status = "Modified"

            # Save verification result automatically
            save_history(
                uploaded_file.name,
                current_hash,
                status
            )

            st.info("Verification result saved to history.")


# HISTORY PAGE
elif page == "History":

    st.header("Verification History")

    history = load_history()

    if not history.empty:

        st.write(
            "Below are the previously saved hashing "
            "and verification activities."
        )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        st.write("**Total Records:**", len(history))

        csv_data = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download History as CSV",
            data=csv_data,
            file_name="verification_history.csv",
            mime="text/csv"
        )

    else:

        st.info("No history available yet. Generate a hash or verify a file.")


# ABOUT PAGE
elif page == "About":

    st.header("About This Project")

    st.write(
        "The File Integrity Checker is a Cyber and Network "
        "Security mini-project that uses the SHA-256 "
        "cryptographic hashing algorithm to detect changes in files."
    )

    st.subheader("Technologies Used")

    st.write("- Python")
    st.write("- Streamlit")
    st.write("- SHA-256")
    st.write("- hashlib")
    st.write("- Pandas")
    st.write("- CSV file storage")

    st.write("**Project Name:** CNS - File Integrity Checker")