# FTP Brute Force Lab

This is an educational cybersecurity lab demonstrating FTP brute force attacks using credentials from the LinkedIn data breach.

## Components

### 1. Streamlit FTP Interface (`streamlit_ftp_app.py`)
A fake FTP server interface built with Streamlit that simulates a corporate FTP server.

**Features:**
- Login interface with username/password authentication
- 10 accounts created from LinkedIn breach data
- File browser with fake corporate documents
- Admin panel showing login attempts (accessible with admin account)
- Download functionality for fake files

**Credentials (from LinkedIn breach):**
- `michael123` / `123456`
- `jennifer88` / `password`
- `david2012` / `12345678`
- `admin` / `qwerty` (has access to admin panel)
- `robert1` / `abc123`
- `jessica` / `password1`
- `john.smith` / `123456789`
- `mary_jones` / `letmein`
- `william` / `monkey`
- `susan2023` / `1234567`

### 2. Running the Streamlit App

#### Local Testing:
```bash
# Install dependencies
pip install -r requirements_streamlit.txt

# Run the app
streamlit run streamlit_ftp_app.py
```

#### Deploy to Streamlit Cloud:
1. Push this repository to GitHub
2. Go to https://share.streamlit.io/
3. Deploy the `streamlit_ftp_app.py` file
4. The app will be available at a public URL

### 3. Fake Documents Structure
```
/
├── public/
│   ├── readme.txt
│   ├── company_info.pdf
│   └── welcome.doc
├── private/
│   ├── confidential.xlsx
│   ├── passwords.txt
│   └── employee_data.csv
├── reports/
│   ├── Q3_2023_financial.pdf
│   ├── Q4_2023_financial.pdf
│   └── annual_report.doc
└── backups/
    ├── database_backup_20231201.sql
    ├── website_backup.zip
    └── config_backup.tar.gz
```

### 4. Brute Force Script (Coming Soon)
A Python script that demonstrates brute force attacks against the FTP interface.

## Educational Purpose

This lab is designed for educational purposes to demonstrate:
- How weak passwords from data breaches can be exploited
- The importance of strong, unique passwords
- How brute force attacks work
- Security monitoring through login attempt tracking

**WARNING:** This is for educational use only. Never attempt brute force attacks on systems you don't own or have explicit permission to test.

## Next Steps

1. Deploy the Streamlit app
2. Create the brute force demonstration script
3. Use the lab to teach about password security and attack prevention