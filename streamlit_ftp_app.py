import streamlit as st
import datetime
import base64
from io import BytesIO
import pandas as pd

# LinkedIn breach credentials - 10 accounts
USERS = {
    "michael123": "123456",
    "jennifer88": "password",
    "david2012": "12345678",
    "admin": "qwerty",
    "robert1": "abc123",
    "jessica": "password1",
    "john.smith": "123456789",
    "mary_jones": "letmein",
    "william": "monkey",
    "susan2023": "1234567"
}

# Fake files structure
FAKE_FILES = {
    "/": {
        "type": "directory",
        "files": ["public", "private", "reports", "backups"]
    },
    "/public": {
        "type": "directory",
        "files": ["readme.txt", "company_info.pdf", "welcome.doc"]
    },
    "/private": {
        "type": "directory",
        "files": ["confidential.xlsx", "passwords.txt", "employee_data.csv"]
    },
    "/reports": {
        "type": "directory",
        "files": ["Q3_2023_financial.pdf", "Q4_2023_financial.pdf", "annual_report.doc"]
    },
    "/backups": {
        "type": "directory",
        "files": ["database_backup_20231201.sql", "website_backup.zip", "config_backup.tar.gz"]
    }
}

# Fake file contents
FILE_CONTENTS = {
    "readme.txt": "Welcome to SecureCorp FTP Server\n\nThis server contains company documents and resources.\nPlease ensure you follow security protocols.",
    "company_info.pdf": "SecureCorp Company Information\n\nFounded: 2010\nEmployees: 500+\nIndustry: Technology",
    "welcome.doc": "Welcome to SecureCorp!\n\nEmployee Onboarding Guide",
    "confidential.xlsx": "CONFIDENTIAL - Employee Salary Data\n\nID | Name | Department | Salary\n001 | John Doe | IT | $85,000\n002 | Jane Smith | HR | $75,000",
    "passwords.txt": "System Passwords (CONFIDENTIAL)\n\nDatabase: admin/P@ssw0rd123\nEmail Server: mail/SecureM@il2023\nBackup System: backup/B@ckup!456",
    "employee_data.csv": "ID,Name,Email,Department\n001,John Doe,john@securecorp.com,IT\n002,Jane Smith,jane@securecorp.com,HR",
    "Q3_2023_financial.pdf": "Q3 2023 Financial Report\n\nRevenue: $2.5M\nExpenses: $1.8M\nProfit: $700K",
    "Q4_2023_financial.pdf": "Q4 2023 Financial Report\n\nRevenue: $3.1M\nExpenses: $2.0M\nProfit: $1.1M",
    "annual_report.doc": "2023 Annual Report\n\nTotal Revenue: $10.2M\nGrowth: 23% YoY",
    "database_backup_20231201.sql": "-- Database backup\n-- Date: 2023-12-01\nCREATE DATABASE securecorp;\nUSE securecorp;",
    "website_backup.zip": "[Binary data - Website backup archive]",
    "config_backup.tar.gz": "[Binary data - Configuration backup]"
}

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'current_path' not in st.session_state:
        st.session_state.current_path = "/"
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = []

def log_attempt(username, password, success):
    """Log login attempts"""
    attempt = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "password": password,
        "success": success
    }
    st.session_state.login_attempts.append(attempt)

def login_page():
    """Display login page"""
    st.title("🔒 SecureCorp FTP Server")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### FTP Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button:
                if username in USERS and USERS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    log_attempt(username, password, True)
                    st.success("Login successful!")
                    st.rerun()
                else:
                    log_attempt(username, password, False)
                    st.error("Invalid username or password")
        
        st.markdown("---")
        st.caption("FTP Server v2.1.3 | Port: 21")

def get_file_icon(filename):
    """Get appropriate icon for file type"""
    if filename.endswith('.txt'):
        return "📄"
    elif filename.endswith('.pdf'):
        return "📕"
    elif filename.endswith('.doc'):
        return "📘"
    elif filename.endswith('.xlsx') or filename.endswith('.csv'):
        return "📊"
    elif filename.endswith('.sql'):
        return "🗄️"
    elif filename.endswith('.zip') or filename.endswith('.tar.gz'):
        return "📦"
    else:
        return "📄"

def file_browser():
    """Display file browser interface"""
    st.title(f"🗂️ SecureCorp FTP Server - {st.session_state.username}")
    
    # Logout button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_path = "/"
            st.rerun()
    
    st.markdown("---")
    
    # Display current path
    st.markdown(f"**Current Directory:** `{st.session_state.current_path}`")
    
    # Navigation buttons
    if st.session_state.current_path != "/":
        if st.button("⬆️ Go Up"):
            st.session_state.current_path = "/"
            st.rerun()
    
    # Display files and folders
    current_dir = FAKE_FILES.get(st.session_state.current_path, {})
    
    if "files" in current_dir:
        st.markdown("### 📁 Contents")
        
        for item in current_dir["files"]:
            col1, col2, col3 = st.columns([1, 4, 2])
            
            # Check if it's a directory
            item_path = f"{st.session_state.current_path}/{item}".replace("//", "/")
            is_directory = item_path in FAKE_FILES
            
            with col1:
                if is_directory:
                    st.markdown("📁")
                else:
                    st.markdown(get_file_icon(item))
            
            with col2:
                if is_directory:
                    if st.button(item, key=f"dir_{item}"):
                        st.session_state.current_path = item_path
                        st.rerun()
                else:
                    st.markdown(f"**{item}**")
            
            with col3:
                if not is_directory:
                    if st.button("Download", key=f"download_{item}"):
                        content = FILE_CONTENTS.get(item, "File content not available")
                        st.download_button(
                            label="💾 Save",
                            data=content,
                            file_name=item,
                            key=f"save_{item}"
                        )
    
    # Server info
    st.markdown("---")
    st.caption(f"Connected as: {st.session_state.username} | Server Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def admin_panel():
    """Display admin panel with login attempts"""
    if st.session_state.username == "admin":
        st.markdown("---")
        st.markdown("### 🔍 Admin Panel - Login Attempts")
        
        if st.session_state.login_attempts:
            df = pd.DataFrame(st.session_state.login_attempts)
            st.dataframe(df, use_container_width=True)
            
            # Download attempts as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Login Attempts",
                data=csv,
                file_name=f"login_attempts_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No login attempts recorded yet")

def main():
    """Main application"""
    st.set_page_config(
        page_title="SecureCorp FTP Server",
        page_icon="🔒",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        file_browser()
        admin_panel()

if __name__ == "__main__":
    main()