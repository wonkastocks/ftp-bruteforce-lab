import streamlit as st
import datetime
import base64
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import openpyxl
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import random

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

def create_sales_excel():
    """Create Excel file with fake sales data"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Q3 2023 Sales"
    
    # Headers
    headers = ["Date", "Product", "Quantity", "Unit Price", "Total", "Region", "Sales Rep"]
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)
        ws.cell(row=1, column=col).font = openpyxl.styles.Font(bold=True)
    
    # Sample data
    products = ["Widget Pro", "Super Widget", "Widget Lite", "Enterprise Widget", "Widget Plus"]
    regions = ["North", "South", "East", "West", "Central"]
    reps = ["J. Smith", "M. Johnson", "S. Williams", "R. Brown", "K. Davis"]
    
    row = 2
    for month in range(7, 10):  # July to September
        for day in range(1, 29, 3):
            date = f"2023-{month:02d}-{day:02d}"
            product = random.choice(products)
            quantity = random.randint(10, 100)
            unit_price = random.randint(50, 500)
            total = quantity * unit_price
            region = random.choice(regions)
            rep = random.choice(reps)
            
            ws.cell(row=row, column=1, value=date)
            ws.cell(row=row, column=2, value=product)
            ws.cell(row=row, column=3, value=quantity)
            ws.cell(row=row, column=4, value=f"${unit_price}")
            ws.cell(row=row, column=5, value=f"${total:,}")
            ws.cell(row=row, column=6, value=region)
            ws.cell(row=row, column=7, value=rep)
            row += 1
    
    # Auto-adjust column widths
    for column in ws.columns:
        max_length = max(len(str(cell.value)) for cell in column if cell.value)
        ws.column_dimensions[column[0].column_letter].width = max_length + 2
    
    # Save to bytes
    excel_buffer = BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    return excel_buffer.getvalue()

def create_financial_pdf(quarter, revenue, expenses):
    """Create PDF financial report"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "SecureCorp Financial Report")
    c.setFont("Helvetica", 16)
    c.drawString(50, height - 80, f"{quarter}")
    
    # Line
    c.line(50, height - 100, width - 50, height - 100)
    
    # Financial Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, "Executive Summary")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 160, f"Total Revenue: ${revenue}")
    c.drawString(50, height - 180, f"Total Expenses: ${expenses}")
    c.drawString(50, height - 200, f"Net Profit: ${int(revenue.replace('M', '')) - int(expenses.replace('M', ''))}M")
    
    # Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 250, "Revenue Breakdown")
    c.setFont("Helvetica", 11)
    y_pos = height - 280
    categories = [
        ("Software Licenses", "45%"),
        ("Support Services", "30%"),
        ("Consulting", "20%"),
        ("Training", "5%")
    ]
    for category, percentage in categories:
        c.drawString(70, y_pos, f"• {category}: {percentage}")
        y_pos -= 20
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "Confidential - SecureCorp Financial Report")
    c.drawString(width - 150, 50, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def create_employee_doc():
    """Create Word document with employee handbook"""
    doc = Document()
    
    # Title
    title = doc.add_heading('SecureCorp Employee Handbook', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add company info
    doc.add_heading('Welcome to SecureCorp', level=1)
    doc.add_paragraph(
        'SecureCorp is a leading technology company specializing in '
        'enterprise software solutions. Founded in 2010, we have grown '
        'to over 500 employees worldwide.'
    )
    
    # Mission Statement
    doc.add_heading('Our Mission', level=2)
    doc.add_paragraph(
        'To provide innovative, secure, and reliable software solutions '
        'that empower businesses to achieve their full potential.'
    )
    
    # Company Policies
    doc.add_heading('Company Policies', level=1)
    doc.add_heading('Work Hours', level=2)
    doc.add_paragraph('Standard work hours are 9:00 AM to 5:00 PM, Monday through Friday.')
    
    doc.add_heading('Remote Work Policy', level=2)
    doc.add_paragraph(
        'Employees may work remotely up to 3 days per week with manager approval. '
        'All remote work must be conducted from a secure location with reliable internet.'
    )
    
    # Benefits
    doc.add_heading('Employee Benefits', level=1)
    benefits = [
        'Health, Dental, and Vision Insurance',
        '401(k) with company matching',
        '20 days PTO + holidays',
        'Professional development budget',
        'Gym membership reimbursement'
    ]
    for benefit in benefits:
        doc.add_paragraph(f'• {benefit}', style='List Bullet')
    
    # Save to bytes
    doc_buffer = BytesIO()
    doc.save(doc_buffer)
    doc_buffer.seek(0)
    return doc_buffer.getvalue()

def create_database_backup():
    """Create SQL backup file"""
    sql_content = """-- SecureCorp Database Backup
-- Generated: 2023-12-01 03:00:00
-- Database: securecorp_prod

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Database: `securecorp_prod`
CREATE DATABASE IF NOT EXISTS `securecorp_prod` DEFAULT CHARACTER SET utf8mb4;
USE `securecorp_prod`;

-- Table structure for table `employees`
DROP TABLE IF EXISTS `employees`;
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` varchar(10) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `department` varchar(50) NOT NULL,
  `hire_date` date NOT NULL,
  `salary` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample data for `employees`
INSERT INTO `employees` VALUES
(1,'EMP001','John','Doe','john.doe@securecorp.com','Engineering','2020-01-15',95000.00),
(2,'EMP002','Jane','Smith','jane.smith@securecorp.com','Marketing','2019-03-22',85000.00),
(3,'EMP003','Michael','Johnson','michael.j@securecorp.com','Sales','2021-06-10',78000.00),
(4,'EMP004','Sarah','Williams','sarah.w@securecorp.com','HR','2018-11-05',72000.00),
(5,'EMP005','Robert','Brown','robert.b@securecorp.com','Engineering','2022-02-28',102000.00);

-- Table structure for table `customers`
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(100) NOT NULL,
  `contact_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `contract_value` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

COMMIT;
"""
    return sql_content.encode()

def login_page():
    """Display login page"""
    st.markdown("""
    <style>
    .login-container {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 5px;
        margin: 20px auto;
        max-width: 400px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("SecureCorp FTP Server")
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
        st.caption("FTP Server v2.1.3 | Port: 21 | Protocol: FTP/FTPS")

def file_browser():
    """Display file browser interface with traditional FTP listing"""
    # Custom CSS for FTP-like interface
    st.markdown("""
    <style>
    .ftp-listing {
        font-family: monospace;
        background-color: #1e1e1e;
        color: #00ff00;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .ftp-header {
        color: #ffffff;
        background-color: #333;
        padding: 5px 10px;
        margin-bottom: 10px;
        border-radius: 3px;
    }
    .stButton > button {
        background-color: transparent;
        color: #0084ff;
        border: none;
        padding: 0;
        text-decoration: underline;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"### 📁 FTP File Browser - Connected as: **{st.session_state.username}**")
    with col2:
        if st.button("Logout", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_path = "/"
            st.rerun()
    
    # Current directory display
    st.markdown(f"**Current Directory:** `{st.session_state.current_path}`")
    
    # File listing header
    st.markdown("""
    <div class="ftp-header">
    <pre>Permissions    Size     Date Modified    Name</pre>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    if st.session_state.current_path != "/":
        if st.button("📁 ..", key="parent_dir"):
            st.session_state.current_path = "/"
            st.rerun()
    
    # Define file structure with real files
    if st.session_state.current_path == "/":
        files = [
            ("drwxr-xr-x", "4096", "Nov 15 09:30", "public", True),
            ("drwx------", "4096", "Nov 20 14:15", "private", True),
            ("drwxr-xr-x", "4096", "Dec 01 08:45", "reports", True),
            ("drwxr-xr-x", "4096", "Dec 01 03:00", "backups", True),
        ]
    elif st.session_state.current_path == "/public":
        files = [
            ("-rw-r--r--", "1234", "Nov 10 12:00", "readme.txt", False),
            ("-rw-r--r--", "45678", "Nov 12 15:30", "company_brochure.pdf", False),
            ("-rw-r--r--", "23456", "Nov 14 09:15", "welcome_packet.docx", False),
        ]
    elif st.session_state.current_path == "/private":
        files = [
            ("-rw-------", "98765", "Nov 18 16:45", "salary_data.xlsx", False),
            ("-rw-------", "2345", "Nov 19 10:30", "passwords.txt", False),
            ("-rw-------", "87654", "Nov 20 14:00", "employee_records.xlsx", False),
        ]
    elif st.session_state.current_path == "/reports":
        files = [
            ("-rw-r--r--", "156789", "Sep 30 17:00", "Q3_2023_financial.pdf", False),
            ("-rw-r--r--", "167890", "Oct 31 17:00", "Q4_2023_financial.pdf", False),
            ("-rw-r--r--", "234567", "Dec 15 12:00", "annual_report_2023.docx", False),
            ("-rw-r--r--", "345678", "Dec 20 14:30", "sales_analysis_2023.xlsx", False),
        ]
    elif st.session_state.current_path == "/backups":
        files = [
            ("-rw-r--r--", "5678901", "Dec 01 03:00", "database_backup_20231201.sql", False),
            ("-rw-r--r--", "8901234", "Dec 01 03:00", "website_backup.tar.gz", False),
            ("-rw-r--r--", "2345678", "Dec 01 03:00", "config_backup.zip", False),
        ]
    else:
        files = []
    
    # Display files
    for perms, size, date, name, is_dir in files:
        col1, col2, col3, col4 = st.columns([3, 1, 2, 4])
        
        with col1:
            st.text(perms)
        with col2:
            st.text(size)
        with col3:
            st.text(date)
        with col4:
            if is_dir:
                if st.button(f"📁 {name}", key=f"dir_{name}"):
                    st.session_state.current_path = f"/{name}"
                    st.rerun()
            else:
                # Generate file content based on filename
                file_content = generate_file_content(name)
                
                st.download_button(
                    label=f"📄 {name}",
                    data=file_content,
                    file_name=name,
                    mime=get_mime_type(name),
                    key=f"download_{name}"
                )
    
    # Server info
    st.markdown("---")
    st.caption(f"Server: ftp.securecorp.com | Connected: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Transfer Mode: Binary")

def generate_file_content(filename):
    """Generate appropriate content based on filename"""
    if filename == "readme.txt":
        return b"""SecureCorp FTP Server
=====================

Welcome to the SecureCorp FTP server. This server contains company documents,
reports, and resources for authorized personnel only.

Directory Structure:
- /public    : Public company information and resources
- /private   : Confidential documents (restricted access)
- /reports   : Financial and business reports
- /backups   : System and database backups

For support, contact: support@securecorp.com
"""
    
    elif filename == "passwords.txt":
        return b"""CONFIDENTIAL - System Passwords
================================

Database Server:
- Host: db.securecorp.local
- Admin: dbadmin / P@ssw0rd2023!

Email Server:
- Host: mail.securecorp.com
- Admin: mailadmin / M@ilSecure#456

Backup System:
- Host: backup.securecorp.local
- Admin: backupadmin / B@ckup!789

WiFi Networks:
- SecureCorp-Guest: Welcome2023
- SecureCorp-Staff: Staff#Secure$2023

IMPORTANT: Change these passwords regularly!
"""
    
    elif filename.endswith('.pdf'):
        if 'financial' in filename:
            if 'Q3' in filename:
                return create_financial_pdf("Q3 2023", "2.5M", "1.8M")
            elif 'Q4' in filename:
                return create_financial_pdf("Q4 2023", "3.1M", "2.0M")
            else:
                return create_financial_pdf("Q2 2023", "2.2M", "1.6M")
        else:
            # Company brochure
            return create_financial_pdf("Company Overview", "10.2M", "7.1M")
    
    elif filename.endswith('.xlsx'):
        if 'salary' in filename or 'employee' in filename:
            return create_employee_excel()
        else:
            return create_sales_excel()
    
    elif filename.endswith('.docx'):
        return create_employee_doc()
    
    elif filename.endswith('.sql'):
        return create_database_backup()
    
    elif filename.endswith('.zip') or filename.endswith('.tar.gz'):
        # Create a simple text file as placeholder
        return b"[Binary archive file - Contains compressed backup data]"
    
    else:
        return b"File content not available"

def create_employee_excel():
    """Create Excel with employee data"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Employee Data"
    
    # Headers
    headers = ["Employee ID", "Name", "Department", "Position", "Salary", "Start Date", "Email"]
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)
        ws.cell(row=1, column=col).font = openpyxl.styles.Font(bold=True)
    
    # Employee data
    employees = [
        ("EMP001", "John Doe", "Engineering", "Senior Developer", "$95,000", "2020-01-15", "john.doe@securecorp.com"),
        ("EMP002", "Jane Smith", "Marketing", "Marketing Manager", "$85,000", "2019-03-22", "jane.smith@securecorp.com"),
        ("EMP003", "Michael Johnson", "Sales", "Sales Representative", "$78,000", "2021-06-10", "michael.j@securecorp.com"),
        ("EMP004", "Sarah Williams", "HR", "HR Specialist", "$72,000", "2018-11-05", "sarah.w@securecorp.com"),
        ("EMP005", "Robert Brown", "Engineering", "Lead Engineer", "$102,000", "2022-02-28", "robert.b@securecorp.com"),
        ("EMP006", "Lisa Davis", "Finance", "Financial Analyst", "$80,000", "2020-09-14", "lisa.d@securecorp.com"),
        ("EMP007", "James Wilson", "IT", "System Administrator", "$88,000", "2019-07-20", "james.w@securecorp.com"),
        ("EMP008", "Patricia Garcia", "Sales", "Sales Director", "$110,000", "2017-04-03", "patricia.g@securecorp.com"),
    ]
    
    for row, employee in enumerate(employees, 2):
        for col, value in enumerate(employee, 1):
            ws.cell(row=row, column=col, value=value)
    
    # Auto-adjust columns
    for column in ws.columns:
        max_length = max(len(str(cell.value)) for cell in column if cell.value)
        ws.column_dimensions[column[0].column_letter].width = max_length + 2
    
    excel_buffer = BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    return excel_buffer.getvalue()

def get_mime_type(filename):
    """Get MIME type based on file extension"""
    if filename.endswith('.txt'):
        return 'text/plain'
    elif filename.endswith('.pdf'):
        return 'application/pdf'
    elif filename.endswith('.xlsx'):
        return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif filename.endswith('.docx'):
        return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif filename.endswith('.sql'):
        return 'application/sql'
    elif filename.endswith('.zip'):
        return 'application/zip'
    elif filename.endswith('.tar.gz'):
        return 'application/gzip'
    else:
        return 'application/octet-stream'

def admin_panel():
    """Display admin panel with login attempts"""
    if st.session_state.username == "admin":
        st.markdown("---")
        st.markdown("### 🔍 Admin Panel - Login Attempts")
        
        if st.session_state.login_attempts:
            df = pd.DataFrame(st.session_state.login_attempts)
            st.dataframe(df, use_container_width=True)
            
            # Stats
            total_attempts = len(df)
            successful = len(df[df['success'] == True])
            failed = len(df[df['success'] == False])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Attempts", total_attempts)
            with col2:
                st.metric("Successful", successful)
            with col3:
                st.metric("Failed", failed)
            
            # Download attempts as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Login Log",
                data=csv,
                file_name=f"ftp_login_attempts_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
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
    
    init_session_state()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        file_browser()
        admin_panel()

if __name__ == "__main__":
    main()