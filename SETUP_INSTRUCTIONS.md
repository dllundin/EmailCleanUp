# Gmail Lensa Cleanup - Setup Instructions

## Folder Structure
Create the following directory structure:
```
C:\AI\EmailCleanUp\
├── gmail_lensa_cleanup.py
├── setup.bat
├── run_cleanup.bat
├── credentials.json (generated after first run)
├── gmail_token.json (generated after first run)
└── logs\
    └── cleanup_log.txt (auto-created on first run)
```

## Step 1: Create Directories

```powershell
mkdir C:\AI\EmailCleanUp
mkdir C:\AI\EmailCleanUp\logs
```

## Step 2: Install Python Dependencies

Run `setup.bat` or manually run:

```powershell
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Step 3: Get Gmail API Credentials

1. Go to https://console.cloud.google.com/
2. Create a new project (name it "Email Cleanup" or similar)
3. Search for and enable the **Gmail API**
4. Go to "Credentials" → Create OAuth 2.0 credentials
   - Application type: Desktop application
   - Download as JSON
5. Save the downloaded file as `credentials.json` in `C:\AI\EmailCleanUp\`

## Step 4: Test the Script

Run `run_cleanup.bat` or manually:

```powershell
cd C:\AI\EmailCleanUp
python gmail_lensa_cleanup.py
```

On first run:
- Browser will open asking for Gmail permission
- Click "Allow" to authorize
- Token will be saved locally for future runs

## Step 5: Schedule with Windows Task Scheduler

1. Open **Task Scheduler** (search in Windows)
2. Click **Create Basic Task**
3. Fill in details:
   - **Name:** Gmail Lensa Cleanup
   - **Description:** Automatically removes lensa.com job alert emails
   - **Trigger:** Daily (or any schedule)
   - **Repeat every:** 2 hours (on the detailed settings page)
4. **Action:**
   - Program: `python.exe` (or full path like `C:\Python312\python.exe`)
   - Arguments: `C:\AI\EmailCleanUp\gmail_lensa_cleanup.py`
   - Start in: `C:\AI\EmailCleanUp`
5. Click Finish

## Logs

Check results in: `C:\AI\EmailCleanUp\logs\cleanup_log.txt`

Each run appends a timestamp and list of deleted emails.

## Troubleshooting

**"credentials.json not found"**
- Download it from Google Cloud Console (see Step 3)
- Place in `C:\AI\EmailCleanUp\`

**"Permission denied when accessing logs"**
- Close the log file if open in editor
- Make sure Task Scheduler is running as your user (not SYSTEM)

**Script not running from Task Scheduler**
- Check that Python path is correct
- Test manually first with `run_cleanup.bat`
- Verify "Start in" folder is set to `C:\AI\EmailCleanUp`
