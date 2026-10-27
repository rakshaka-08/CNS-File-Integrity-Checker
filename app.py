
import streamlit as st
import hashlib
import os
import pandas as pd
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="File Integrity Checker",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #f5f7ff, #eef2ff);
}

/* Main content */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}

/* Headings */
h1 {
    color: #182848 !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2, h3 {
    color: #263b68 !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172554, #312e81);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 10px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08);
    padding: 10px 14px;
    border-radius: 10px;
    transition: 0.2s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.2);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.3rem;
    font-weight: 700;
    min-height: 45px;
    transition: all 0.25s ease;
    box-shadow: 0 4px 12px rgba(79,70,229,0.22);
}

.stButton > button:hover {
    background: linear-gradient(90deg, #3730a3, #6d28d9);
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(79,70,229,0.3);
}

.stButton > button:active {
    transform: scale(0.97);
}

/* Download buttons */
.stDownloadButton > button {
    background: #0f766e;
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 45px;
}

.stDownloadButton > button:hover {
    background: #115e59;
}

/* Input fields */
.stTextInput input {
    border-radius: 9px;
    border: 1px solid #c7d2fe;
    background: white;
}

/* File uploader */
section[data-testid="stFileUploader"] {
    background: white;
    border: 2px dashed #818cf8;
    border-radius: 12px;
    padding: 12px;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Dataframes */
.stDataFrame {
    border: 1px solid #dbe3f5;
    border-radius: 10px;
    overflow: hidden;
}

/* Dividers */
hr {
    border-color: #c7d2fe;
}

/* Responsive design */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }

    h1 {
        font-size: 1.8rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# CSV FILES
# ==========================================

HISTORY_FILE = "history.csv"
REFERENCE_FILE = "references.csv"


# ==========================================
# SHA-256 HASH FUNCTION
# ==========================================

def calculate_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()


# ==========================================
# HISTORY FUNCTIONS
# ==========================================

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


# ==========================================
# HASH REFERENCE FUNCTIONS
# ==========================================

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


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown(
    """
    <h1 style="color:white; font-size:25px;">
    🔐 File Integrity
    </h1>
    <p style="color:#c7d2fe; font-size:13px;">
    SHA-256 Security Dashboard
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Generate SHA-256 Hash",
        "Verify File Integrity",
        "History",
        "Manage Hash References",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "CNS Mini Project | Secure File Verification"
)


# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

    st.title("🔐 File Integrity Checker")

    st.markdown(
        """
        <p style="font-size:17px; color:#64748b;">
        Secure your files with SHA-256 cryptographic hashing.
        Generate hashes, verify file integrity and manage
        original hash references in one place.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Dashboard Features")

    col1, col2 = st.columns(2)

    with col1:
        st.info("🔐 **SHA-256 Hash Generation**")
        st.write(
            "Generate unique cryptographic hashes for your files."
        )

        st.info("🛡️ **File Integrity Verification**")
        st.write(
            "Detect whether a file has been modified."
        )

    with col2:
        st.info("📋 **Verification History**")
        st.write(
            "View previously saved file hashing and verification activities."
        )

        st.info("🔑 **Hash Reference Management**")
        st.write(
            "Save and reuse original SHA-256 hashes."
        )

    st.divider()

    st.subheader("Project Overview")

    col1, col2, col3 = st.columns(3)

    history = load_history()
    references = load_references()

    with col1:
        st.metric(
            "Total Activities",
            len(history)
        )

    with col2:
        st.metric(
            "Saved References",
            len(references)
        )

    with col3:
        st.metric(
            "Hash Algorithm",
            "SHA-256"
        )


# ==========================================
# GENERATE HASH PAGE
# ==========================================

elif page == "Generate SHA-256 Hash":

    st.title("🔐 Generate SHA-256 Hash")

    st.write(
        "Upload a file to generate its unique SHA-256 hash."
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        key="hash_upload"
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        file_hash = calculate_file_hash(file_bytes)

        st.success("Hash generated successfully!")

        st.write("**File Name:**", uploaded_file.name)

        st.write("**SHA-256 Hash:**")

        st.code(file_hash)

        if st.button("💾 Save Hash to History"):

            save_history(
                uploaded_file.name,
                file_hash,
                "Hash Generated"
            )

            st.success("Hash saved successfully!")


# ==========================================
# VERIFY FILE INTEGRITY PAGE
# ==========================================

elif page == "Verify File Integrity":

    st.title("🛡️ Verify File Integrity")

    st.write(
        "Compare the current file hash with its original SHA-256 hash."
    )

    uploaded_file = st.file_uploader(
        "Upload the file to verify",
        key="verify_upload"
    )

    references = load_references()

    original_hash = ""

    if not references.empty:

        hash_source = st.radio(
            "Choose original hash source",
            [
                "Use Saved Reference",
                "Enter Hash Manually"
            ]
        )

        if hash_source == "Use Saved Reference":

            selected_index = st.selectbox(
                "Select saved hash reference",
                references.index,
                format_func=lambda i: (
                    str(references.loc[i, "File Name"])
                    + " - "
                    + str(references.loc[i, "Date Saved"])
                )
            )

            original_hash = str(
                references.loc[
                    selected_index,
                    "SHA-256 Hash"
                ]
            )

        else:

            original_hash = st.text_input(
                "Enter original SHA-256 hash"
            )

    else:

        st.info(
            "No saved references available. "
            "You can enter the original hash manually."
        )

        original_hash = st.text_input(
            "Enter original SHA-256 hash"
        )

    if st.button("🔍 Verify File"):

        if uploaded_file is None:

            st.warning("Please upload a file.")

        elif not original_hash.strip():

            st.warning("Please enter or select an original hash.")

        elif (
            len(original_hash.strip()) != 64
            or any(
                char not in "0123456789abcdefABCDEF"
                for char in original_hash.strip()
            )
        ):

            st.error("Please enter a valid SHA-256 hash.")

        else:

            current_hash = calculate_file_hash(
                uploaded_file.getvalue()
            )

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

            st.info(
                "Verification result saved to history."
            )


# ==========================================
# HISTORY PAGE
# ==========================================

elif page == "History":

    st.title("📋 Verification History")

    st.write(
        "View your previously saved hashing and verification activities."
    )

    history = load_history()

    if not history.empty:

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Total Records",
            len(history)
        )

        csv_data = history.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download History as CSV",
            data=csv_data,
            file_name="verification_history.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No history available yet. Generate a hash or verify a file."
        )


# ==========================================
# HASH REFERENCE MANAGEMENT PAGE
# ==========================================

elif page == "Manage Hash References":

    st.title("🔑 Manage Hash References")

    st.write(
        "Save original SHA-256 hashes and reuse them for future verification."
    )

    st.divider()

    st.subheader("Save New Hash Reference")

    uploaded_file = st.file_uploader(
        "Upload a file",
        key="reference_upload"
    )

    if uploaded_file is not None:

        file_hash = calculate_file_hash(
            uploaded_file.getvalue()
        )

        st.write("**File Name:**", uploaded_file.name)

        st.write("**Original SHA-256 Hash:**")

        st.code(file_hash)

        if st.button("💾 Save Hash Reference"):

            save_reference(
                uploaded_file.name,
                file_hash
            )

            st.success(
                "Original hash reference saved successfully!"
            )

    st.divider()

    st.subheader("Previously Saved References")

    references = load_references()

    if not references.empty:

        st.dataframe(
            references,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Total Saved References",
            len(references)
        )

        selected_index = st.selectbox(
            "Select a saved reference",
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
            "No saved references available. Upload a file "
            "and save its original hash."
        )


# ==========================================
# ABOUT PAGE
# ==========================================

elif page == "About":

    st.title("ℹ️ About This Project")

    st.markdown(
        """
        ### File Integrity Checker

        The File Integrity Checker is a Cyber and Network
        Security mini-project that uses the SHA-256
        cryptographic hashing algorithm to identify changes
        in files.

        ### Technologies Used

        - Python
        - Streamlit
        - SHA-256
        - hashlib
        - Pandas
        - CSV storage

        ### Main Features

        - Generate SHA-256 hashes.
        - Verify file integrity.
        - Detect modified files.
        - Store verification history.
        - Manage original hash references.
        - Download history records.

        ### Project Information

        **Project:** CNS - File Integrity Checker

        **Contributors:** Diya and Raksha
        """
    )

    st.divider()

    st.success(
        "Thank you for using the File Integrity Checker!"
    )
