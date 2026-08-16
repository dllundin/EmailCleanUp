# Gmail Domain Cleanup - Setup Instructions

## Folder Structure
```
C:\_AI\EmailCleanUp\
├── gmail_domain_cleanup.py
├── domains.txt (copy from domains.example.txt, edit with your domains)
├── setup.bat
├── run_cleanup.bat
├── credentials.json (from Google Cloud Console)
├── gmail_token.json (generated after first run)
└── Output\
    ├── lensa.com.txt (auto-created, rolling log per domain)
    └── indeed.com.txt
```

## Step 1: Install Python Dependencies

Run `setup.bat` or manually run:

```powershell
pip install -r requirements.txt
```

## Step 2: Get Gmail API Credentials

1. Go to https://console.cloud.google.com/
2. Create a new project (name it "Email Cleanup" or similar)
3. Search for and enable the **Gmail API**
4. Go to "Credentials" → Create OAuth 2.0 credentials
   - Application type: Desktop application
   - Download as JSON
5. Save the downloaded file as `credentials.json` in `C:\_AI\EmailCleanUp\`

## Step 3: Set Your Domain List

Copy `domains.example.txt` to `domains.txt` and add one domain per line
(e.g. `lensa.com`). Any inbox email sent from `@<domain>` will be trashed.

## Step 4: Test the Script

Run `run_cleanup.bat --dry-run` first to preview matches, then run for real:

```powershell
cd C:\_AI\EmailCleanUp
python gmail_domain_cleanup.py --dry-run
python gmail_domain_cleanup.py
```

On first run:
- Browser will open asking for Gmail permission
- Click "Allow" to authorize
- Token will be saved locally for future runs

## Step 5: Schedule with Windows Task Scheduler

1. Open **Task Scheduler** (search in Windows)
2. Click **Create Basic Task**
3. Fill in details:
   - **Name:** Gmail Domain Cleanup
   - **Description:** Automatically removes emails from domains listed in domains.txt
   - **Trigger:** Daily (or any schedule)
   - **Repeat every:** 2 hours (on the detailed settings page)
4. **Action:**
   - Program: `python.exe` (or full path like `C:\Python312\python.exe`)
   - Arguments: `C:\_AI\EmailCleanUp\gmail_domain_cleanup.py`
   - Start in: `C:\_AI\EmailCleanUp`
5. Click Finish

## Logs

Each domain gets its own rolling log file: `C:\_AI\EmailCleanUp\Output\<domain>.txt`

Every run appends a timestamped entry to that domain's file — a list of deleted
emails, or "No matching emails." if there were none. This lets you track a
single domain's history over time and confirm the scheduled job is actually running.

## Troubleshooting

**"credentials.json not found"**
- Download it from Google Cloud Console (see Step 2)
- Place in `C:\_AI\EmailCleanUp\`

**"Domains file not found" or "No domains found"**
- Copy `domains.example.txt` to `domains.txt`
- Add at least one domain, one per line

**"Permission denied when accessing logs"**
- Close the log file if open in editor
- Make sure Task Scheduler is running as your user (not SYSTEM)

**Script not running from Task Scheduler**
- Check that Python path is correct
- Test manually first with `run_cleanup.bat`
- Verify "Start in" folder is set to `C:\_AI\EmailCleanUp`
