# Email CleanUp

Automated email cleanup tool that searches Gmail for emails from a configurable list of domains and moves them to trash on a scheduled basis.

## Overview

This project provides a Python script that:

- Reads a list of domains from `domains.txt`
- Searches your Gmail inbox for emails sent from any of those domains
- Automatically moves matching emails to trash
- Logs every run to a rolling, timestamped text file per domain
- Supports `--dry-run` to preview what would be deleted first
- Supports `--max-per-domain N` to cap deletions per domain per run (0 or omitted = delete all matches)
- Can be scheduled to run automatically every 2 hours (or any interval)

## Features

- **Automated cleanup** \- Remove unwanted emails automatically  
- **Per-domain logging** \- Each domain gets its own rolling log file, timestamped on every run  
- **Easy scheduling** \- Windows Task Scheduler integration ready  
- **Gmail API** \- Uses official Google Gmail API for reliable access  
- **No data deletion** \- Emails go to Trash, not permanently deleted (can be recovered)

## Project Structure

EmailCleanUp/

├── gmail\_domain\_cleanup.py      \# Main cleanup script

├── domains.txt                  \# Your domain list (gitignored, edit this)

├── requirements.txt             \# Python dependencies

├── setup.bat                    \# Automated setup script

├── run\_cleanup.bat              \# Quick run script

├── .gitignore                   \# Git ignore rules

├── README.md                    \# This file

├── Output/                      \# Log files directory

│   └── 2026-08-16/              \# One subfolder per day, created on first run that day

│       ├── lensa.com.txt        \# Rolling log for lensa.com (one file per domain)

│       └── indeed.com.txt       \# Rolling log for indeed.com

├── credentials.json             \# Google API credentials

└── gmail\_token.json             \# Cached OAuth token (generated)

## Prerequisites

- Python 3.7+  
- Windows 10+ (or Python \+ bash on Linux/Mac)  
- Google account with Gmail access  
- Google Cloud project with Gmail API enabled

## Setup

### 1\. Clone the Repository

git clone https://github.com/dllundin/\_AI/EmailCleanUp.git

cd EmailCleanUp

### 2\. Install Dependencies

**Option A: Using setup.bat (Windows)**

setup.bat

**Option B: Manual installation**

pip install \-r requirements.txt

### 3\. Configure Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)  
2. Create a new project (e.g., "Email CleanUp")  
3. Search for and enable **Gmail API**  
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Desktop Application**  
5. Download the credentials file as JSON  
6. Save it as `credentials.json` in the project directory

### 4\. List the Domains to Clean Up

Create `domains.txt` in the project directory and add one domain per line (`#` for comments):

lensa.com
indeed.com

`setup.bat` will create an empty `domains.txt` for you if it doesn't exist yet.

### 5\. Test the Script

**Option A: Using run\_cleanup.bat (Windows)**

run\_cleanup.bat --dry-run

**Option B: Manual run**

python gmail\_domain\_cleanup.py --dry-run

Review `Output/<YYYY-MM-DD>/<domain>.txt` for each domain, then re-run without `--dry-run` to actually trash the matching emails.

On first run:

- A browser window will open asking for Gmail permission  
- Click **Allow** to authorize the app  
- Authorization token is saved locally (`gmail_token.json`) for future runs

## Usage

### Run Manually

python gmail\_domain\_cleanup.py

### Preview Without Deleting

python gmail\_domain\_cleanup.py --dry-run

### Use a Different Domains File

python gmail\_domain\_cleanup.py --domains-file other_domains.txt

### Limit How Many Emails Are Deleted Per Domain

python gmail\_domain\_cleanup.py --max-per-domain 25

Omit this flag, or pass `0`, to delete all matching emails for every domain.

### Schedule with Windows Task Scheduler

1. Open **Task Scheduler**  
2. Click **Create Basic Task**  
3. Configure:  
   - **Name:** Gmail Domain Cleanup  
   - **Description:** Automatically removes emails from domains listed in domains.txt  
   - **Trigger:** Set to repeat every 2 hours (or your preferred interval)  
4. **Action:**  
   - Program: `python.exe` (or full path to Python)  
   - Arguments: `C:\_AI\EmailCleanUp\gmail_domain_cleanup.py`  
   - Start in: `C:\_AI\EmailCleanUp`  
5. Click **Finish**

### Schedule with Cron (Linux/Mac)

Add to crontab to run every 2 hours:

0 \*/2 \* \* \* /usr/bin/python3 /path/to/gmail\_domain\_cleanup.py

## Logs

Each day's first run creates `Output/<YYYY-MM-DD>/`. Within that folder, each domain gets its own rolling log file at `Output/<YYYY-MM-DD>/<domain>.txt`. Every run appends a new timestamped entry, so history for that domain accumulates within the day:

\================================================================================

Run: 2026-08-16 14:26:23

\================================================================================

Deleted 10 email(s) from lensa.com:

1\. Date: Fri, 16 Aug 2026 14:26:23 \+0000

   Sender: jobalert@lensa.com

   Subject: Senior Firmware Engineer jobs in Lincolnshire, IL

2\. Date: Fri, 16 Aug 2026 15:00:00 \+0000

   Sender: jobalert@lensa.com

   Subject: 15 companies hiring Azure Developer in Rolling Meadows, IL

...

A run with no matches for a domain still appends a timestamped "No matching emails." entry, so you can see the job ran.

## Configuration

Edit `domains.txt` to add or remove domains (one per line, `#` for comments) — no code changes needed.

## Troubleshooting

### "Domains file not found" or "No domains found"

- Create `domains.txt` in the project directory  
- Add at least one domain, one per line

### "credentials.json not found"

- Download `credentials.json` from Google Cloud Console  
- Place it in the project root directory

### "Permission denied" when writing logs

- Check that the `Output/` directory exists and is writable  
- If running from Task Scheduler, ensure it runs as your user account

### Script not running from Task Scheduler

- Test manually first: `run_cleanup.bat`  
- Verify Python path is correct  
- Check Task Scheduler event logs for errors  
- Try running with full paths (e.g., `C:\Python312\python.exe`)

### "OAuth error" or authentication fails

- Delete `gmail_token.json` to force re-authentication  
- Ensure Gmail API is enabled in Google Cloud Console  
- Verify `credentials.json` is valid

## Security

⚠️ **Important:**

- **Do not commit** `credentials.json` or `gmail_token.json` to version control (already in .gitignore)  
- Keep API credentials private and secure  
- Regenerate credentials if they are accidentally exposed

## Files

| File | Purpose |
| :---- | :---- |
| `gmail_domain_cleanup.py` | Main cleanup script |
| `domains.txt` | Your list of domains to clean up (gitignored) |
| `requirements.txt` | Python package dependencies |
| `setup.bat` | Windows setup automation |
| `run_cleanup.bat` | Quick run script |
| `test_run.bat` | Like run_cleanup.bat, but pauses after so you can read the output |
| `README.md` | Documentation (this file) |
| `.gitignore` | Git ignore rules |

## License

MIT License \- see LICENSE file for details

## Support

For issues or questions:

1. Check the Troubleshooting section above  
2. Verify setup steps were followed correctly  
3. Check `Output/<YYYY-MM-DD>/<domain>.txt` for error messages

## Future Enhancements

- [ ] Web dashboard for monitoring  
- [ ] Support for other email providers  
- [ ] Docker containerization  
- [ ] Unit tests

---

**Last Updated:** August 16, 2026  
