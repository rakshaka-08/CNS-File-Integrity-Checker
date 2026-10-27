
import streamlit as st
import hashlib
import os
import pandas as pd
from datetime import datetime

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="File Integrity Checker",
    page_icon="🔐",
    layout="centered"
)

# CSV storage files
HISTORY_FILE = "history.csv"
REFERENCE_FILE = "references.csv"


# --------------------------------
# SHA-256 HASH FUNCTION
# --------------------------------

def calculate_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()


# --------------------------------
# VERIFICATION HISTORY FUNCTIONS
# --------------------------------

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


# --------------------------------
# HASH REFERENCE FUNCTIONS
# --------------------------------

def save_reference(file_name, file_hash):

    record = {
        "File Name": file_name,
        "SHA-256 Hash": file_hash,
        "Date Saved": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    }

    df = pd.DataFrame([record])

    if os.path.exists(REFERENCE_FILE):

        df.to_csv(
            REFERENCE_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:
        df.to_csv(REFERENCE_FILE, index=False)


def load_references():

    if os.path.exists(REFERENCE_FILE):

        try:
            return pd.read_csv(REFERENCE_FILE)

        except pd.errors.EmptyDataError:
            pass

    return pd.DataFrame(
        columns=[
            "File Name",
            "SHA-256 Hash",
            "Date Saved"
        ]
    )


# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------

st.sidebar.title("🔐 Navigation")

page = st.sidebar.radio(
    "Choose an option",
    [
        "Home",
        "Generate SHA-256 Hash",
        "Verify File Integrity",
        "History",
        "Manage Hash References",
        "About"
    ]
)


# --------------------------------
# HOME PAGE
# --------------------------------

if page == "Home":

    st.title("🔐 File Integrity Checker")

    st.write(
        "A simple application to generate SHA-256 hashes "
        "and verify the integrity of files."
    )

    st.divider()

    st.subheader("Available Features")

    st.write("1. Generate SHA-256 hash of a file")
    st.write("2. Verify file integrity")
    st.write("3. View previous verification activities")
    st.write("4. Save original hash references")
    st.write("5. Download history records")

    st.info(
        "Upload a file and use SHA-256 hashing "
        "to check whether its contents have changed."
    )


# --------------------------------
# GENERATE SHA-256 HASH PAGE
# --------------------------------

elif page == "Generate SHA-256 Hash":

    st.title("Generate SHA-256 Hash")

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


# --------------------------------
# VERIFY FILE INTEGRITY PAGE
# --------------------------------

elif page == "Verify File Integrity":

    st.title("Verify File Integrity")

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

            save_history(
                uploaded_file.name,
                current_hash,
                status
            )

            st.info("Verification result saved to history.")


# --------------------------------
# VERIFICATION HISTORY PAGE
# --------------------------------

elif page == "History":

    st.title("Verification History")

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

        csv_data = history.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download History as CSV",
            data=csv_data,
            file_name="verification_history.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No history available yet. Generate a hash "
            "or verify a file."
        )


# --------------------------------
# MANAGE HASH REFERENCES PAGE
# --------------------------------

elif page == "Manage Hash References":

    st.title("Manage Original Hash References")

    st.write(
        "Save original SHA-256 hashes and reuse them "
        "for future file integrity verification."
    )

    st.divider()

    st.subheader("Save a New Hash Reference")

    uploaded_file = st.file_uploader(
        "Upload a file to save its original hash",
        key="reference_upload"
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        file_hash = calculate_file_hash(file_bytes)

        st.write("**File Name:**", uploaded_file.name)

        st.write("**Original SHA-256 Hash:**")

        st.code(file_hash)

        if st.button("Save Hash Reference"):

            save_reference(
                uploaded_file.name,
                file_hash
            )

            st.success(
                "Original hash reference saved successfully!"
            )

    st.divider()

    st.subheader("Previously Saved Hash References")

    references = load_references()

    if not references.empty:

        st.dataframe(
            references,
            use_container_width=True,
            hide_index=True
        )

        st.write(
            "**Total Saved References:**",
            len(references)
        )

        selected_index = st.selectbox(
            "Select an original hash reference",
            references.index,
            format_func=lambda i: (
                str(references.loc[i, "File Name"])
                + " - "
                + str(references.loc[i, "Date Saved"])
            )
        )

        selected_hash = str(
            references.loc[
                selected_index,
                "SHA-256 Hash"
            ]
        )

        st.write("**Selected Original Hash:**")

        st.code(selected_hash)

    else:

        st.info(
            "No saved hash references available. "
            "Upload a file and save its original hash."
        )


# --------------------------------
# ABOUT PAGE
# --------------------------------

elif page == "About":

    st.title("About This Project")

    st.write(
        "The File Integrity Checker is a Cyber and Network "
        "Security mini-project that uses the SHA-256 "
        "cryptographic hashing algorithm to detect changes "
        "in files."
    )

    st.subheader("Technologies Used")

    st.write("- Python")
    st.write("- Streamlit")
    st.write("- SHA-256")
    st.write("- hashlib")
    st.write("- Pandas")
    st.write("- CSV file storage")

    st.divider()

    st.write("**Project Name:** CNS - File Integrity Checker")
