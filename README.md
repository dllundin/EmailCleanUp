# Email CleanUp

Automated email cleanup tool that searches Gmail for emails from lensa.com and moves them to trash on a scheduled basis.

## Overview

This project provides a Python script that:

- Searches Gmail for emails from `lensa.com` (job alert emails)  
- Automatically moves matching emails to trash  
- Logs all deleted emails with timestamps and details  
- Can be scheduled to run automatically every 2 hours (or any interval)

## Features

- **Automated cleanup** \- Remove unwanted job alert emails automatically  
- **Detailed logging** \- Track every deleted email with date, sender, and subject  
- **Easy scheduling** \- Windows Task Scheduler integration ready  
- **Gmail API** \- Uses official Google Gmail API for reliable access  
- **No data deletion** \- Emails go to Trash, not permanently deleted (can be recovered)

## Project Structure

EmailCleanUp/

├── gmail\_lensa\_cleanup.py      \# Main cleanup script

├── requirements.txt             \# Python dependencies

├── setup.bat                    \# Automated setup script

├── run\_cleanup.bat              \# Quick run script

├── .gitignore                   \# Git ignore rules

├── README.md                    \# This file

├── logs/                        \# Log files directory

│   └── cleanup\_log.txt          \# Cleanup history

└── credentials.json             \# Google API credentials (generated)

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

### 4\. Test the Script

**Option A: Using run\_cleanup.bat (Windows)**

run\_cleanup.bat

**Option B: Manual run**

python gmail\_lensa\_cleanup.py

On first run:

- A browser window will open asking for Gmail permission  
- Click **Allow** to authorize the app  
- Authorization token is saved locally for future runs

## Usage

### Run Manually

python gmail\_lensa\_cleanup.py

### Schedule with Windows Task Scheduler

1. Open **Task Scheduler**  
2. Click **Create Basic Task**  
3. Configure:  
   - **Name:** Gmail Lensa Cleanup  
   - **Description:** Automatically removes lensa.com job alert emails  
   - **Trigger:** Set to repeat every 2 hours (or your preferred interval)  
4. **Action:**  
   - Program: `python.exe` (or full path to Python)  
   - Arguments: `C:\AI\EmailCleanUp\gmail_lensa_cleanup.py`  
   - Start in: `C:\AI\EmailCleanUp`  
5. Click **Finish**

### Schedule with Cron (Linux/Mac)

Add to crontab to run every 2 hours:

0 \*/2 \* \* \* /usr/bin/python3 /path/to/gmail\_lensa\_cleanup.py

## Logs

All cleanup activity is logged to `logs/cleanup_log.txt`:

\================================================================================

Cleanup Run: 2026-08-16 14:26:23

\================================================================================

Deleted 10 email(s) from lensa.com:

1\. Date: Fri, 16 Aug 2026 14:26:23 \+0000

   Sender: jobalert@lensa.com

   Subject: Senior Firmware Engineer jobs in Lincolnshire, IL

2\. Date: Fri, 16 Aug 2026 15:00:00 \+0000

   Sender: jobalert@lensa.com

   Subject: 15 companies hiring Azure Developer in Rolling Meadows, IL

...

## Configuration

Edit `gmail_lensa_cleanup.py` to customize:

\# Change the search query

q='from:lensa.com'

\# Change log output directory

OUTPUT\_DIR \= Path(\_\_file\_\_).parent / 'logs'

## Troubleshooting

### "credentials.json not found"

- Download `credentials.json` from Google Cloud Console  
- Place it in the project root directory

### "Permission denied" when writing logs

- Check that the `logs/` directory exists and is writable  
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
| `gmail_lensa_cleanup.py` | Main cleanup script |
| `requirements.txt` | Python package dependencies |
| `setup.bat` | Windows setup automation |
| `run_cleanup.bat` | Quick run script |
| `README.md` | Documentation (this file) |
| `.gitignore` | Git ignore rules |

## License

MIT License \- see LICENSE file for details

## Support

For issues or questions:

1. Check the Troubleshooting section above  
2. Verify setup steps were followed correctly  
3. Check `logs/cleanup_log.txt` for error messages

## Future Enhancements

- [ ] Configuration file for custom search queries  
- [ ] Email templates for different senders  
- [ ] Web dashboard for monitoring  
- [ ] Support for other email providers  
- [ ] Docker containerization  
- [ ] Unit tests

---

**Last Updated:** August 16, 2026  
