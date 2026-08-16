"""Trash Gmail inbox emails sent from domains listed in a local file.

Usage:
    python gmail_domain_cleanup.py [--domains-file domains.txt] [--dry-run] [--max-per-domain N]

--max-per-domain limits how many emails are deleted per domain per run. If
omitted or 0, all matching emails are deleted.

On first run this opens a browser window to authorize access to the Gmail
account via OAuth (using credentials.json). The resulting token is cached in
gmail_token.json so future runs are non-interactive.

Matching emails are moved to Trash (recoverable for ~30 days), never
permanently deleted.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

BASE_DIR = Path(__file__).parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "gmail_token.json"
DEFAULT_DOMAINS_FILE = BASE_DIR / "domains.txt"
OUTPUT_DIR = BASE_DIR / "Output"


def load_domains(domains_file: Path) -> list[str]:
    if not domains_file.exists():
        sys.exit(
            f"Domains file not found: {domains_file}\n"
            f"Create {domains_file.name} with one domain per line and add your domains."
        )

    domains = []
    for line in domains_file.read_text(encoding="utf-8").splitlines():
        line = line.strip().lower()
        if not line or line.startswith("#"):
            continue
        domains.append(line)

    if not domains:
        sys.exit(f"No domains found in {domains_file}. Add at least one domain, one per line.")

    return domains


def get_gmail_service():
    if not CREDENTIALS_FILE.exists():
        sys.exit(
            f"credentials.json not found at {CREDENTIALS_FILE}\n"
            "Download OAuth credentials from Google Cloud Console and save them there."
        )

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("gmail", "v1", credentials=creds)


def list_message_ids(service, query: str, limit: int = 0) -> list[str]:
    ids = []
    page_token = None
    while True:
        response = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=page_token)
            .execute()
        )
        ids.extend(m["id"] for m in response.get("messages", []))
        if limit and len(ids) >= limit:
            return ids[:limit]
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return ids


def get_message_summary(service, message_id: str) -> dict:
    msg = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        )
        .execute()
    )
    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    return {
        "id": message_id,
        "from": headers.get("From", "(unknown sender)"),
        "subject": headers.get("Subject", "(no subject)"),
        "date": headers.get("Date", "(unknown date)"),
    }


def daily_output_dir() -> Path:
    day_dir = OUTPUT_DIR / datetime.now().strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    return day_dir


def domain_log_file(domain: str) -> Path:
    safe_name = "".join(c if c.isalnum() or c in ".-_" else "_" for c in domain)
    return daily_output_dir() / f"{safe_name}.txt"


def append_domain_log(domain: str, dry_run: bool, summaries: list[dict], error: str | None) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"Run: {timestamp}"
    if dry_run:
        header += " (DRY RUN - nothing deleted)"

    lines = ["=" * 80, header, "=" * 80]
    if error:
        lines.append(f"Error searching {domain}: {error}")
    elif not summaries:
        lines.append("No matching emails.")
    else:
        action = "Would delete" if dry_run else "Deleted"
        lines.append(f"{action} {len(summaries)} email(s) from {domain}:")
        for i, s in enumerate(summaries, 1):
            lines.append(f"{i}. Date: {s['date']}")
            lines.append(f"   Sender: {s['from']}")
            lines.append(f"   Subject: {s['subject']}")
    lines.append("")

    with domain_log_file(domain).open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def cleanup(domains_file: Path, dry_run: bool, max_per_domain: int = 0) -> None:
    domains = load_domains(domains_file)
    service = get_gmail_service()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_deleted = 0

    for domain in domains:
        query = f"in:inbox from:@{domain}"
        try:
            message_ids = list_message_ids(service, query, limit=max_per_domain)
        except HttpError as e:
            print(f"Error searching for domain {domain}: {e}", file=sys.stderr)
            append_domain_log(domain, dry_run, [], str(e))
            continue

        if not message_ids:
            print(f"{domain}: no matching emails")
            append_domain_log(domain, dry_run, [], None)
            continue

        summaries = []
        for message_id in message_ids:
            try:
                summaries.append(get_message_summary(service, message_id))
            except HttpError as e:
                print(f"Error reading message {message_id}: {e}", file=sys.stderr)

        action = "Would delete" if dry_run else "Deleted"
        print(f"{domain}: {action.lower()} {len(summaries)} email(s)")

        if not dry_run:
            for s in summaries:
                try:
                    service.users().messages().trash(userId="me", id=s["id"]).execute()
                    total_deleted += 1
                except HttpError as e:
                    print(f"Error trashing message {s['id']}: {e}", file=sys.stderr)
        else:
            total_deleted += len(summaries)

        append_domain_log(domain, dry_run, summaries, None)

    summary = f"Total {'would-delete' if dry_run else 'deleted'}: {total_deleted}"
    print(summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--domains-file",
        type=Path,
        default=DEFAULT_DOMAINS_FILE,
        help="Path to file listing domains, one per line (default: domains.txt)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview matching emails without moving them to trash",
    )
    parser.add_argument(
        "--max-per-domain",
        type=int,
        default=1,
        help="Max number of emails to delete per domain per run. "
        "Omit or use 0 to delete all matches (default: 0)",
    )
    args = parser.parse_args()
    if args.max_per_domain < 0:
        parser.error("--max-per-domain must be 0 or a positive integer")
    cleanup(args.domains_file, args.dry_run, args.max_per_domain)


if __name__ == "__main__":
    main()
